import modules.scripts as scripts
from modules import script_callbacks

import gradio as gr

from scripts.module.sd_command_gen import project_config as gen_config
from scripts.module.web_api import (create_prompts)

project_config = gen_config
t2i_text_box = None


def base_update(type_key, the_value):
    project_config[f"{type_key}"] = the_value
    return project_config


def get_model_input(com_value):
    arr = com_value.split(",")
    target_list = []
    if len(arr) > 0:
        target_list = [x.strip() for x in arr if x.strip()]
    return target_list


######### gen #########
# 我有史以来写的最长的方法
def gen_action(gen_times, lora, lyco, embeddings, model_order, additional_prompt, angle, body_framing, location,
               pose_type,
               dynamic_mode, breasts_size, body_wear, top_wear, bottom_wear, leg_wear, panties, shoes_type, body_with,
               body_status, body_desc, cloth_trim, profession, hair_color, add_hair_style, enable_eye_color,
               face_expression, add_girl_beautyful, has_girl_desc, nsfw_type, is_nsfw, is_uncensored, is_simple_nude,
               nude_strong, sexual_list_random_index_times, nude_list_random_index_times, has_starting, is_realistic,
               add_colors, enable_day_weather, enable_light_effect, enable_image_tech, accessories_random_tims,
               object_random_times, suffix_words_random_times, assign_angle, assign_body_framing, assign_place,
               assign_pose, assign_job, assigin_expression, assign_clothes, assign_leg_wear, assign_shoes,
               assign_leg_wear_color, assign_shoes_color, assign_hair_color):
    if angle:
        project_config["angle"] = ""
    else:
        project_config["angle"] = assign_angle

    if body_framing:
        project_config["body_framing"] = ""
    else:
        project_config["body_framing"] = assign_body_framing

    if location:
        project_config["place"] = ""
    else:
        project_config["place"] = assign_place

    if pose_type == 2:
        project_config["assign_pose"] = assign_pose
    else:
        project_config["assign_pose"] = ""
        project_config["pose_type"] = pose_type + 1

    project_config["dynamic_mode"] = dynamic_mode
    if breasts_size == "空NULL":
        project_config["breasts_size"] = "null"
    else:
        project_config["breasts_size"] = breasts_size

    project_config["body_wear"] = body_wear + 1
    project_config["top_wear"] = top_wear + 1
    project_config["bottom_wear"] = bottom_wear + 1
    project_config["leg_wear"] = leg_wear + 1
    project_config["panties"] = panties
    project_config["shoes_type"] = shoes_type + 1
    project_config["body_with"] = body_with
    project_config["body_status"] = body_status
    project_config["body_description"] = body_desc
    project_config["cloth_trim"] = cloth_trim
    if profession:
        project_config["assign_profession"] = ""
    else:
        project_config["assign_profession"] = assign_job

    if hair_color and assign_hair_color == "":
        project_config["hair_color"] = "random"
    else:
        if assign_hair_color == "":
            project_config["hair_color"] = "null"
        else:
            project_config["hair_color"] = assign_hair_color
    project_config["add_hair_style"] = add_hair_style
    project_config["enable_eye_color"] = enable_eye_color
    project_config["has_girl_desc"] = has_girl_desc
    project_config["add_girl_beautyful"] = add_girl_beautyful

    if face_expression <= 4:
        project_config["face_expression"] = face_expression + 1
    else:
        project_config["assign_expression"] = assigin_expression

    project_config["nsfw_type"] = nsfw_type + 1
    project_config["is_nsfw"] = is_nsfw
    project_config["is_uncensored"] = is_uncensored
    project_config["is_simple_nude"] = is_simple_nude
    project_config["nude_strong"] = nude_strong

    project_config["sexual_list_random_index_times"] = sexual_list_random_index_times
    project_config["nude_list_random_index_times"] = nude_list_random_index_times

    project_config["use_starting"] = has_starting
    project_config["is_realistic"] = is_realistic
    project_config["add_colors"] = add_colors
    project_config["enable_day_weather"] = enable_day_weather
    project_config["enable_light_effect"] = enable_light_effect
    project_config["enable_image_tech"] = enable_image_tech
    project_config["accessories_random_tims"] = accessories_random_tims
    project_config["object_random_times"] = object_random_times
    project_config["suffix_words_random_times"] = suffix_words_random_times

    project_config["assign_body_clothes"] = assign_clothes
    project_config["assign_leg_wear"] = assign_leg_wear
    project_config["assign_shoes"] = assign_shoes
    project_config["leg_wear_color"] = assign_leg_wear_color
    project_config["shoes_color"] = assign_shoes_color

    lora_config = get_model_input(lora)
    lyco_config = get_model_input(lyco)
    embeddings_config = get_model_input(embeddings)
    project_config["lora"] = lora_config
    project_config["lyco"] = lyco_config
    project_config["embeddings"] = embeddings_config
    if model_order is None or model_order == '':
        model_order = "xyz"
    project_config["models_order"] = model_order
    project_config["additional_prompt"] = additional_prompt
    return create_prompts(gen_times, project_config)


