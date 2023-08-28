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
7. 可配置本地安装的lora/loha/embedding，实现简单输入即可生成提示词
8. 可输入额外提示词
9. 可精细手动输入，精细控制人物，视角等。
10. 可将生成内容一键发送到文生图

## Lora/Loha/embedding控制说明

### 配置修改
该功能可实现输入个人自定义的文字来生成本地Lora/Loha/embedding提示词。
安装本extension成功后，可以在extensions/prompt-r-gen-sd/scripts 文件中找到`modelsConfig.xlsx`，打开该excel，直接进行编辑。
参照下面的图示添加你本地的lora等模型配置：
<img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/model_guide.png" alt="guide" width="50%">

### 使用说明
<img src="https://github.com/HeathWang/prompt-r-gen-sd/blob/master/ui_lora.png" alt="lora" width="50%">
点开“Lora Loha embedding控制”下拉菜单，以本地下载的`st louis epoch5.safetensors`为例，
在lora框输入：
1. "圣姨"，则表示“lora模型按照指定权重随机”
2. "圣姨:0.6"，则说明"lora模型固定0.6权重"

对于使用多个模型，中间以“,”分割即可
如：
1. "圣姨,666:0.8,xyz"，则表示"生成这3个配置lora的提示词"

### Lora/Loha/embedding输出顺序
默认情况下，按照Lora/Loha/embedding顺序输出，你可以在顺序更改输入框更改它们的输出顺序。
1. xyz：Lora/Loha/embedding
2. yxz：Loha/Lora/embedding
3. zxy：embedding/Lora/loha
......



## 后续功能

1. ~~添加精细控制模块，可自定义输入覆盖随机配置 [DONE]~~
2. 存储默认配置项，下次启动自动载入
3. 可查看历史生成记录📝。


