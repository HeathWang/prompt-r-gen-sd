import importlib
import json
import re
from collections import defaultdict
import os

import gradio as gr

from promptsModules.db.datamodel import (
    DataBase,
    Image as DbImg,
    Tag,
    TrainTag,
    TrainImageTags,
)
from promptsModules.db.update_image_data import (update_image_data)
from promptsModules.model_manager import (LoraConfigManager)
from promptsModules.sd_command_gen import project_config as gen_config
from promptsModules.train_tags import (handle_train_tag)
from promptsModules.web_api import (create_prompts)

project_config = gen_config
t2i_text_box = None
query_cursor: str = None
IS_PLUGIN = True

cache_search = defaultdict(int)


def get_model_input(com_value):
    arr = com_value.split(",")
    target_list = []
    if len(arr) > 0:
        target_list = [x.strip() for x in arr if x.strip()]
    return target_list


######### gen #########
# 我有史以来写的最长的方法
def gen_action(gen_times, widget_lora, widget_lyco, widget_embeddings, model_order, additional_prompt, angle,
               body_framing, location,
               pose_type,
               dynamic_mode, breasts_size, body_wear, top_wear, bottom_wear, leg_wear, panties, shoes_type, body_with,
               body_status, body_desc, cloth_trim, profession, hair_color, add_hair_style, enable_eye_color,
               face_expression, add_girl_beautyful, has_girl_desc, nsfw_type, is_nsfw, is_uncensored, is_simple_nude,
               nude_strong, sexual_list_random_index_times, nude_list_random_index_times, has_starting, is_realistic,
               add_colors, enable_day_weather, enable_light_effect, enable_image_tech, accessories_random_tims,
               object_random_times, suffix_words_random_times, assign_angle, assign_body_framing, assign_place,
               assign_pose, assign_job, assigin_expression, assign_clothes, assign_leg_wear, assign_shoes,
               assign_leg_wear_color, assign_shoes_color, assign_hair_color, hair_accessories, neck_accessories,
               earrings, has_ending, hair_length, people_cnt, body_skin):
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
    project_config["body_skin"] = body_skin
    project_config["cloth_trim"] = cloth_trim
    if profession:
        project_config["assign_profession"] = ""
    else:
        project_config["assign_profession"] = assign_job

    project_config["hair_color"] = hair_color
    project_config["assign_hair_color"] = assign_hair_color
    project_config["add_hair_style"] = add_hair_style
    project_config["add_hair_length"] = hair_length
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

    project_config["add_hair_accessories"] = hair_accessories
    project_config["add_neck_accessories"] = neck_accessories
    project_config["add_earrings"] = earrings
    project_config["add_detail_suffix"] = has_ending
    project_config["girl_cnt"] = people_cnt

    lora_config = get_model_input(widget_lora)
    lyco_config = get_model_input(widget_lyco)
    embeddings_config = get_model_input(widget_embeddings)
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
            top_ele = stripped_lines[0]
            top_ele = re.sub(r'\n+$', '', top_ele)
            return top_ele
    else:
        raise gr.Error("请安装到sd webui中使用此功能.")


def load_config_action():
    return LoraConfigManager().export_to_data_frame()


def get_prompts_from_folder(file_path, check_force, check_flux_flag_2=False):
    try:
        DataBase._initing = True
        img_count = DbImg.count(DataBase.get_conn())
        update_image_data([file_path], is_rebuild=check_force, is_flux=check_flux_flag_2)
        after_img_cnt = DbImg.count(DataBase.get_conn())
        return f"新增{after_img_cnt - img_count}条记录", f"共{after_img_cnt}条记录"
    finally:
        DataBase._initing = False


def create_tag_html(tag, height, suffix=None, border_color="#25BDCDAD", score=None):
    tag_html = ""
    height_style = ""
    if height is not None:
        height_style = f"height: {height}px;"
    tag_html += (
        f"<div style='display: flex; align-items: center; justify-content: flex-start; padding: 0px 12px 0px 12px; margin: 0 12px 12px 0; border: 2px solid {border_color}; border-radius: 12px; {height_style} font-size: 18px;'>"
        f"<div>{tag}</div>"
    )
    if suffix is not None:
        text, color = suffix
        suffix_v = text
        if score is not None and score != "" and score != 0:
            suffix_v += f"({score})"
        tag_html += (
            f"<div style='padding-left: 12px;  font-style: italic; font-weight: bolder; color: {color};'>{suffix_v}</div>"
        )
    tag_html += "</div>"
    return tag_html


