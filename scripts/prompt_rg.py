import gradio as gr
from module.sd_nsfw_random import project_config as gen_config
from module.web_api import (create_prompts)

project_config = gen_config
times = 2


def base_update(type_key, the_value):
  project_config[f"{type_key}"] = the_value
  return project_config

def update_gen_times(com_value):
  global times
  times = com_value
def update_angle(com_value):
  if com_value:
    project_config["angle"] = ""
  else:
    project_config["angle"] = "null"
  return project_config

def update_body_framing(com_value):
  if com_value:
    project_config["body_framing"] = ""
  else:
    project_config["body_framing"] = "null"
  return project_config

def update_place(com_value):
  if com_value:
    project_config["place"] = ""
  else:
    project_config["place"] = "null"
  return project_config

def update_pose_type(com_value):
  if com_value == "全身":
    project_config["pose_type"] = 2
  else:
    project_config["pose_type"] = 1
  return project_config

def update_dynamic_mode(com_value):
  return base_update("dynamic_mode", com_value) 

def update_breasts(com_value):
  if com_value == "空NULL":
    project_config["breasts_size"] = "null"
  else:
    project_config["breasts_size"] = com_value
  return project_config


def update_body_wear(com_value):
  return base_update("body_wear", com_value + 1)


def update_top_wear(com_value):
  return base_update("top_wear", com_value + 1)

def update_bottom_wear(com_value):
  return base_update("bottom_wear", com_value + 1)

def update_leg_wear(com_value):
  return base_update("leg_wear", com_value + 1)

def update_panties(com_value):
  return base_update("panties", com_value)

def update_shoes(com_value):
  return base_update("shoes_type", com_value + 1)

def update_body_with(com_value):
  return base_update("body_with", com_value)

def update_body_status(com_value):
  return base_update("body_status", com_value)


def update_body_desc(com_value):
  return base_update("body_description", com_value)

def update_clothes_trim(com_value):
  return base_update("cloth_trim", com_value)

def update_person_job(com_value):
  if com_value:
    return base_update("assign_profession", "")
  else:
    return base_update("assign_profession", "null")

def update_hair_color(com_value):
  if com_value == 0:
    return base_update("hair_color", "random")
  elif com_value == 1:
    return base_update("hair_color", "null")

def update_hair_stlye(com_value):
  return base_update("add_hair_style", com_value)

def update_eye_color(com_value):
  return base_update("enable_eye_color", com_value)

def update_girl_desc(com_value):
  return base_update("has_girl_desc", com_value)

def update_gril_beautiful(com_value):
  return base_update("add_girl_beautyful", com_value)

def update_face_express(com_value):
  print(com_value)
  if com_value <= 4:
    base_update("face_expression", com_value + 1)
  else:
    base_update("face_expression", 1)
    base_update("assign_expression", "null")

######### gen #########

def gen_action():
  return create_prompts(times, project_config)

