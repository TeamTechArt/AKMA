# AKMA (Audio Kinetic Media Art) Project Overview

AIFFEL X SeSAC Hackathon Project

## Table of Contents

- [Overview](#Overview)
  - [Team-Introduction](#Team-Introduction)
  - [AKMA-Introduction](#AKMA-Introduction)
  - [Factors-in-AKMA](#Factors-in-AKMA)
  - [AKMA-Walkthrough](#AKMA-Walkthrough)
  - [Project-Timeline](#Project-Timeline)
- [Workflow](#Workflow)
  - [Data-Acquisition](#Data-Acquisition)
  - [Architecture](#Architecture)
  - [Model](#Model)
- [Tech-Stack](#Tech-Stack)
- [Sample](#Sample)
- [Reference](#Reference)

## Overview

2022.01.17 ~ 2022.03.10 약 2 달간 진행한 AKMA (Audio Kinetic Media Art) 프로젝트의 Overview와 각 리포지토리 설명, 노션의 다큐멘테이션을 정리해보았습니다.

**모두의연구소 AIFFEL** 에서 개인 과제 **_StyleGAN3 Based Audio Reactive Media Art Generator Model_**를 주제로 프로젝트를 진행하였습니다.

## Team-Introduction

| Name | Role | Email | Focus |
|:-------------:|:-------------:|:-------------:|:-------------:|
| [최동현](https://github.com/donghyundavidchoi) | 팀장 | david0302@naver.com | ? |
| [김영현](https://github.com/kim1987) | 팀원 | overevo489@gmail.com | ? |
| [윤세영](https://github.com/uni1023) | 팀원 | yoonsy1023@gmail.com | ? |
| [이상현](https://github.com/oddhyeon) | 팀원 | roughideal@gmail.com | ? |
| [이호진](https://github.com/ghwlsdl) | 팀원 | hojinlee93@gmail.com | ? |

## AKMA-Introduction

Audio Kinetic Media Art, shortly AKMA, which pronounces the same as the devil in Korean, is the media art generation solution based on StlyeGAN3 that produces a media art reacting actively to the volume of input audio.

## Factors-in-AKMA

Users can adjust the following factors to produce target media art.

	- Input Audio : Must be wav file (24bit wav file is not acceptable)
	- Input Network_pkl : StyleGAN3 model containing contents that the user wants for media art
  	- Fps : frame per second of the result
	- window length : It mainly adjust the flatness of the waveform of input audio, affect how sensitively the media art reacts to the volume of the input audio. Must be an odd number.
 	- Polyorder : The order of the polynomial used to fit the samples. Must be smaller than window length. 
  	- Compression : The larger you give a number, the more it compresses the waveform of the input audio exponentially, reducing the variance of the waveform, making the result less reactive to the input audio. The default value is 1. Must be larger than 0. Recommend Value between 0.5 and 2.
  	- seeds_top_num : number of seeds corresponds to the largest volume of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Must be larger than 4.
  	- seeds_bottom_num : number of seeds corresponds to the 0 volume of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Must be larger than 4.

## AKMA-Walkthrough


	1. Input audio file. It must be wav file. 24bit wav file is not acceptable.


	2. Adjust fps, window length, polyorder, compression. You can check the waveform image which will be the guidance for audio reactive function. Adjust those factors until you get a desirable waveform for your media art.


	3. Input StyleGAN3 network pkl file.


	4. Adjust the number of seeds for the top and bottom of the waveform. The more you give the number, the model produces more images in the same duration, making the speed of the video faster. Usually, I recommend you to give more numbers for the top, so the video gets more active when the volume gets larger.


	5. Start generation and wait till the process ends.


## [Project-Timeline](https://github.com/TeamTechArt/AKMA/blob/main/Readme_Project-Timeline.md)


## Workflow


### Data-Acquisition

- 공사 중 입니다.


## Model Architecture


### StyleGAN3
![styelgan3](https://user-images.githubusercontent.com/67223441/157396919-04b48c92-6787-4610-aacb-6794c6bb4f12.png)


### Real-ESRGAN
![Real-ESRGAN](https://user-images.githubusercontent.com/67223441/157398801-5922a4d4-c06e-4946-adf2-fbad0ff95245.png)


## Tech Art Team Piple Line


## 초기 Pipline


![Tech Art 초기 Pipline drawio](https://user-images.githubusercontent.com/90362869/150274518-22b3e367-765b-43f4-94b8-c5dd6a85e6a6.png)


## 중간발표 시기 Pipline


![Tech Art 중간발표 시기 Pipline drawio](https://user-images.githubusercontent.com/90362869/154292356-cf968c4f-e0f4-47e1-a8ec-0fd06088c636.jpeg)


## Tech-Stack


- Model
  - PyTorch
  - [Stylegan3](https://github.com/NVlabs/stylegan3)
  - [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
- Custom Data
  - [YOUTUBE-WAVE](https://drive.google.com/drive/folders/1197NN3gqxi2mEQ5do1Lmp4UQIq-SfO9L)
  - [EAST-SEA](https://drive.google.com/file/d/1SscfF-3Zy9_IPvU6DsBXvmT_isvcoWe4/view?usp=sharing)
- Serving
  - [BentoML](https://github.com/TeamTechArt/AKMA/tree/main/BentoML)
  - [Google Cloud Platform](https://cloud.google.com/gcp/?utm_source=google&utm_medium=cpc&utm_campaign=japac-KR-all-en-dr-bkws-all-all-trial-e-dr-1009882&utm_content=text-ad-none-none-DEV_c-CRE_514666343206-ADGP_Hybrid+%7C+BKWS+-+EXA+%7C+Txt+~+GCP+~+General_+Core+Brand-KWID_43700060620875343-aud-970366092687:kwd-26415313501-userloc_1009871&utm_term=KW_google%20cloud%20platform-ST_google+cloud+platform&gclid=CjwKCAiAvaGRBhBlEiwAiY-yMAduyI7HaEG-UsISeqSyI5c90KsorWSA22E2QyR1DATrsZh9PadL1BoCaJoQAvD_BwE&gclsrc=aw.ds)


## Sample
 - [landscape-paradox](https://drive.google.com/file/d/1dX7UPuy-rlaeYYTrlXPJFFV4FssCj7-N/view?usp=sharing)
 - [wikiart-paradox](https://drive.google.com/file/d/1fGUIIfBadJuCWPwkMxHawxT8wfl1iNUJ/view?usp=sharing)
 - [EAST-SEA](https://drive.google.com/file/d/1ncnCM0SLFSmsjungRs4aEvL8tv0x_uZU/view?usp=sharing)


## Reference
- [Stylegan3](https://github.com/NVlabs/stylegan3)
- [StyleGAN2 Reactive Audio](https://github.com/dvschultz/ai/blob/master/StyleGAN2_AudioReactive.ipynb)
- [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN)