def create_img_info_html(exif, check_res_show, check_adetailer_show, date_info=""):
    if check_res_show is not True and check_adetailer_show is not True:
        return ""
    tag_html = ""
    res = ""
    adetailer = ""
    if exif is not None and exif != "" and check_res_show is True:
        res_match = re.search(r'\bSize: (\d+x\d+)\b', exif)
        if res_match:
            res = res_match.group(1)

    if exif is not None and exif != "" and check_adetailer_show is True:
        adetailer_match = re.search(r'ADetailer prompt: "([^"]+)"', exif)
        if adetailer_match:
            adetailer = adetailer_match.group(1)
            adetailer = adetailer.replace("<", "&lt;").replace(">", "&gt;")
    tag_html += (
        f"<div style='display: flex; align-items: center; justify-content: start; padding: 0px 12px 0px 12px; margin: 0 12px 12px 0; background: #3C2DFF60; font-size: 14px;'>"
        f"<div style='padding-right: 14px;'>{res}</div>"
        f"<div style='padding-right: 14px;'>{adetailer}</div>"
        f"<div>{date_info}</div>"
        "</div>"
    )

    return tag_html


def search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                  check_search_adetailer_prompt=False, check_search_flux=False):
    return base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                              check_search_adetailer_prompt, check_search_flux)


def next_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                       check_search_adetailer_prompt=False, check_search_flux=False):
    return base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                              check_search_adetailer_prompt, check_search_flux, is_next=True)


def base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                       check_search_adetailer_prompt, check_search_flux:bool, is_next=False):
    query_name = extract_tag_name(key_input)
    global query_cursor
    global cache_search
    cache_search[query_name] += 1

    conn = DataBase.get_conn()
    imgs, next_cursor = DbImg.find_by_substring(
        conn=conn,
        substring=query_name.strip(),
        cursor=is_next and query_cursor or None,
        limit=limit_slider,
        regexp=check_search_adetailer_prompt and r'ADetailer prompt: "([^"]+)"' or None,
        from_exif=check_search_adetailer_prompt,
        is_flux=check_search_flux
    )

    pos_prompt_counts = defaultdict(int)
    exif_dict = defaultdict(str)
    date_dict = defaultdict(str)
    list_search = []
    index = 0

    for img in imgs:
        pos_prompt = img.pos_prompt
        pos_prompt_counts[pos_prompt] += 1
        exif_dict[pos_prompt] = img.exif
        date_dict[pos_prompt] = img.date

    target_prompt_counts = list(pos_prompt_counts.items())
    if sort_drop == 0:
        sorted_pos_prompt_counts = sorted(pos_prompt_counts.items(), key=lambda x: x[1], reverse=True)
        target_prompt_counts = sorted_pos_prompt_counts

    for pos_prompt_t, count in target_prompt_counts:
        list_search.append([index, pos_prompt_t, count])
        index += 1

    result_count = f"🔍{len(imgs)}: {len(list_search)}"

    table_html = "<table><tr><th>序列</th><th>prompt</th><th>count</th></tr>"
    for row in list_search:
        table_html += (f"<tr>"
                       f"<td>{row[0]}</td>"
                       f"<td>{create_tag_html(row[1].replace('<', '&lt;').replace('>', '&gt;'), height=None)}{create_img_info_html(exif_dict[row[1]], check_res_show, check_adetailer_show, date_dict[row[1]])}</td>"
                       f"<td style='font-style: italic; font-weight: bolder; color: burlywood;'>{row[2]}</td>"
                       f"</tr>")
    table_html += "</table>"
    query_cursor = next_cursor
    # make cache_search to List[Tuple[str, float | str]]]
    cache_search_list = cache_search_list = [(key, str(value)) for key, value in cache_search.items()]
    print(cache_search_list)

    return [result_count, table_html, cache_search_list]

