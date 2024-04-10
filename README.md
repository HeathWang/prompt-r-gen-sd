---
title: prompt-r-gen-sd
app_file: scripts/prompt_rg.py
sdk: gradio
sdk_version: 3.40.1
---
# prompt-r-gen-sd

## Introduction 
This is a [stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) plug-in (extension), which is mainly used to generate random text prompt words. The original intention of doing this is that I am too lazy to write prompt words, but I also want the prompt words to be generated with one click and have a certain degree of randomness, so I have this plug-in.

 ~~Currently, only prompt words for drawing girls are supported~~, others are to be developed.
 
Feature preview：[https://huggingface.co/spaces/heath1989/prompt-rp](https://huggingface.co/spaces/heath1989/prompt-r-gen-sd)

## Function

<img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/snap_Shot.png" alt="ui" width="100%">

1. The number of prompt words generated at one time can be configured, with a minimum of 1 and a maximum of 6
2. Can randomize perspective, location, character actions
3. Can randomize character clothing: clothes, shoes, socks, underwear, etc.
4. Can randomize character description: occupation, hairstyle, hair color, eyes, eye color, facial expression (no negative expressions) )
5. NSFW can be configured,~~try it yourself~~
6. Other enhancements can be configured: whether it is a real photo, colorful, weather, lighting effects, photography technology, items, accessories, etc.
7. Locally installed lora/loha/embedding can be configured to generate prompt words by simple input
8. Additional prompt words can be input
9. Fine manual input is possible, and characters, perspective, etc. can be precisely controlled.
10. The generated content can be sent to Wenshengtu with one click

## Lora/Loha/eembedding control instructions

### Configuring and modifying this function allows you to enter personal customized text to generate local Lora/Loha/embedding prompt words.
 After successfully installing this extension, you can find `modelsConfig.xlsx` in the extensions/prompt-r-gen-sd/scripts file, open the excel, and edit it directly.

You can also download it at the following address: https://huggingface.co/spaces/heath1989/prompt-rp/resolve/main/modelsConfig.xlsx

Refer to the diagram below to add your local lora and other model configurations:

<img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/model_guide.png" alt="guide" width="100%">
After the excel modification is saved, the configuration can take effect in real time. For cloud deployment, the cloud needs to cover `modelsConfig.xlsx` to take effect.

### Instructions for use <img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/ui_lora.png" alt="lora" width="100%">

 Click on the "Lora Loha embedding control" drop-down menu, taking the locally downloaded `st louis epoch5.safetensors` as an example,

 Enter in the lora box:

1. "Shengyi" means "the lora model is random according to the specified weight"
 2. "Saint Aunt: 0.6" means "the lora model has a fixed weight of 0.6"

 For using multiple models, separate them with "," as follows:
 1. "Shengyi,666:0.8,xyz" means "generate these three prompt words for configuring lora"

### Lora/Loha/embedding
Lora/Loha/embedding output order By default, output is in the order of Lora/Loha/embedding. You can change their output order in the order change input box.
1. xyz：Lora/Loha/embedding
2. yxz：Loha/Lora/embedding
3. zxy：embedding/Lora/loha

......

## Follow-up functions

1. ~~Add fine control module, customizable input overrides random configuration [DONE]~~
 2. Store the default configuration items and load them automatically next time.
 3. You can view the historical generation records📝.


