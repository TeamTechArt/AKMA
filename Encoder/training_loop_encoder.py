import copy
import json
import os
import random
import pickle
import time
from pprint import pprint

import PIL.Image
import numpy as np
import torch
import torch.utils.tensorboard as tensorboard
from lpips import LPIPS
from torch.nn.parallel import DistributedDataParallel as DDP

import dnnlib
import legacy
from torch_utils import misc
from training.dataset_encoder import ImagesDataset
from training.loss_encoder import l2_loss, IDLoss
from training.networks_encoder import Encoder
from training.ranger import Ranger
from training.moco_loss import MocoLoss

#----------------------------------------------------------------------------

def save_image(images, save_path, gh, gw, H, W):
    np_imgs = []
    for i, image in enumerate(images):
        image = images[i][None,:,:]
        image = (image.permute(0,2,3,1)*127.5+128).clamp(0,255).to(torch.uint8).cpu().numpy()
        np_imgs.append(np.asarray(PIL.Image.fromarray(image[0], 'RGB').resize((H,W),PIL.Image.LANCZOS)))
    np_imgs = np.stack(np_imgs)
    np_imgs = np_imgs.reshape(gh,gw,H,W,3)
    np_imgs = np_imgs.transpose(0,2,1,3,4)
    np_imgs = np_imgs.reshape(gh*H, gw*W, 3)
    PIL.Image.fromarray(np_imgs, 'RGB').save(save_path)

#----------------------------------------------------------------------------