def extract_tag_name(tip):
    match = re.match(r"^(.*) \[✨", tip)
    return match.group(1) if match else tip

def get_tag_info(tag: Tag):
    cnt = f""
    suffix_color = "burlywood"
    if tag.count is not None and tag.count > 0:
        if tag.count < 1000:
            cnt = f"\t<{tag.count}>"
        elif tag.count < 10000:
            cnt = f"\t<{tag.count / 1000:.2f}k>"
        else:
            cnt = f"\t<{tag.count / 10000:.2f}w>"

        if tag.count < 16:
            suffix_color = "#63FFA2"  # 绿色
        elif tag.count < 128:
            suffix_color = "#559BFF"  # 黄色
        elif tag.count < 256:
            suffix_color = "#3553FF"  # 浅蓝
        elif tag.count < 512:
            suffix_color = "#7214FF"  # 浅紫
        elif tag.count < 1024:
            suffix_color = "#00EAFB"  # 青色
        elif tag.count < 5210:
            suffix_color = "#FF2700"  # 浅红
        else:
            suffix_color = "#FF0035"  # 红色

    return tag.name, (cnt.replace("<", "&lt;").replace(">", "&gt;"), suffix_color)


def inner_fetch_lora(conn):
    lora_result = Tag.get_all_lora_tag(conn)
    lora_html = "<div style='display: flex; align-items: flex-start; justify-content: flex-start; flex-wrap: wrap;'>"
    for lora in lora_result:
        tag, cnt = get_tag_info(lora)
        lora_html += create_tag_html(tag=tag, height=28, suffix=cnt, score=lora.score)
    lora_html += "</div>"
    return lora_html


def fetch_lora_action():
    conn = DataBase.get_conn()
    return inner_fetch_lora(conn)


def fetch_lyco_action():
    conn = DataBase.get_conn()
    lora_result = Tag.get_all_lyco_tag(conn)
    lyco_html = "<div style='display: flex; align-items: flex-start; justify-content: flex-start; flex-wrap: wrap;'>"
    for lyco in lora_result:
        tag, cnt = get_tag_info(lyco)
        lyco_html += create_tag_html(tag, suffix=cnt, height=28)
    lyco_html += "</div>"
    return lyco_html


def delete_lora_action(delete_lora_input):
    if delete_lora_input is None or delete_lora_input == "":
        raise gr.Error("请输入要删除的lora")
    conn = DataBase.get_conn()
    Tag.remove_by_name(conn, delete_lora_input)
    lora_html = inner_fetch_lora(conn)
    conn.close()
    DataBase.reConnect = True
    return lora_html

def load_lora_list():
    lora_result = Tag.get_all_lora_tag(DataBase.get_conn())

    lora_list = []
    for lora in lora_result:
        lora_list.append(lora.name)
    return lora_list