######### UI #########
with gr.Blocks() as demo:
    gr.Markdown("根据下面配置随机生成prompt")

    time_slider = gr.Slider(1, 6, value=4, label="随机生成条数", step=1, interactive=True)
    time_slider.change(update_gen_times, inputs=time_slider)

    with gr.Box():
      gr.Markdown("视角、地点、动作")
      with gr.Row():
        angle = gr.Checkbox(False, label="视角", info="正面，侧面，背面...")
        angle.change(update_angle, inputs=[angle], )
        body_framing = gr.Checkbox(False, label="身体框架", info="肖像，半身，全身...")
        body_framing.change(update_body_framing, inputs=body_framing, )
        location = gr.Checkbox(False, label="地点", info="随机地点")
        location.change(update_place, inputs=location, )
        pose_type = gr.Radio(['全身', '基础'], value='基础', label="动作类型", interactive=True, info="任务动作，站、坐、躺...")
        pose_type.change(update_pose_type, inputs=pose_type, )
        dynamic_mode = gr.Checkbox(False, label="动态模式", info="使用dynamic pose, angle")
        dynamic_mode.change(update_dynamic_mode, inputs=dynamic_mode, )
    with gr.Box():
      gr.Markdown("身体穿着描述, 选择空NULL则不生成该tag")
      with gr.Column():
        with gr.Row():
          breasts_size = gr.Dropdown(["medium", "large", "huge", "gigantic", "空NULL"], value="large", label="胸大小描述", info="", interactive=True)
          breasts_size.change(update_breasts, inputs=breasts_size, )
          body_wear = gr.Dropdown(["裙子dress", "制服UNIFORM", "紧身衣BODYSUIT", "传统服饰TRADITIONAL", "上下搭配(如上身体恤下身短裙)", "以上随机", "空NULL"], value="裙子dress",type="index", label="衣服", info="", interactive=True)
          body_wear.change(update_body_wear, inputs=body_wear, )
          top_wear = gr.Dropdown(["衬衫SHIRTS", "外套COAT", "毛衣SWEATER", "其他OTHERS", "以上随机RANDOM"], value="衬衫SHIRTS", type="index", label="上身衣物", info="选择上下搭配(如上身体恤下身短裙)该配置生效", interactive=True)
          top_wear.change(update_top_wear, inputs=top_wear, )
          bottom_wear = gr.Dropdown(["裤子PANTS", "短裙SKIRT", "短裤SHORTS", "以上随机RANDOM"], value="短裙SKIRT", type="index", label="下身衣物", info="选择上下搭配(如上身体恤下身短裙)该配置生效", interactive=True)
          bottom_wear.change(update_bottom_wear, inputs=bottom_wear, )
        with gr.Row():
          leg_wear = gr.Dropdown(["短袜SOCKS", "小腿袜KNEEHIGHS", "过膝袜OVERKNEEHIGHS", "大腿袜THIGHHIGHS", "连裤袜PANTYHOSE", "光腿BARE", "空NULL", "以上随机RANDOM"], value="空NULL", type="index", label="袜子", interactive=True)
          leg_wear.change(update_leg_wear, inputs=leg_wear, )
          panties = gr.Checkbox(False, label="内裤", info="勾选则随机给生成一种内裤类型")
          panties.change(update_panties, inputs=panties, )
          shoes_type = gr.Dropdown(["靴子BOOTS", "高跟鞋HIGHHEELS", "凉鞋SANDALS", "拖鞋SLIPPERS", "光脚BARE", "空NULL"], value="空NULL", type="index", label="鞋子", info="", interactive=True)
          shoes_type.change(update_shoes, inputs=shoes_type, )
        with gr.Row():
          body_with = gr.Checkbox(False, label="身体缠绕物", info="缠绕一些东西，束缚，丝带，链条")
          body_with.change(update_body_with, inputs=body_with, )
          body_status = gr.Checkbox(False, label="身体状态", info="湿身、出汗...")
          body_status.change(update_body_status, inputs=body_status, )
          body_desc = gr.Checkbox(False, label="身体描述", info="完美身材，纤细身体...")
          body_desc.change(update_body_desc, inputs=body_desc, )
          cloth_trim = gr.Checkbox(False, label="衣服装饰", info="蕾丝，丝带，金色，花等等...")
          cloth_trim.change(update_clothes_trim, inputs=cloth_trim, )
    with gr.Box():
      gr.Markdown("人物描述")
      with gr.Row():
        profession = gr.Checkbox(False, label="职业", info="随机职业，学生，护士...")
        profession.change(update_person_job, inputs=profession, )
        hair_color = gr.Dropdown(["随机RANDOM", "空NULL"], value="随机RANDOM", type="index", label="头发颜色", info="", interactive=True)
        hair_color.change(update_hair_color, inputs=hair_color, )
        add_hair_style = gr.Checkbox(False, label="头发风格", info="发型")
        add_hair_style.change(update_hair_stlye, inputs=add_hair_style, )
        enable_eye_color = gr.Checkbox(True, label="眼睛颜色", info="")
        enable_eye_color.change(update_eye_color, inputs=enable_eye_color, )
      with gr.Row():
        face_expression = gr.Dropdown(["情绪EMOTIONS", "诱惑SEXUAL", "笑SMILE", "俏皮SMUG", "以上随机", "空NULL"], value="笑SMILE", type="index", label="表情", interactive=True)
        face_expression.change(update_face_express, inputs=face_expression)
        add_girl_beautyful = gr.Checkbox(False, label="描述妹子的短词缀", info="")
        add_girl_beautyful.change(update_gril_beautiful, inputs=add_girl_beautyful, )
        has_girl_desc = gr.Checkbox(False, label="描述妹子的长词缀", info="")
        has_girl_desc.change(update_girl_desc, inputs=has_girl_desc, )
    with gr.Box():
      gr.Markdown("NSFW")
      with gr.Row():
        nsfw_type = gr.Dropdown(["裸NUDE", "性感SEXUAL", "常规NOTNSFW"], value="常规NOTNSFW", label="NSFW等级", info="请确保你知道自己在干嘛！选择非常规类型，上面的人物衣服设置不生效", interactive=True)
        is_nsfw = gr.Checkbox(False, label="是否添加nfsw词缀")
        is_uncensored = gr.Checkbox(False, label="是否添加uncensored词缀")
        is_simple_nude = gr.Checkbox(False, label="是否是简单的nude模式")
        nude_strong = gr.Checkbox(False, label="是否加强nude模式")
      with gr.Row():
        sexual_list_random_index_times = gr.Slider(0, 5, value=0, step=1, label="性感词缀随机数", interactive=True)
        nude_list_random_index_times = gr.Slider(0, 9, value=0, step=1, label="裸体词缀随机数", interactive=True)
    with gr.Box():
      gr.Markdown("其他")
      with gr.Row():
        has_starting = gr.Checkbox(False, label="是否使用起手式")
        is_realistic = gr.Checkbox(False, label="是否添加真实词缀")
        add_colors = gr.Checkbox(False, label="是否添加多彩词缀")
        enable_day_weather = gr.Checkbox(False, label="是否添加天气信息")
        enable_light_effect = gr.Checkbox(True, label="是否添加灯光效果")
        enable_image_tech = gr.Checkbox(False, label="是否开启图像技术，如模糊")
      with gr.Row():
        accessories_random_tims = gr.Slider(0, 8, value=0, step=1, label="饰物随机数", interactive=True)
        object_random_times = gr.Slider(0, 8, value=0, step=1, label="物品随机数", info="花，元素等", interactive=True)
        suffix_words_random_times = gr.Slider(0, 10, value=0, step=1, label="形容词缀随机数", info="", interactive=True)
    with gr.Box():
      gr.Markdown("lora,embedding配置")
      with gr.Row():
        lora = gr.Textbox("", label="Lora【x】", info="格式如下：100, '100:0.6', '100:0.6'\n输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'100:0.8'，则表示lora权重0.8")
        lyco = gr.Textbox("", label="lyco【y】", info="格式如下：100, '100:0.6', '100:0.6'\n输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'100:0.8'，则表示lora权重0.8")
      with gr.Row():
        embeddings = gr.Textbox("", label="embeddings【z】", info="格式如下：100, '100:0.6', '100:0.6'\n输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'100:0.8'，则表示lora权重0.8")
        model_order = gr.Textbox("", label="lora，lyco，embed顺序", info="xyz顺序")
    with gr.Box():
      gr.Markdown("手动输入项")
      with gr.Row():
        additional_prompt = gr.Textbox("", label="额外的prompt")

    results = gr.Textbox("", label="生成的prompt")
    gen_button = gr.Button("生成prompt")

    gen_button.click(gen_action, outputs=results)

demo.launch(debug=True)