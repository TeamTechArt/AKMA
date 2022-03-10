# StyleGAN Encoder

## Encoder Train
Input 이미지를 통해 타겟 이미지를 생성하도록 w를 생성하는 네트워크를 학습합니다.

## pixel2style2piel : psp

StyleGAN2를 기반으로 encoder-synthesis 구조의 모델을 생성하여 encoder 또는 encoder-synthesis를 학습하여 StyleGAN-encoder, Face Frontalization, Super Resolution 등을 수행합니다.

## StyleGAN3-Encoder
psp 에서 사용하는 encoder를 기반으로 StyleGAN3에서 이용할 수 있도록 수정하였습니다.

## id loss vs moco loss

### id loss 활용
<img width="960" alt="image" src="https://user-images.githubusercontent.com/90362869/157570565-b61f5cf5-dcca-4d51-b8f8-3ff61288ecaa.png">

### id loss 를 moco loss 로 변경
<img width="960" alt="image" src="https://user-images.githubusercontent.com/90362869/157570602-fc737610-876d-4ecc-9abd-7909597969d2.png">

## StyleGAN3 Decoder loss

### 실제 이미지
<img width="512" alt="image" src="https://user-images.githubusercontent.com/90362869/157570691-0087a415-d88d-44a3-8326-18566743997f.png">

### 기존의 StyleGAN3 Encoder + StyleGAN3 Decoder loss 추가
<img width="512" alt="image" src="https://user-images.githubusercontent.com/90362869/157570759-28b36362-1a8c-4c01-8169-2a05a91986d4.png">

## Discriminator with R1 for Encoder

### Only StlyeGAN2 Encoder

<img width="512" alt="image" src="https://user-images.githubusercontent.com/90362869/157570900-38d4dd46-8a24-4e87-aadd-45dadec598ac.png">

### StyleGAN3 Encoder + Discriminator with R1 for Encoder

<img width="512" alt="image" src="https://user-images.githubusercontent.com/90362869/157570924-abd508fc-799d-40a2-b64b-033e9a7c47e2.png">

[Encoder_Result](https://drive.google.com/drive/folders/1m0VS5NTGoCdypPNh6mz9sIBcaoaSpS4K)

If you want to see the results created by the encoder, you can click the link.