def open_sd_image_broswer_html():
    # 创建包含按钮的HTML
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
    
    <h2>打开Infinite image browsing</h2>
    
    <button style='width:100%;' onclick="window.location.href='/infinite_image_browsing'">点我</button>
    
    </body>
    </html>
    """
    return html_code


def save_train_tag_action(train_source_path, train_alias, train_comments, check_handle_train_folder:bool, check_is_flux_model:bool):
    if check_handle_train_folder:
        # check if folder
        if not os.path.isdir(train_source_path):
            return f"{train_source_path}不是文件夹"
        # get all sub folder
        conn = DataBase.get_conn()
        count = 0

        for file_name in os.listdir(train_source_path):
            file_path = os.path.join(train_source_path, file_name)
            if os.path.isdir(file_path):
                json_str, alias_name, files_list = handle_train_tag(file_path, "")

                train = TrainTag(alias_name, json_str, comments=train_comments)
                train.save(conn)
                TrainImageTags.saveTags(conn, train.id, files_list)
                count += 1

        conn.close()
        DataBase.reConnect = True
        return f"处理完成，共{count}个文件夹"
    else:
        json_str, alias_name, files_list = handle_train_tag(train_source_path, train_alias)
        conn = DataBase.get_conn()
        resp = json_str
        if not check_is_flux_model:
            train = TrainTag(alias_name, json_str, comments=train_comments, is_flux=0)
        else:
            resp = "success"
            train = TrainTag(alias_name, '{}', comments=train_comments, is_flux=1)
        train.save(conn)
        TrainImageTags.saveTags(conn, train.id, files_list)
        conn.close()
        DataBase.reConnect = True
        return resp

def update_train_tag_comments(train_model_dropdown, train_update_comments):
    conn = DataBase.get_conn()
    train = TrainTag(train_model_dropdown, tags_info="", comments=train_update_comments)
    train.update_comments(conn)
    gr.Info(f"更新{train_model_dropdown}完成")


def get_train_model_tags(train_input_model):
    conn = DataBase.get_conn()
    train = TrainTag.get(conn, train_input_model.strip())

    source_tag = TrainImageTags.getAllTags(conn, train.id)
    if train is None:
        return [], ""
    tags = json.loads(train.tags_info)
    # 将字典按照值的数值降序排序
    sorted_tags = sorted(tags.items(), key=lambda x: int(x[1]), reverse=True)

    # 将排序后的结果转换为列表
    results = [(key, str(value)) for key, value in sorted_tags]

    html_comments = (f"<div style='display: flex; color: aqua; font-size: 14px; font-weight: lighter; text-decoration: underline;'>"
                     f"<div style='padding-right: 10px;'>{train.model_name}</div><div>{train.comments}</div>"
                     f"</div>")

    table_html = "<table><tr><th>序列</th><th>prompt</th></tr>"
    for index, image_file_tag in enumerate(source_tag):
        table_html += (f"<tr>"
                       f"<td>{index}</td>"
                       f"<td>{create_tag_html(image_file_tag.replace('<', '&lt;').replace('>', '&gt;'), height=None)}</td>"
                       f"</tr>")
    table_html += "</table>"

    return results, html_comments, table_html

def load_train_models(is_flux=False):
    conn = DataBase.get_conn()
    train_models = TrainTag.get_all(conn, is_flux=is_flux)
    names = []
    for train in train_models:
        names.append(train.model_name)
    return names

def reload_train_models(check_flux_flag:bool):
    return gr.update(choices=load_train_models(is_flux=check_flux_flag))

def load_query_tips():
    tags = Tag.get_all_model_tags(DataBase.get_conn())
    tips = []
    for tag in tags:
        tips.append(f"{tag.name} [✨{tag_count_to_short_str(tag.count)}]")
    return tips

def tag_count_to_short_str(count):
    cnt = ""
    if count < 1000:
        cnt = f"{count}"
    elif count < 10000:
        cnt = f"{count / 1000:.2f}k"
    else:
        cnt = f"{count / 10000:.2f}w"
    return cnt


def reload_query_tips():
    return gr.update(choices=load_query_tips())

def update_lora_score_action(lora_list_dropdown, score_slider):
    Tag.update_tag_score(DataBase.get_conn(), lora_list_dropdown, score_slider)
    return inner_fetch_lora(DataBase.get_conn())

######### UI #########
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Tab('🔍'):
            with gr.Column():
                with gr.Row(variant="panel"):
                    key_dropdown = gr.Dropdown(choices=load_query_tips(), allow_custom_value=True, interactive=True, type="value", label="🔍", show_label=True)
                with gr.Row():
                    sort_drop = gr.Dropdown(["数量", "时间"], value="数量", type="index", label="排序方式",
                                            interactive=True)
                    check_res_show = gr.Checkbox(True, label="分辨率", info="是否显示分辨率", interactive=True)
                    check_adetailer_show = gr.Checkbox(True, label="adetailer", info="显示adetailer提示词",
                                                       interactive=True)
                    check_search_adetailer_prompt = gr.Checkbox(False, label="adetailer prompt", info="搜索adetailer",
                                                                interactive=True)
                    check_search_flux = gr.Checkbox(False, label="flux模型", info="是否是flux模型", interactive=True)
                    limit_slider = gr.Slider(64, 5120, value=512, label="搜索limit", step=4, min_width=600,
                                             interactive=True)
                search_history = gr.HighlightedText(show_label=False)
                with gr.Row():
                    search_button = gr.Button("搜索", variant='primary')
                    next_query_button = gr.Button("下一页", size="sm", variant='secondary')
                    refresh_dp_button = gr.Button("刷新下拉数据", variant="secondary")
                    search_info = gr.Textbox("", show_label=False, interactive=False)
                html_table = gr.HTML("", label=None, show_label=False, interactive=False)

                search_button.click(search_action,
                                    inputs=[key_dropdown, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                                            check_search_adetailer_prompt, check_search_flux],
                                    outputs=[search_info, html_table, search_history])
                key_dropdown.select(search_action,
                                 inputs=[key_dropdown, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                                         check_search_adetailer_prompt, check_search_flux],
                                 outputs=[search_info, html_table, search_history])
                next_query_button.click(next_search_action, inputs=[key_dropdown, limit_slider, sort_drop, check_res_show,
                                                                    check_adetailer_show,
                                                                    check_search_adetailer_prompt, check_search_flux],
                                        outputs=[search_info, html_table, search_history])
                refresh_dp_button.click(reload_query_tips, inputs=None, outputs=key_dropdown)
        with gr.Tab("Model"):
            with gr.Tab("Lora"):
                with gr.Column():
                    with gr.Row(equal_height=False, variant="panel"):
                        fetch_lora_btn = gr.Button("查询lora", variant='primary')
                        delete_lora_input = gr.Textbox("", show_label=False)
                        delete_lora_btn = gr.Button("删除lora", variant='secondary')
                    with gr.Row(equal_height=False):
                        lora_list_dropdown = gr.Dropdown(choices=load_lora_list(), allow_custom_value=True, interactive=True, type="value", show_label=False)
                        score_slider = gr.Slider(0, 1, value=0, label="分数", step=0.05, interactive=True)
                        score_btn = gr.Button("更新", variant='primary')
                    html_loras = gr.HTML("", label=None, show_label=False, interactive=False)
                    fetch_lora_btn.click(fetch_lora_action, outputs=html_loras)
                    delete_lora_btn.click(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    delete_lora_input.submit(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    score_btn.click(update_lora_score_action, inputs=[lora_list_dropdown, score_slider], outputs=html_loras)
            with gr.Tab("Lyco"):
                fetch_lyco_btn = gr.Button("查询lyco", variant='primary')
                html_lyco = gr.HTML("", label=None, show_label=False, interactive=False)
                fetch_lyco_btn.click(fetch_lyco_action, outputs=html_lyco)
            with gr.Tab("Tags"):
                with gr.Row():
                    check_flux_flag = gr.Checkbox(False, label="flux模型", info="是否是flux模型", interactive=True)
                with gr.Row(equal_height=False):
                    train_input_model = gr.Dropdown(choices=load_train_models(), allow_custom_value=True, interactive=True, type="value", show_label=False)
                    fetch_train_info_btn = gr.Button("查询train tags", variant='primary')
                    refresh_train_models_btn = gr.Button("刷新下拉数据", variant="secondary")
                train_tags_comments = gr.HTML("", label=None, show_label=False, interactive=False)
                tags_highlighted = gr.HighlightedText(show_label=False)
                tag_source_list = gr.HTML("", label=None, show_label=False, interactive=False)
                train_input_model.select(get_train_model_tags, inputs=[train_input_model],
                                         outputs=[tags_highlighted, train_tags_comments, tag_source_list])
                fetch_train_info_btn.click(get_train_model_tags, inputs=[train_input_model],
                                           outputs=[tags_highlighted, train_tags_comments, tag_source_list])
                refresh_train_models_btn.click(reload_train_models, inputs=[check_flux_flag], outputs=train_input_model)
        with gr.Tab('提取Prompt'):
            with gr.Tab("Images"):
                with gr.Column():
                    with gr.Row():
                        file_path = gr.Textbox("/notebooks/resource/outputs/20231225", label="文件路径", lines=1,
                                               show_copy_button=True, interactive=True)
                        check_force = gr.Checkbox(label='是否强制', show_label=True, info='')
                        check_flux_flag_2 = gr.Checkbox(False, label="flux模型", info="是否是flux模型", interactive=True)
                    extract_btn = gr.Button("提取prompt", variant="primary")
                    with gr.Row():
                        text2 = gr.Textbox(label="状态")
                        img_cnt = gr.Textbox(label="图片数量")
                    extract_btn.click(get_prompts_from_folder, inputs=[file_path, check_force, check_flux_flag_2], outputs=[text2, img_cnt])
                    file_path.submit(get_prompts_from_folder, inputs=[file_path, check_force, check_flux_flag_2], outputs=[text2, img_cnt])
            with gr.Tab("Train Source"):
                with gr.Column():
                    with gr.Row():
                        train_source_path = gr.Textbox("/notebooks/", label="训练的tag文件路径", lines=1,
                                                       show_copy_button=True, interactive=True)
                        train_alias = gr.Textbox(None, label="别名", lines=1, interactive=True)
                        train_comments = gr.Textbox(None, label="添加备注，描述模型详情", lines=2, interactive=True)
                        check_handle_train_folder = gr.Checkbox(False, label="是否处理文件夹",
                                                                info="勾选则处理文件夹下所有子目录", interactive=True)
                        check_is_flux_model = gr.Checkbox(False, label="是否flux模型", info="是否是flux模型，不处理tag分组", interactive=True)
                    train_result = gr.Textbox("", label="汇总结果", lines=1, show_copy_button=True, interactive=False)
                    with gr.Row():
                        train_tag_btn = gr.Button("汇总tag", variant="primary")
                    train_tag_btn.click(save_train_tag_action, inputs=[train_source_path, train_alias, train_comments, check_handle_train_folder, check_is_flux_model],
                                        outputs=[train_result])
                    train_source_path.submit(save_train_tag_action, inputs=[train_source_path, train_alias, train_comments, check_handle_train_folder, check_is_flux_model],
                                             outputs=[train_result])

                with gr.Column():
                    with gr.Row(equal_height=False):
                        train_model_dropdown = gr.Dropdown(choices=load_train_models(), interactive=True, allow_custom_value=True, show_label=False)
                        train_update_comments = gr.Textbox(None, label="添加备注，描述模型详情", lines=2, interactive=True)
                    train_update_btn = gr.Button("更新备注", variant="primary")
                    train_update_btn.click(update_train_tag_comments, inputs=[train_model_dropdown, train_update_comments])


        with gr.Tab("生成Prompt"):
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("请修改以下配置")

                    with gr.Box():
                        with gr.Row():
                            time_slider = gr.Slider(1, 6, value=1, label="随机生成条数", step=1, interactive=True)
                    with gr.Accordion("视角、地点、动作", open=False):
                        with gr.Row():
                            angle = gr.Checkbox(False, label="视角", info="正面，侧面，背面...")
                            body_framing = gr.Checkbox(False, label="身体框架", info="肖像，半身，全身...")
                            location = gr.Checkbox(False, label="地点", info="随机地点")
                            pose_type = gr.Dropdown(['基础', '全身', '空NULL'], value='空NULL', type="index",
                                                    label="动作类型",
                                                    interactive=True,
                                                    info="人物动作，站、坐、躺...")
                            dynamic_mode = gr.Checkbox(False, label="动态模式",
                                                       info="使用dynamic pose, angle，需对应配置勾选")
                    with gr.Accordion("人物衣着", open=False):
                        with gr.Column():
                            with gr.Row():
                                breasts_size = gr.Dropdown(["medium", "large", "huge", "gigantic", "空NULL"],
                                                           value="空NULL",
                                                           label="胸大小描述", info="依次增大= =#", interactive=True)
                                body_wear = gr.Dropdown(
                                    ["裙子dress", "制服UNIFORM", "紧身衣BODYSUIT", "传统服饰TRADITIONAL",
                                     "上下搭配(如上身体恤下身短裙)", "以上随机", "空NULL"], value="空NULL",
                                    type="index", label="衣服", info="", interactive=True)
                                top_wear = gr.Dropdown(
                                    ["衬衫SHIRTS", "外套COAT", "毛衣SWEATER", "其他OTHERS", "以上随机RANDOM"],
                                    value="衬衫SHIRTS", type="index", label="上身衣物",
                                    info="选择上下搭配(如上身体恤下身短裙)该配置生效", interactive=True)
                                bottom_wear = gr.Dropdown(["裤子PANTS", "短裙SKIRT", "短裤SHORTS", "以上随机RANDOM"],
                                                          value="短裙SKIRT", type="index", label="下身衣物",
                                                          info="选择上下搭配(如上身体恤下身短裙)该配置生效",
                                                          interactive=True)
                            with gr.Row():
                                leg_wear = gr.Dropdown(
                                    ["短袜SOCKS", "小腿袜KNEEHIGHS", "过膝袜OVERKNEEHIGHS", "大腿袜THIGHHIGHS",
                                     "连裤袜PANTYHOSE",
                                     "光腿BARE", "空NULL", "以上随机RANDOM"], value="空NULL", type="index",
                                    label="袜子",
                                    interactive=True)
                                panties = gr.Checkbox(False, label="内裤", info="勾选则随机给生成一种内裤类型")
                                shoes_type = gr.Dropdown(
                                    ["靴子BOOTS", "高跟鞋HIGHHEELS", "凉鞋SANDALS", "拖鞋SLIPPERS", "光脚BARE",
                                     "空NULL"],
                                    value="空NULL", type="index", label="鞋子", info="", interactive=True)
                            with gr.Row():
                                body_with = gr.Checkbox(False, label="身体缠绕物", info="缠绕一些东西，束缚，丝带，链条")
                                body_status = gr.Checkbox(False, label="身体状态", info="湿身、出汗...")
                                body_desc = gr.Checkbox(False, label="身体描述", info="完美身材，纤细身体...")
                                cloth_trim = gr.Checkbox(False, label="衣服装饰", info="蕾丝，丝带，金色，花等等...")
                    with gr.Accordion("人物描述", open=False):
                        with gr.Row():
                            profession = gr.Checkbox(False, label="职业")
                            people_cnt = gr.Slider(0, 8, value=1, label="人物数量", step=1, interactive=True)
                        with gr.Row():
                            hair_length = gr.Checkbox(True, label="头发长度")
                            hair_color = gr.Checkbox(True, label="头发颜色", interactive=True)
                            add_hair_style = gr.Checkbox(False, label="头发风格")
                            enable_eye_color = gr.Checkbox(True, label="眼睛颜色")
                        with gr.Row():
                            hair_accessories = gr.Checkbox(True, label="头饰")
                            neck_accessories = gr.Checkbox(True, label="颈部饰物")
                            earrings = gr.Checkbox(True, label="耳环")
                            body_skin = gr.Checkbox(False, label="皮肤")
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
                                nsfw_type = gr.Dropdown(["裸NUDE", "性感SEXUAL", "常规NOTNSFW"], value="常规NOTNSFW",
                                                        type="index",
                                                        label="NSFW等级",
                                                        info="请确保你知道自己在干嘛！选择非常规类型，上面的人物衣服设置不生效",
                                                        interactive=True)
                                is_nsfw = gr.Checkbox(False, label="是否添加nfsw词缀")
                                is_uncensored = gr.Checkbox(False, label="是否添加uncensored词缀")
                                is_simple_nude = gr.Checkbox(False, label="是否是简单的nude模式", info="裸模式生效")
                                nude_strong = gr.Checkbox(False, label="是否加强nude模式", info="裸模式生效")
                            with gr.Row():
                                sexual_list_random_index_times = gr.Slider(0, 5, value=0, step=1,
                                                                           label="性感词缀随机数",
                                                                           interactive=True)
                                nude_list_random_index_times = gr.Slider(0, 9, value=0, step=1, label="裸体词缀随机数",
                                                                         interactive=True)
                    with gr.Accordion("Lora Loha embedding控制", open=False):
                        gr.Markdown(
                            """
                            关于lora/loha/embedding详细配置使用：[点我查看](https://github.com/HeathWang/prompt-r-gen-sd#loralohaembedding%E6%8E%A7%E5%88%B6%E8%AF%B4%E6%98%8E)
                            """
                        )
                        with gr.Box():
                            with gr.Row():
                                widget_lora = gr.Textbox("", label="Lora【x】",
                                                         info="格式如下：101, 101:0.6, 路易斯:0.65",
                                                         elem_id="rp_widget_lora")
                                widget_lyco = gr.Textbox("", label="lyco【y】",
                                                         info="格式如下：101, 101:0.6, 添加细节:1",
                                                         elem_id="rp_widget_lyco")
                            with gr.Row():
                                widget_embeddings = gr.Textbox("", label="embeddings【z】",
                                                               info="格式如下：100, ul:0.6",
                                                               elem_id="rp_widget_embeddings")
                                model_order = gr.Textbox("xyz", label="lora，lyco，embed顺序",
                                                         info="默认为xyz顺序，即按照lora，lyco，emb顺序")
                    with gr.Accordion("其他", open=False):
                        with gr.Row():
                            has_starting = gr.Checkbox(True, label="是否使用起手式", info="best quality, absurdres,")
                            has_ending = gr.Checkbox(True, label="添加细节", info="jewelry, ultra-detailed, 8k,")
                            is_realistic = gr.Checkbox(False, label="是否添加真实词缀",
                                                       info="realistic, photorealistic")
                            add_colors = gr.Checkbox(False, label="是否添加多彩词缀")
                        with gr.Row():
                            enable_day_weather = gr.Checkbox(False, label="是否添加天气信息")
                            enable_light_effect = gr.Checkbox(True, label="是否添加灯光效果")
                            enable_image_tech = gr.Checkbox(False, label="是否开启图像技术，如模糊")
                        with gr.Row():
                            accessories_random_tims = gr.Slider(0, 8, value=0, step=1, label="饰物随机数",
                                                                interactive=True,
                                                                info="戒指，袜带等")
                            object_random_times = gr.Slider(0, 8, value=0, step=1, label="物品随机数",
                                                            info="花，冰火元素等",
                                                            interactive=True)
                            suffix_words_random_times = gr.Slider(0, 10, value=0, step=1, label="形容词缀随机数",
                                                                  info="一些描述奇幻，美丽相关的词缀",
                                                                  interactive=True)

                    with gr.Accordion("精准控制项", open=False):
                        with gr.Box():
                            with gr.Row():
                                assign_angle = gr.Textbox("null", label="指定视角")
                                assign_body_framing = gr.Textbox("null", label="指定身体框架")
                                assign_place = gr.Textbox("null", label="指定地点")
                            with gr.Row():
                                assign_pose = gr.Textbox("null", label="指定人物动作")
                                assign_job = gr.Textbox("null", label="指定角色")
                                assigin_expression = gr.Textbox("null", label="指定人物表情")
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
                with gr.Column(scale=1):
                    gr.Markdown("prompt输出：")
                    results = gr.Textbox("", label="生成的prompt", lines=20, show_copy_button=True, interactive=True)
                    with gr.Row():
                        gen_button = gr.Button("生成prompt")
                        send_button = gr.Button("发送到文生图")
        with gr.Tab("其他"):
            with gr.Column():
                gr.HTML(open_sd_image_broswer_html(), label=None, show_label=False, interactive=True)
        with gr.Tab("查看配置"):
            review_btn = gr.Button("加载excel配置")
            data_sheet = gr.DataFrame(
                headers=["序列", "id", "类型", "模型名", "描述"],
                datatype=['number', "str", "str", "str", "str"],
                col_count=5,
                interactive=False,
            )
            review_btn.click(load_config_action, outputs=data_sheet)

        gen_button.click(gen_action,
                         inputs=[time_slider, widget_lora, widget_lyco, widget_embeddings, model_order,
                                 additional_prompt, angle,
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
                                 assign_hair_color, hair_accessories, neck_accessories, earrings, has_ending,
                                 hair_length, people_cnt, body_skin], outputs=results)
        send_button.click(send_action, inputs=results, outputs=t2i_text_box)
        if IS_PLUGIN:
            return [(ui_component, "RP", "RP")]
        else:
            return ui_component


def after_component(component, **kwargs):
    # Find the text2img textbox component
    global t2i_text_box
    if kwargs.get("elem_id") == "txt2img_prompt":  # postive prompt textbox
        t2i_text_box = component


if IS_PLUGIN:
    module_plugin1 = "modules.script_callbacks"
    script_module = importlib.import_module(module_plugin1)
    script_module.on_ui_tabs(on_ui_tabs)
    script_module.on_after_component(after_component)

else:
    app = on_ui_tabs()
    app.queue(max_size=10)
    app.launch(debug=True)