def training_loop(
    run_dir                 = '.',          # Output directory.
    rank                    = 0,            # Rank of the current process in [0, num_gpus].
    model_architecture      = 'base',       # Model architecture type, ['base', 'transformer']
    w_avg                   = False,        # Train delta w from w_avg
    num_encoder_layers      = 1,            # Encoder layers if model_architecture is transformer
    dataset_dir             = 'ffhq',       # Train dataset directory
    num_gpus                = 1,            # Number of GPUs participating in the training.
    batch_size              = 32,           # Total batch size for one training iteration. Can be larger than batch_gpu * num_gpus.
    batch_gpu               = 4,            # Number of samples processed at a time by one GPU.
    generator_pkl           = None,         # Generator pickle to encode.
    val_dataset_dir         = 'celeba-hq',  # Validation dataset directory
    training_steps          = 100001,       # Total training batch steps
    val_steps               = 10000,        # Validation batch steps 
    print_steps             = 50,           # How often to print logs
    tensorboard_steps       = 50,           # How often to log to tensorboard?
    image_snapshot_steps    = 100,          # How often to save image snapshots? None=disable.
    network_snapshot_steps  = 5000,         # How often to save network snapshots?
    learning_rate           = 0.001,        # Learning rate
    l2_lambda               = 1.0,          # L2 loss multiplier factor
    lpips_lambda            = 0.8,          # LPIPS loss multiplier factor
    moco_lambda               = 0.1,          # ID loss multiplier factor
    reg_lambda              = 0.0,          # e4e reg loss multiplier factor
    gan_lambda              = 0.0,          # e4e latent gan loss multiplier factor
    edit_lambda             = 0.0,          # e4e editability loss multiplier factor
    random_seed             = 0,            # Global random seed.
    num_workers             = 3,            # Dataloader workers.
    resume_pkl              = None,         # Network pickle to resume training from.
    cudnn_benchmark         = True,         # Enable torch.backends.cudnn.benchmark?
    d_lambda                =0.05
):

    # initialize
    device = torch.device('cuda', rank)

    # Reproducability
    random.seed(random_seed * num_gpus + rank)
    np.random.seed(random_seed * num_gpus + rank)
    torch.manual_seed(random_seed * num_gpus + rank)
    torch.cuda.manual_seed(random_seed * num_gpus + rank)
    torch.cuda.manual_seed_all(random_seed * num_gpus + rank)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = cudnn_benchmark 
    
    # Load training set.
    if rank == 0:
        print('Loading training set...')
    training_set = ImagesDataset(dataset_dir, mode='train')
    training_set_sampler = torch.utils.data.distributed.DistributedSampler(training_set, num_replicas=num_gpus, rank=rank, shuffle=True, seed=random_seed, drop_last=False)
    training_loader = torch.utils.data.DataLoader(dataset=training_set, sampler=training_set_sampler, batch_size=batch_size//num_gpus, num_workers=num_workers)
    if rank == 0:
        print()
        print('Num images: ', len(training_set))
        print('Image shape:', training_set.__getitem__(0)[0].shape)
        print()

    # Load validation set.

    # Construct networks.
    if rank == 0:
        print('Constructing networks...')
    with dnnlib.util.open_url(generator_pkl) as f:
        gan_data = legacy.load_network_pkl(f)
        G = gan_data['G_ema'].to(device)
        if d_lambda >0:
          D = gan_data['D'].to(device).eval()

    latent_avg = None
    if w_avg:
        latent_avg = G.mapping.w_avg
    if model_architecture == 'base':
        if resume_pkl is None:
            E = DDP(Encoder(pretrained=None,w_avg=latent_avg).to(device), device_ids=[rank])
        else:
            E = DDP(Encoder(pretrained=resume_pkl,w_avg=latent_avg).to(device), device_ids=[rank])
    elif model_architecture == 'transformer':
        styleblock = dict(arch='transformer', num_encoder_layers=num_encoder_layers)
        if resume_pkl is None:
            E = DDP(Encoder(pretrained=None, w_avg=latent_avg, **styleblock).to(device), device_ids=[rank])
        else:
            E = DDP(Encoder(pretrained=resume_pkl, w_avg=latent_avg, **styleblock).to(device), device_ids=[rank])
    cur_step = E.module.resume_step

    # Initizlize loss
    if rank == 0:
        print('Initialize loss...')
    moco_loss = MocoLoss().to(device).eval()
    lpips_loss = LPIPS(net='alex', verbose=False).to(device).eval()

    # Initialize optimizer
    if rank == 0: 
        print('Initialize optimizer...')
    params = list(E.parameters())
    optimizer = Ranger(params, lr=learning_rate)
    optimizer_d = torch.optim.Adam(E.parameters(),lr=learning_rate)

    # Initialize logs.
    if rank == 0:
        print('Initialize tensorboard logs...')
        logger = tensorboard.SummaryWriter(run_dir)

    # Train.
    E.train()
    G.eval()
    if d_lambda >0:
      D.eval()
    start_time = time.time()
    #TODO : implement validation
    while cur_step < training_steps:
        for batch_idx, batch in enumerate(training_loader): 
            optimizer.zero_grad()
            # x:source image = y:real image
            # E(x): w, encoded latent
            # G.synthesis(E(x)):encoded_images
            x,y = batch 
            x,real_images = x.to(device),y.to(device)
            face_pool=torch.nn.AdaptiveAvgPool2d((256,256))
            encoded_images = face_pool(G.synthesis(E(x)))
            # get loss
            loss = 0.0
            loss_dict = {} # for tb logs
            
            loss_l2 = l2_loss(encoded_images, real_images)
            loss_dict['l2'] = loss_l2.item()
            loss += loss_l2 * l2_lambda

            loss_lpips = lpips_loss(encoded_images, real_images).squeeze().mean()
            loss_dict['lpips'] = loss_lpips.item()
            loss += loss_lpips * lpips_lambda

            loss_moco, sim_improvement,_ = moco_loss(encoded_images, real_images, x)
            loss_dict['moco'] = loss_moco.item()
            loss_dict['moco_improve'] = float(sim_improvement)
            loss += loss_moco * moco_lambda



            # back propagation
            loss.backward()
            # optimizer step
            optimizer.step()
            
            if d_lambda >0:
              optimizer_d.zero_grad()
              encoded_images = G.synthesis(E(x))
              gen_logits = D(encoded_images,None)
              loss_D = torch.nn.functional.softplus(-gen_logits).squeeze().mean()
              loss_dict['D'] = loss_D.item()
              loss_D = loss_D * d_lambda
              loss_D.backward()
              optimizer_d.step()
            loss_dict['loss'] = loss.item()

            if rank == 0 and cur_step % print_steps == 0:
                loss_dict['time']=time.time()-start_time
                print(f'\nCurrent batch step: {cur_step}')
                pprint(loss_dict)
                start_time=time.time()

            # barrier
            torch.distributed.barrier()

            # Save image snapshot.
            if rank == 0 and cur_step % image_snapshot_steps == 0:
                print(f"Saving image snapshot at step {cur_step}...")
                gh, gw = 1, batch_gpu
                H,W = real_images.shape[2], real_images.shape[3]
                real_path = f'image-snapshot-real-{cur_step:06d}.png'
                encoded_path = f'image-snapshot-encoded-{cur_step:06d}.png'
                save_image(real_images, os.path.join(run_dir, 'image_snapshots', real_path), gh, gw, H, W)
                save_image(encoded_images, os.path.join(run_dir, 'image_snapshots', encoded_path), gh, gw, H, W)

            # Save network snapshot.
            snapshot_pkl = None
            snapshot_data = None
            if rank == 0 and cur_step % network_snapshot_steps == 0:
                print(f"Saving netowrk snapshot at step {cur_step}...")
                # TODO: save lr scheduler, optimizer status, etc...
                snapshot_data = dict(
                    E=E.state_dict(),
                    step=cur_step,
                )
                snapshot_pkl = os.path.join(run_dir, 'network_snapshots',f'network-snapshot-{cur_step:06d}.pkl')
                with open(snapshot_pkl, 'wb') as f:
                    pickle.dump(snapshot_data, f)
            del snapshot_data # conserve memory

            # Tensorboard logs.
            if rank == 0 and cur_step % tensorboard_steps == 0:
                for key in loss_dict:
                    logger.add_scalar(f'train/{key}', loss_dict[key], cur_step)
            # barrier
            torch.distributed.barrier()

            # update cur_step
            cur_step += 1
            if cur_step == training_steps:
                break

    # Done.
    torch.distributed.destroy_process_group()

    if rank == 0:
        print()
        print('Exiting...')
