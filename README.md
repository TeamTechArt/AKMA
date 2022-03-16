# AKMA : Audio Kinetic Media Art

AIFFEL X SeSAC Hackathon Project

## Table of Contents


- [Team-Introduction](#Team-Introduction)
- [Team-Member](#Team-Member)
- [AKMA-Introduction](#AKMA-Introduction)
- [Factors-in-AKMA](#Factors-in-AKMA)
- [AKMA-Walkthrough](#AKMA-Walkthrough)
- [Changes-from-the-reference](#Changes-from-the-reference)
- [Project-Timeline](#Project-Timeline)
- [Custom-Model](#Custom-Model)
  - [East-Sea](#East-Sea)
- [Tech-Stack](#Tech-Stack)
- [Sample-Result](#Sample-Result)
- [Reference](#Reference)


## Team-Introduction


Audio Kinetic Media Art, shortly AKMA, which pronounces the same as the devil in Korean, is the media art generation solution based on StlyeGAN3 that produces a media art reacting actively to the volume of input audio.


## Team-Member


| Name | Position | Email | Role |
|:-------------:|:-------------:|:-------------:|:-------------:|
| [최동현](https://github.com/donghyundavidchoi) | Project Manager | david0302@naver.com | Project Management, Model Framework Development, ML Research, Model Optimization, Model Automation, Data Acquisition |
| [이상현](https://github.com/oddhyeon) | Technology Manager | roughideal@gmail.com | ML Research, Server Engineering, Model Version Management, StyleGAN3 Model Training, Model Automation |
| [김영현](https://github.com/kim1987) | Team Member | overevo489@gmail.com | ML Research, StyleGAN Encoder Training, Model Serving, Tech Adamin, Modifying the model code, Model Automation |
| [이호진](https://github.com/ghwlsdl) | Team Member | hojinlee93@gmail.com | ML Research, Model QA, Documentation | 
| [윤세영](https://github.com/uni1023) | Team Member | yoonsy1023@gmail.com | Data Acquisition |


## AKMA-Introduction


Audio Kinetic Media Art, shortly AKMA, which pronounces the same as the devil in Korean, is the media art generation solution based on StlyeGAN3 that produces a media art reacting actively to the volume of input audio.


## Factors-in-AKMA


Users can adjust following factors to produce target media art.

	- Input Audio : Must be wav file (24bit wav file is not acceptable)
	- Input Network_pkl : StyleGAN3 model containing contents that the user wants for media art
  	- fps : frame per second of the result
	- window length : It mainly adjust the flatness of the waveform of input audio, affect how sensitively the media art reacts to the volume of the input audio. Must be an odd number.
 	- polyorder : The order of the polynomial used to fit the samples. Must be smaller than window length. 
  	- compression : The larger you give a number, the more it compresses the waveform of the input audio exponentially, reducing the variance of the waveform, making the result less reactive to the input audio. The default value is 1. Must be larger than 0. Recommend Value between 0.5 and 2.
  	- seeds_top_num : Number of seeds corresponds to the largest volume of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Must be larger than 4.
  	- seeds_bottom_num : Number of seeds corresponds to the 0 volume of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Must be larger than 4.


## AKMA-Walkthrough


![AKMA Pipeline](https://user-images.githubusercontent.com/90362869/157410524-5e9c5cfb-0810-4b55-9344-b3b972664b1f.png)


	1. Input audio file. It must be wav file. 24bit wav file is not acceptable.


	2. Adjust fps, window length, polyorder, compression. You can check the waveform image which will be the guidance for audio reactive function. Adjust those factors until you get a desirable waveform for your media art.


	3. Input StyleGAN3 network pkl file.


	4. Adjust the number of seeds for the top and bottom of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Usually, I recommend you to give more numbers for the top, so the video gets more active when the volume gets larger.


	5. Start generation and wait till the process ends.


## Changes-from-the-reference


### Changes from StlyeGAN2 audio reactive

	StyleGAN3 applied.  

	More adjustment functions have been provided for waveform, the guidance for audio reactive function.

	Interpolate two videos by the waveform, not only two images.  

	Able to adjust video speed by adding more seeds.  


### Why StlyeGAN3?

	By achieving Alias-Free using signal processing theory, it solved texture-sticking problem of StyleGAN2, producing higher quality images.  

	This shows significantly better video generation.  


### Changes from Real-ESRGAN-Video-Batch-Process

	The reference does not keep the original audio file. Now it keeps the original audio file and merges it to enhanced video.


### Why Real-ESRGAN?

	By using sinc filter, Real-ESRGAN reduces ringing and overshooting, improving image quality.


## [Project-Timeline](https://github.com/TeamTechArt/AKMA/blob/main/Readme_Project-Timeline.md)

If you are curious about the project timeline, please click the link above.


## Custom-Model


### [East-Sea](https://drive.google.com/file/d/1SscfF-3Zy9_IPvU6DsBXvmT_isvcoWe4/view)

<img width="1079" alt="East-Sea Data" src="https://user-images.githubusercontent.com/90362869/157467318-74311ade-d022-4067-8272-a04fa42ba303.png">


- The model trained with image data from the East Sea.


## Tech-Stack


- Model
  - [PyTorch](https://pytorch.org/)
  - [Stylegan3](https://github.com/NVlabs/stylegan3)
  - [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)


- Custom Data
  - [YOUTUBE-WAVE](https://drive.google.com/drive/folders/1197NN3gqxi2mEQ5do1Lmp4UQIq-SfO9L)
  - [EAST-SEA](https://drive.google.com/file/d/1SscfF-3Zy9_IPvU6DsBXvmT_isvcoWe4/view?usp=sharing)


- Serving
  - [BentoML](https://github.com/TeamTechArt/AKMA/tree/main/BentoML)
  - [Google Cloud Platform](https://cloud.google.com/gcp/?utm_source=google&utm_medium=cpc&utm_campaign=japac-KR-all-en-dr-bkws-all-all-trial-e-dr-1009882&utm_content=text-ad-none-none-DEV_c-CRE_514666343206-ADGP_Hybrid+%7C+BKWS+-+EXA+%7C+Txt+~+GCP+~+General_+Core+Brand-KWID_43700060620875343-aud-970366092687:kwd-26415313501-userloc_1009871&utm_term=KW_google%20cloud%20platform-ST_google+cloud+platform&gclid=CjwKCAiAvaGRBhBlEiwAiY-yMAduyI7HaEG-UsISeqSyI5c90KsorWSA22E2QyR1DATrsZh9PadL1BoCaJoQAvD_BwE&gclsrc=aw.ds)


## Sample-Result
 - [Landscape-paradox](https://drive.google.com/file/d/1dX7UPuy-rlaeYYTrlXPJFFV4FssCj7-N/view?usp=sharing)
 - [Wikiart-paradox](https://drive.google.com/file/d/1fGUIIfBadJuCWPwkMxHawxT8wfl1iNUJ/view?usp=sharing)
 - [EAST-SEA](https://drive.google.com/file/d/1ncnCM0SLFSmsjungRs4aEvL8tv0x_uZU/view?usp=sharing)


## Reference
- [Stylegan3](https://github.com/NVlabs/stylegan3)
- [StyleGAN2 Reactive Audio](https://github.com/dvschultz/ai/blob/master/StyleGAN2_AudioReactive.ipynb)
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
- [Real-ESRGAN-Video-Batch-Process](https://github.com/GeeveGeorge/Real-ESRGAN-Video-Batch-Process/tree/main)
