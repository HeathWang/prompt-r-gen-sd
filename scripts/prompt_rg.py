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
# The longest method I've ever written
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


def get_prompts_from_folder(file_path, check_force):
    try:
        DataBase._initing = True
        img_count = DbImg.count(DataBase.get_conn())
        update_image_data([file_path], is_rebuild=check_force)
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
        f"<div style='display: flex; align-items: center; justify-content: center; padding: 0px 12px 0px 12px; margin: 0 12px 12px 0; border: 2px solid {border_color}; border-radius: 12px; {height_style} font-size: 18px;'>"
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
                  check_search_adetailer_prompt=False):
    return base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                              check_search_adetailer_prompt)


def next_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                       check_search_adetailer_prompt=False):
    return base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                              check_search_adetailer_prompt, is_next=True)


def base_search_action(key_input, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                       check_search_adetailer_prompt, is_next=False):
    global query_cursor
    global cache_search
    cache_search[key_input] += 1

    conn = DataBase.get_conn()
    imgs, next_cursor = DbImg.find_by_substring(
        conn=conn,
        substring=key_input.strip(),
        cursor=is_next and query_cursor or None,
        limit=limit_slider,
        regexp=check_search_adetailer_prompt and r'ADetailer prompt: "([^"]+)"' or None,
        from_exif=check_search_adetailer_prompt,
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
        raise gr.Error("Please enter the lora")
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
    # Create HTML containing buttons
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body>
    
    <h2>OpenInfinite image browsing</h2>
    
    <button style='width:100%;' onclick="window.location.href='/infinite_image_browsing'">I point</button>
    
    </body>
    </html>
    """
    return html_code


def save_train_tag_action(train_source_path, train_alias, train_comments, check_handle_train_folder:bool):
    if check_handle_train_folder:
        # check if folder
        if not os.path.isdir(train_source_path):
            return f"{train_source_path}Not a folder"
        # get all sub folder
        conn = DataBase.get_conn()
        count = 0

        for file_name in os.listdir(train_source_path):
            file_path = os.path.join(train_source_path, file_name)
            if os.path.isdir(file_path):
                json_str, alias_name = handle_train_tag(file_path, "")

                train = TrainTag(alias_name, json_str, comments=train_comments)
                train.save(conn)
                count += 1

        conn.close()
        DataBase.reConnect = True
return f"Processing completed, total {count} folders"
    else:
        json_str, alias_name = handle_train_tag(train_source_path, train_alias)
        conn = DataBase.get_conn()
        train = TrainTag(alias_name, json_str, comments=train_comments)
        train.save(conn)
        conn.close()
        DataBase.reConnect = True
        return json_str

def update_train_tag_comments(train_model_dropdown, train_update_comments):
    conn = DataBase.get_conn()
    train = TrainTag(train_model_dropdown, tags_info="", comments=train_update_comments)
    train.update_comments(conn)
    gr.Info(f"Update {train_model_dropdown} completed")


def get_train_model_tags(train_input_model):
    conn = DataBase.get_conn()
    train = TrainTag.get(conn, train_input_model.strip())
    if train is None:
        return [], ""
    tags = json.loads(train.tags_info)
    # # Sort the dictionary in descending order of values
    sorted_tags = sorted(tags.items(), key=lambda x: int(x[1]), reverse=True)

    # Convert sorted results to list
    results = [(key, str(value)) for key, value in sorted_tags]

    html_comments = (f"<div style='display: flex; color: aqua; font-size: 14px; font-weight: lighter; text-decoration: underline;'>"
                     f"<div style='padding-right: 10px;'>{train.model_name}</div><div>{train.comments}</div>"
                     f"</div>")
    return results, html_comments

def load_train_models():
    conn = DataBase.get_conn()
    train_models = TrainTag.get_all(conn)
    names = []
    for train in train_models:
        names.append(train.model_name)
    return names

def load_query_tips():
    tags = Tag.get_all_model_tags(DataBase.get_conn())
    tips = []
    for tag in tags:
        tips.append(tag.name)
    return tips

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
                        sort_drop = gr.Dropdown(["Quantity", "Time"], value="Quantity", type="index", label="Sort method",
                                            interactive=True)
                    check_res_show = gr.Checkbox(True, label="Resolution", info="Whether to display resolution", interactive=True)
                    check_adetailer_show = gr.Checkbox(True, label="adetailer", info="Show adetailer prompt word",
                                                       interactive=True)
                    check_search_adetailer_prompt = gr.Checkbox(False, label="adetailer prompt", info="Search adetailer",
                                                                interactive=True)
                    limit_slider = gr.Slider(64, 5120, value=512, label="Search limit", step=4, min_width=600,
                                             interactive=True)
                search_history = gr.HighlightedText(show_label=False)
                with gr.Row():
                    search_button = gr.Button("search", variant='primary')
                    next_query_button = gr.Button("Next page", size="sm", variant='secondary')
                    search_info = gr.Textbox("", show_label=False, interactive=False)
                html_table = gr.HTML("", label=None, show_label=False, interactive=False)

                search_button.click(search_action,
                                    inputs=[key_dropdown, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                                            check_search_adetailer_prompt],
                                    outputs=[search_info, html_table, search_history])
                key_dropdown.select(search_action,
                                 inputs=[key_dropdown, limit_slider, sort_drop, check_res_show, check_adetailer_show,
                                         check_search_adetailer_prompt],
                                 outputs=[search_info, html_table, search_history])
                next_query_button.click(next_search_action, inputs=[key_dropdown, limit_slider, sort_drop, check_res_show,
                                                                    check_adetailer_show,
                                                                    check_search_adetailer_prompt],
                                        outputs=[search_info, html_table, search_history])
        with gr.Tab("Model"):
            with gr.Tab("Lora"):
                with gr.Column():
                    with gr.Row(equal_height=False, variant="panel"):
                        fetch_lora_btn = gr.Button("Query lora", variant='primary')
                        delete_lora_input = gr.Textbox("", show_label=False)
                        delete_lora_btn = gr.Button("Delete lora", variant='secondary')
                    with gr.Row(equal_height=False):
                        lora_list_dropdown = gr.Dropdown(choices=load_lora_list(), allow_custom_value=True, interactive=True, type="value", show_label=False)
                        score_slider = gr.Slider(0, 1, value=0, label="Fraction", step=0.05, interactive=True)
                        score_btn = gr.Button("renew", variant='primary')
                    html_loras = gr.HTML("", label=None, show_label=False, interactive=False)
                    fetch_lora_btn.click(fetch_lora_action, outputs=html_loras)
                    delete_lora_btn.click(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    delete_lora_input.submit(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    score_btn.click(update_lora_score_action, inputs=[lora_list_dropdown, score_slider], outputs=html_loras)
            with gr.Tab("Lyco"):
                fetch_lyco_btn = gr.Button("Query lyco", variant='primary')
                html_lyco = gr.HTML("", label=None, show_label=False, interactive=False)
                fetch_lyco_btn.click(fetch_lyco_action, outputs=html_lyco)
            with gr.Tab("Tags"):
                with gr.Row(equal_height=False):
                    train_input_model = gr.Dropdown(choices=load_train_models(), allow_custom_value=True, interactive=True, type="value", show_label=False)
                    fetch_train_info_btn = gr.Button("Query train tags", variant='primary')
                train_tags_comments = gr.HTML("", label=None, show_label=False, interactive=False)
                tags_highlighted = gr.HighlightedText(show_label=False)
                train_input_model.select(get_train_model_tags, inputs=[train_input_model],
                                         outputs=[tags_highlighted, train_tags_comments])
                fetch_train_info_btn.click(get_train_model_tags, inputs=[train_input_model],
                                           outputs=[tags_highlighted, train_tags_comments])
        with gr.Tab('ExtractPrompt'):
            with gr.Tab("Images"):
                with gr.Column():
                    with gr.Row():
                        file_path = gr.Textbox("/notebooks/resource/outputs/20231225", label="file path", lines=1,
                                               show_copy_button=True, interactive=True)
                        check_force = gr.Checkbox(label='Is it mandatory?', show_label=True, info='')
                    extract_btn = gr.Button("Extract prompt", variant="primary")
                    with gr.Row():
                        text2 = gr.Textbox(label="state")
                        img_cnt = gr.Textbox(label="Number of pictures")
                    extract_btn.click(get_prompts_from_folder, inputs=[file_path, check_force], outputs=[text2, img_cnt])
                    file_path.submit(get_prompts_from_folder, inputs=[file_path, check_force], outputs=[text2, img_cnt])
            with gr.Tab("Train Source"):
                with gr.Column():
                    with gr.Row():
                        train_source_path = gr.Textbox("/notebooks/", label="Training tag file path", lines=1,
                                                       show_copy_button=True, interactive=True)
                        train_alias = gr.Textbox(None, label="Alias", lines=1, interactive=True)
                        train_comments = gr.Textbox(None, label="Add notes to describe model details", lines=2, interactive=True)
                        check_handle_train_folder = gr.Checkbox(False, label="Whether to process folders",
                                                                info="If checked, all subdirectories under the folder will be processed.", interactive=True)
                    train_result = gr.Textbox("", label="Summary results", lines=1, show_copy_button=True, interactive=False)
                    with gr.Row():
                        train_tag_btn = gr.Button("Summary tag", variant="primary")
                    train_tag_btn.click(save_train_tag_action, inputs=[train_source_path, train_alias, train_comments, check_handle_train_folder],
                                        outputs=[train_result])
                    train_source_path.submit(save_train_tag_action, inputs=[train_source_path, train_alias, train_comments, check_handle_train_folder],
                                             outputs=[train_result])

                with gr.Column():
                    with gr.Row(equal_height=False):
                        train_model_dropdown = gr.Dropdown(choices=load_train_models(), interactive=True, allow_custom_value=True, show_label=False)
                        train_update_comments = gr.Textbox(None, label="Add notes to describe model details", lines=2, interactive=True)
                    train_update_btn = gr.Button("Update notes", variant="primary")
                    train_update_btn.click(update_train_tag_comments, inputs=[train_model_dropdown, train_update_comments])


        with gr.Tab("Generate Prompt"):
            with gr.Row():
                with gr.Column(scale=3):
                    gr.Markdown("Please modify the following configuration")

                    with gr.Box():
                        with gr.Row():
                            time_slider = gr.Slider(1, 6, value=1, label="Randomly generate numbers", step=1, interactive=True)
                    with gr.Accordion("perspective, location, action", open=False):
                        with gr.Row():
                            angle = gr.Checkbox(False, label="perspective", info="front, side, back...")
                            body_framing = gr.Checkbox(False, label="body frame", info="portrait, half body, full body...")
                            location = gr.Checkbox(False, label="Place", info="random location")
                            pose_type = gr.Dropdown(['Basic', 'Whole body', 'NULL'], value='NULL', type="index",
                                                    label="action type",
                                                    interactive=True,
                                                    info="Character movements, standing, sitting, lying...")
                            dynamic_mode = gr.Checkbox(False, label="dynamic mode",
                                                       info="use dynamic pose, angle，Need to check the corresponding configuration")
                    with gr.Accordion("Character clothing", open=False):
                        with gr.Column():
                            with gr.Row():
                                breasts_size = gr.Dropdown(["medium", "large", "huge", "gigantic", "NULL"],
                                                           value="NULL",
                                                            label="Breast size description", info="increase in sequence= =#", interactive=True)
                                body_wear = gr.Dropdown(
                                    ["dress", "UNIFORM", "BODYSUIT", "TRADITIONAL",
                                    "Top and bottom matching (such as top body shirt and bottom skirt)", "Above randomly", "Empty NULL"], value="Empty NULL",
                                    type="index", label="clothing", info="", interactive=True)
                                top_wear = gr.Dropdown(
                                    ["SHIRTS", "COAT", "SWEATER", "OTHERS", "RANDOM above"],
                                    value="SHIRTS", type="index", label="upper body clothing",
                                    info="Select top and bottom matching (such as a top body shirt and a bottom skirt), this configuration will take effect", interactive=True)
                                bottom_wear = gr.Dropdown(["PANTS", "SKIRT", "SHORTS", "RANDOM above"],
                                                            value="SKIRT", type="index", label="Lower clothing",
                                                            info="Select top and bottom matching (such as a top body shirt and a bottom skirt) and this configuration will take effect",
                                                          interactive=True)
                            with gr.Row():
                                leg_wear = gr.Dropdown(
                                   ["SOCKS", "Calf socks KNEEHIGHS", "Over the knee socks OVERKNEEHIGHS", "Thigh socks THIGHHIGHS",
                                      "PANTYHOSE",
                                      "Bare legs BARE", "Empty NULL", "Above random RANDOM"], value="Empty NULL", type="index",
                                     label="socks",
                                    interactive=True)
                                panties = gr.Checkbox(False, label="Pants", info="If checked, a type of panties will be randomly generated")
                                shoes_type = gr.Dropdown(
                                   ["BOOTS", "HIGHHEELS", "SANDALS", "SLIPPERS", "BARE",
                                      "Empty NULL"],
                                     value="NULL", type="index", label="Shoes", info="", interactive=True)
                            with gr.Row():
                                body_with = gr.Checkbox(False, label="body wrapping", info="Wrap something around, bondage, ribbon, chain")
                                 body_status = gr.Checkbox(False, label="body status", info="wet, sweaty...")
                                 body_desc = gr.Checkbox(False, label="Body description", info="Perfect figure, slim body...")
                                 cloth_trim = gr.Checkbox(False, label="Clothes Decoration", info="lace, ribbons, gold, flowers, etc...")
                    with gr.Accordion("Character description", open=False):
                        with gr.Row():
                            profession = gr.Checkbox(False, label="Profession")
                            people_cnt = gr.Slider(0, 8, value=1, label="Number of characters", step=1, interactive=True)
                        with gr.Row():
                            hair_length = gr.Checkbox(True, label="hair length")
                            hair_color = gr.Checkbox(True, label="Hair color", interactive=True)
                            add_hair_style = gr.Checkbox(False, label="hair style")
                            enable_eye_color = gr.Checkbox(True, label="eye color")
                        with gr.Row():
                            hair_accessories = gr.Checkbox(True, label="headwear")
                             neck_accessories = gr.Checkbox(True, label="neck accessories")
                             earrings = gr.Checkbox(True, label="earrings")
                             body_skin = gr.Checkbox(False, label="skin")
                        with gr.Row():
                            face_expression = gr.Dropdown(
                                 ["EMOTIONS", "SEXUAL", "SMILE", "SMUG", "Random of the above", "NULL"],
                                 value="SMILE",
                                 type="index", label="expression", interactive=True)
                             add_girl_beautyful = gr.Checkbox(False, label="Short affix to describe a girl", info="")
                             has_girl_desc = gr.Checkbox(False, label="Long affix to describe girls", info="")

                    with gr.Accordion("NSFW configuration", open=False):
                        with gr.Box():
                            with gr.Row():
                                nsfw_type = gr.Dropdown(["NUDE", "SEXUAL", "Regular NOTNSFW"], value="Regular NOTNSFW",
                                                         type="index",
                                                         label="NSFW level",
                                                         info="Please make sure you know what you are doing! If you choose the unconventional type, the character clothing settings above will not take effect",
                                                         interactive=True)
                                 is_nsfw = gr.Checkbox(False, label="Whether to add the nfsw affix")
                                 is_uncensored = gr.Checkbox(False, label="Whether to add the uncensored affix")
                                 is_simple_nude = gr.Checkbox(False, label="Is it simple nude mode", info="Nude mode is in effect")
                                 nude_strong = gr.Checkbox(False, label="Whether to strengthen nude mode", info="Nude mode takes effect")
                            with gr.Row():
                                sexual_list_random_index_times = gr.Slider(0, 5, value=0, step=1,
                                                                            label="Sexy affix random number",
                                                                            interactive=True)
                                 nude_list_random_index_times = gr.Slider(0, 9, value=0, step=1, label="Nude affix random number",
                                                                          interactive=True)
                    with gr.Accordion("Lora Loha embedding control", open=False):
                        gr.Markdown(
                            """
                            Regarding the detailed configuration and use of lora/loha/embedding: [Click here to view](https://github.com/HeathWang/prompt-r-gen-sd#loralohaembedding%E6%8E%A7%E5%88%B6%E8% AF%B4%E6%98%8E)
                            """
                        )
                        with gr.Box():
                            with gr.Row():
                                widget_lora = gr.Textbox("", label="Lora【x】",
                                                          info="The format is as follows: 101, 101:0.6, Louis:0.65",
                                                          elem_id="rp_widget_lora")
                                 widget_lyco = gr.Textbox("", label="lyco【y】",
                                                          info="The format is as follows: 101, 101:0.6, add details: 1",
                                                          elem_id="rp_widget_lyco")
                             with gr.Row():
                                 widget_embeddings = gr.Textbox("", label="embeddings【z】",
                                                                info="The format is as follows: 100, ul:0.6",
                                                                elem_id="rp_widget_embeddings")
                                 model_order = gr.Textbox("xyz", label="lora, lyco, embed order",
                                                          info="The default is xyz order, that is, in the order of lora, lyco, emb")
                    with gr.Accordion("other", open=False):
                        with gr.Row():
                            has_starting = gr.Checkbox(True, label="Whether to use starting style", info="best quality, absurdres,")
                             has_ending = gr.Checkbox(True, label="Add details", info="jewelry, ultra-detailed, 8k,")
                             is_realistic = gr.Checkbox(False, label="Whether to add real affixes",
                                                        info="realistic, photorealistic")
                             add_colors = gr.Checkbox(False, label="Whether to add colorful affixes")
                         with gr.Row():
                             enable_day_weather = gr.Checkbox(False, label="Whether to add weather information")
                             enable_light_effect = gr.Checkbox(True, label="Whether to add light effects")
                             enable_image_tech = gr.Checkbox(False, label="Whether to enable image technology, such as blur")
                        with gr.Row():
                            accessories_random_tims = gr.Slider(0, 8, value=0, step=1, label="Random number of accessories",
                                                                 interactive=True,
                                                                 info="rings, garters, etc.")
                             object_random_times = gr.Slider(0, 8, value=0, step=1, label="item random number",
                                                             info="Flowers, ice and fire elements, etc.",
                                                             interactive=True)
                             suffix_words_random_times = gr.Slider(0, 10, value=0, step=1, label="Adjective affix random number",
                                                                   info="Some affixes related to fantasy and beauty",
                                                                   interactive=True)

                    with gr.Accordion("Precise controls", open=False):
                        with gr.Box():
                            with gr.Row():
                                assign_angle = gr.Textbox("null", label="Specify perspective")
                                 assign_body_framing = gr.Textbox("null", label="Specify body frame")
                                 assign_place = gr.Textbox("null", label="Specify location")
                             with gr.Row():
                                 assign_pose = gr.Textbox("null", label="Specify character action")
                                 assign_job = gr.Textbox("null", label="Specify role")
                                 assigin_expression = gr.Textbox("null", label="Specified character expression")
                             with gr.Row():
                                 assign_clothes = gr.Textbox("", label="Specify clothes")
                                 assign_leg_wear = gr.Textbox("", label="Specify sock type")
                                 assign_shoes = gr.Textbox("", label="Specify shoe type")
                             with gr.Row():
                                 assign_leg_wear_color = gr.Textbox("", label="Specify sock color")
                                 assign_shoes_color = gr.Textbox("", label="Specify shoe color")
                                 assign_hair_color = gr.Textbox("", label="Specify hair color")

                    with gr.Box():
                        gr.Markdown("Manual entry")
                        with gr.Row():
                            additional_prompt = gr.Textbox("", label="additional prompts")
                with gr.Column(scale=1):
                    gr.Markdown("prompt output：")
                    results = gr.Textbox("", label="Generated prompt", lines=20, show_copy_button=True, interactive=True)
                    with gr.Row():
                        gen_button = gr.Button("Generate prompt")
                         send_button = gr.Button("Send to Vincent Picture")
        with gr.Tab("other"):
            with gr.Column():
                gr.HTML(open_sd_image_broswer_html(), label=None, show_label=False, interactive=True)
        with gr.Tab("View configuration"):
             review_btn = gr.Button("Load excel configuration")
             data_sheet = gr.DataFrame(
                 headers=["sequence", "id", "type", "model name", "description"],
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
