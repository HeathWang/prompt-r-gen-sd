# prompt-r-gen-sd

## 介绍
这是一个[stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) 插件(extension)，主要用来生成随机的文生图提示词。
做这个的初衷是自己懒得写提示词，但是又想提示词可以一键生成且具有一定的随机性，所以有了这个插件。

~~目前仅支持画女孩提示词~~，其他待开发。

功能预览：https://huggingface.co/spaces/heath1989/prompt-rp

## 功能

<img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/snap_Shot.png" alt="ui" width="50%">

1. 可配置一次生成的提示词数量，最小1，最大6
2. 可随机视角、地点、人物动作
3. 可随机人物衣着：衣服，鞋子，袜子，内裤等
4. 可随机人物描述：职业，发型，发色，眼睛，眼睛颜色，面部表情(无负面表情)
5. 可配置NSFW，~~自行尝试~~
6. 可配置其他增强项：是否是真实照片，多彩，天气，灯光效果，摄影技术, 物品，饰品等
7. 可通过单纯输入数字生成lora，loha， embedding，可配置权重
8. 可输入额外提示词
9. 可精细手动输入，精细控制人物，视角等。
10. 可将生成内容一键发送到文生图

## Lora Loha embedding控制说明
待完善，大致使用：
1. 101   随机权重
2. 101:0.6 指定权重0.6
3. 101,202:0.6,401   指定多个lora

## 后续功能

1. ~~添加精细控制模块，可自定义输入覆盖随机配置 [DONE]~~
2. 存储默认配置项，下次启动自动载入
3. 可查看历史生成记录📝。