def send_action(result_text):
    if t2i_text_box is not None:
        lines = result_text.split("\n")
        stripped_lines = [line.strip() for line in lines]
        if len(stripped_lines) > 0:
            return stripped_lines[0]


######### UI #########
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        gr.Markdown("根据下面配置随机生成prompt")

        with gr.Box():
            with gr.Row():
                time_slider = gr.Slider(1, 6, value=4, label="随机生成条数", step=1, interactive=True)

        with gr.Box():
            gr.Markdown("视角、地点、动作")
            with gr.Row():
                angle = gr.Checkbox(False, label="视角", info="正面，侧面，背面...")
                body_framing = gr.Checkbox(False, label="身体框架", info="肖像，半身，全身...")
                location = gr.Checkbox(False, label="地点", info="随机地点")
                pose_type = gr.Dropdown(['基础', '全身', '空NULL'], value='空NULL', type="index", label="动作类型",
                                        interactive=True,
                                        info="人物动作，站、坐、躺...")
                dynamic_mode = gr.Checkbox(False, label="动态模式", info="使用dynamic pose, angle，需对应配置勾选")
        with gr.Box():
            gr.Markdown("身体穿着描述, 选择空NULL则不生成该tag")
            with gr.Column():
                with gr.Row():
                    breasts_size = gr.Dropdown(["medium", "large", "huge", "gigantic", "空NULL"], value="空NULL",
                                               label="胸大小描述", info="依次增大= =#", interactive=True)
                    body_wear = gr.Dropdown(["裙子dress", "制服UNIFORM", "紧身衣BODYSUIT", "传统服饰TRADITIONAL",
                                             "上下搭配(如上身体恤下身短裙)", "以上随机", "空NULL"], value="裙子dress",
                                            type="index", label="衣服", info="", interactive=True)
                    top_wear = gr.Dropdown(["衬衫SHIRTS", "外套COAT", "毛衣SWEATER", "其他OTHERS", "以上随机RANDOM"],
                                           value="衬衫SHIRTS", type="index", label="上身衣物",
                                           info="选择上下搭配(如上身体恤下身短裙)该配置生效", interactive=True)
                    bottom_wear = gr.Dropdown(["裤子PANTS", "短裙SKIRT", "短裤SHORTS", "以上随机RANDOM"],
                                              value="短裙SKIRT", type="index", label="下身衣物",
                                              info="选择上下搭配(如上身体恤下身短裙)该配置生效", interactive=True)
                with gr.Row():
                    leg_wear = gr.Dropdown(
                        ["短袜SOCKS", "小腿袜KNEEHIGHS", "过膝袜OVERKNEEHIGHS", "大腿袜THIGHHIGHS", "连裤袜PANTYHOSE",
                         "光腿BARE", "空NULL", "以上随机RANDOM"], value="空NULL", type="index", label="袜子",
                        interactive=True)
                    panties = gr.Checkbox(False, label="内裤", info="勾选则随机给生成一种内裤类型")
                    shoes_type = gr.Dropdown(
                        ["靴子BOOTS", "高跟鞋HIGHHEELS", "凉鞋SANDALS", "拖鞋SLIPPERS", "光脚BARE", "空NULL"],
                        value="空NULL", type="index", label="鞋子", info="", interactive=True)
                with gr.Row():
                    body_with = gr.Checkbox(False, label="身体缠绕物", info="缠绕一些东西，束缚，丝带，链条")
                    body_status = gr.Checkbox(False, label="身体状态", info="湿身、出汗...")
                    body_desc = gr.Checkbox(False, label="身体描述", info="完美身材，纤细身体...")
                    cloth_trim = gr.Checkbox(False, label="衣服装饰", info="蕾丝，丝带，金色，花等等...")
        with gr.Box():
            gr.Markdown("人物描述")
            with gr.Row():
                profession = gr.Checkbox(False, label="职业", info="随机职业，学生，护士...")
                hair_color = gr.Checkbox(True, label="头发颜色", info="", interactive=True)
                add_hair_style = gr.Checkbox(False, label="头发风格", info="发型")
                enable_eye_color = gr.Checkbox(True, label="眼睛颜色", info="")
            with gr.Row():
                face_expression = gr.Dropdown(
                    ["情绪EMOTIONS", "诱惑的SEXUAL", "笑容SMILE", "俏皮的SMUG", "以上随机", "空NULL"],
                    value="笑容SMILE",
                    type="index", label="表情", interactive=True)
                add_girl_beautyful = gr.Checkbox(False, label="描述妹子的短词缀", info="")
                has_girl_desc = gr.Checkbox(False, label="描述妹子的长词缀", info="")

        with gr.Accordion("NSFW配置", open=False):
            with gr.Box():
                with gr.Row():
                    nsfw_type = gr.Dropdown(["裸NUDE", "性感SEXUAL", "常规NOTNSFW"], value="常规NOTNSFW", type="index",
                                            label="NSFW等级",
                                            info="请确保你知道自己在干嘛！选择非常规类型，上面的人物衣服设置不生效",
                                            interactive=True)
                    is_nsfw = gr.Checkbox(False, label="是否添加nfsw词缀")
                    is_uncensored = gr.Checkbox(False, label="是否添加uncensored词缀")
                    is_simple_nude = gr.Checkbox(False, label="是否是简单的nude模式", info="裸模式生效")
                    nude_strong = gr.Checkbox(False, label="是否加强nude模式", info="裸模式生效")
                with gr.Row():
                    sexual_list_random_index_times = gr.Slider(0, 5, value=0, step=1, label="性感词缀随机数",
                                                               interactive=True)
                    nude_list_random_index_times = gr.Slider(0, 9, value=0, step=1, label="裸体词缀随机数",
                                                             interactive=True)
        with gr.Box():
            gr.Markdown("其他")
            with gr.Row():
                has_starting = gr.Checkbox(True, label="是否使用起手式", info="best quality, absurdres,")
                is_realistic = gr.Checkbox(False, label="是否添加真实词缀")
                add_colors = gr.Checkbox(False, label="是否添加多彩词缀")
                enable_day_weather = gr.Checkbox(False, label="是否添加天气信息")
                enable_light_effect = gr.Checkbox(True, label="是否添加灯光效果")
                enable_image_tech = gr.Checkbox(False, label="是否开启图像技术，如模糊")
            with gr.Row():
                accessories_random_tims = gr.Slider(0, 8, value=0, step=1, label="饰物随机数", interactive=True,
                                                    info="戒指，袜带等")
                object_random_times = gr.Slider(0, 8, value=0, step=1, label="物品随机数", info="花，冰火元素等",
                                                interactive=True)
                suffix_words_random_times = gr.Slider(0, 10, value=0, step=1, label="形容词缀随机数",
                                                      info="一些描述奇幻，美丽相关的词缀",
                                                      interactive=True)
        with gr.Accordion("Lora Loha embedding控制", open=False):
            with gr.Box():
                with gr.Row():
                    lora = gr.Textbox("", label="Lora【x】",
                                      info="格式如下：101, '101:0.6',    输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'101:0.8'，则表示lora权重0.8")
                    lyco = gr.Textbox("", label="lyco【y】",
                                      info="格式如下：101, '101:0.6',    输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'101:0.8'，则表示lora权重0.8")
                with gr.Row():
                    embeddings = gr.Textbox("", label="embeddings【z】",
                                            info="格式如下：100, '100:0.6', '100:0.6'\n输入单纯的数字100，或者使用''包裹数字，加上:后面跟上权重'100:0.8'，则表示lora权重0.8")
                    model_order = gr.Textbox("xyz", label="lora，lyco，embed顺序",
                                             info="默认为xyz顺序，即按照lora，lyco，emb顺序")
        with gr.Accordion("精准控制项", open=False):
            with gr.Box():
                with gr.Row():
                    assign_angle = gr.Textbox("null", label="指定视角")
                    assign_body_framing = gr.Textbox("null", label="指定身体框架")
                    assign_place = gr.Textbox("null", label="指定地点")
                with gr.Row():
                    assign_pose = gr.Textbox("null", label="指定人物动作")
                    assign_job = gr.Textbox("null", label="指定角色")
                    assigin_expression = gr.Textbox("", label="指定人物表情")
                with gr.Row():
                    assign_clothes = gr.Textbox("", label="指定衣服")
                    assign_leg_wear = gr.Textbox("", label="指定袜子类型")
                    assign_shoes = gr.Textbox("", label="指定鞋子类型")
                with gr.Row():
                    assign_leg_wear_color = gr.Textbox("", label="指定袜子颜色")
                    assign_shoes_color = gr.Textbox("", label="指定鞋子颜色")
                    assign_hair_color = gr.Textbox("", label="指定头发颜色")

        with gr.Box():
            gr.Markdown("手动输入项")
            with gr.Row():
                additional_prompt = gr.Textbox("", label="额外的prompt")

        results = gr.Textbox("", label="生成的prompt", show_copy_button=True, interactive=False)
        with gr.Row():
            gen_button = gr.Button("生成prompt")
            send_button = gr.Button("发送到文生图")

        gen_button.click(gen_action,
                         inputs=[time_slider, lora, lyco, embeddings, model_order, additional_prompt, angle,
                                 body_framing, location,
                                 pose_type, dynamic_mode, breasts_size, body_wear, top_wear, bottom_wear, leg_wear,
                                 panties, shoes_type, body_with, body_status, body_desc, cloth_trim, profession,
                                 hair_color, add_hair_style, enable_eye_color, face_expression, add_girl_beautyful,
                                 has_girl_desc, nsfw_type, is_nsfw, is_uncensored, is_simple_nude,
                                 nude_strong, sexual_list_random_index_times, nude_list_random_index_times,
                                 has_starting, is_realistic,
                                 add_colors, enable_day_weather, enable_light_effect, enable_image_tech,
                                 accessories_random_tims,
                                 object_random_times, suffix_words_random_times, assign_angle, assign_body_framing,
                                 assign_place, assign_pose, assign_job, assigin_expression, assign_clothes,
                                 assign_leg_wear, assign_shoes, assign_leg_wear_color, assign_shoes_color,
                                 assign_hair_color], outputs=results)
        send_button.click(send_action, inputs=results, outputs=t2i_text_box)
        return [(ui_component, "随机提示词RP", "随机提示词RP")]
        # return ui_component


def after_component(component, **kwargs):
    # Find the text2img textbox component
    global t2i_text_box
    if kwargs.get("elem_id") == "txt2img_prompt":  # postive prompt textbox
        t2i_text_box = component
    # Find the img2img textbox component
    # if kwargs.get("elem_id") == "img2img_prompt":  # postive prompt textbox
    #     self.boxxIMG = component


# on_ui_tabs().launch(debug=True)
script_callbacks.on_ui_tabs(on_ui_tabs)
script_callbacks.on_after_component(after_component)
