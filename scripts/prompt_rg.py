import importlib
import json
import os
import re
from collections import defaultdict

import duckdb
import gradio as gr

from promptsModules.comfy_api import (load_comfy_ui_loras, load_comfyui_workflow, start_run_comfyui_workflow)
from promptsModules.db.datamodel import (
    DataBase,
    Image as DbImg,
    Tag,
    TrainTag,
    TrainImageTags, PromptRecord
)
from promptsModules.db.update_image_data import (update_image_data)
from promptsModules.train_tags import (handle_train_tag)

t2i_text_box = None
query_cursor: str = None
IS_PLUGIN = False

cache_search = defaultdict(int)
comfyUI_lora_list = []
comfyUI_curr_workflow: json = None


def get_model_input(com_value):
    arr = com_value.split(",")
    target_list = []
    if len(arr) > 0:
        target_list = [x.strip() for x in arr if x.strip()]
    return target_list


def get_prompts_from_folder(file_path, check_force, check_flux_flag_2=False):
    try:
        DataBase._initing = True
        img_count = DbImg.count(DataBase.get_conn())
        update_image_data([file_path], is_rebuild=check_force, is_flux=check_flux_flag_2)
        after_img_cnt = DbImg.count(DataBase.get_conn())
        return f"新增{after_img_cnt - img_count}条记录", f"共{after_img_cnt}条记录"
    finally:
        DataBase._initing = False


def create_tag_html(tag, height, suffix=None, border_color="#25BDCDAD", score=None, file_name=None):
    tag_html = ""
    if file_name is not None and file_name != "":
        tag_html += f"<div style='display: flex; align-items: center; justify-content: flex-start; padding: 0px 12px 0px 12px; margin: 0 12px 12px 0; font-size: 18px;'>"
        tag_html += f"<div style='font-style: italic; font-weight: bolder; color: #FF0035;'>{file_name}</div>"
        tag_html += "</div>"
    height_style = ""
    if height is not None:
        height_style = f"height: {height}px;"
    tag_html += (
        f"<div style='display: flex; align-items: center; justify-content: flex-start; padding: 0px 12px 0px 12px; margin: 0 12px 12px 0; border: 2px solid {border_color}; border-radius: 12px; {height_style} font-size: 16px;font-family: monospace;'>"
        f"<div style='white-space: pre-wrap;'>{tag}</div>"
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
                       check_search_adetailer_prompt, check_search_flux: bool, is_next=False):
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
    # print(cache_search_list)

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


def save_train_tag_action(train_source_path, train_alias, train_comments, check_handle_train_folder: bool,
                          check_is_flux_model: bool):
    """
    保存训练标签信息到数据库

    Args:
        train_source_path: 训练数据源路径
        train_alias: 训练别名
        train_comments: 训练注释
        check_handle_train_folder: 是否处理子文件夹
        check_is_flux_model: 是否为flux模型

    Returns:
        str: 处理结果信息
    """
    if check_handle_train_folder:
        # 检查是否为文件夹
        if not os.path.isdir(train_source_path):
            return f"{train_source_path}不是文件夹"

        # 处理所有子文件夹
        conn = DataBase.get_conn()
        processed_folders = []
        error_folders = []

        try:
            for file_name in os.listdir(train_source_path):
                file_path = os.path.join(train_source_path, file_name)
                if os.path.isdir(file_path):
                    result = handle_train_tag(file_path, "")

                    if result["success"]:
                        try:
                            if not check_is_flux_model:
                                train = TrainTag(
                                    result["alias_name"],
                                    json.dumps(result["tag_stats"], ensure_ascii=False),
                                    comments=train_comments,
                                    is_flux=0
                                )
                            else:
                                train = TrainTag(
                                    result["alias_name"],
                                    '{}',
                                    comments=train_comments,
                                    is_flux=1
                                )

                            train.save(conn)
                            TrainImageTags.saveTags(conn, train.id, result["files"])
                            processed_folders.append(file_name)
                        except Exception as e:
                            error_folders.append(f"{file_name}: {str(e)}")
                    else:
                        error_folders.append(f"{file_name}: {result['message']}")

            # 生成处理结果信息
            summary = f"处理完成，共处理{len(processed_folders)}个文件夹"
            if processed_folders:
                summary += f"\n成功处理的文件夹: {', '.join(processed_folders)}"
            if error_folders:
                summary += f"\n处理失败的文件夹: {'; '.join(error_folders)}"

            return summary

        finally:
            conn.close()
            DataBase.reConnect = True

    else:
        result = handle_train_tag(train_source_path, train_alias)
        if result["success"]:
            conn = DataBase.get_conn()
            try:
                if not check_is_flux_model:
                    json_str = json.dumps(result["tag_stats"], ensure_ascii=False)
                    resp = json_str
                    train = TrainTag(result["alias_name"], json_str, comments=train_comments, is_flux=0)
                else:
                    resp = "success"
                    train = TrainTag(result["alias_name"], '{}', comments=train_comments, is_flux=1)

                train.save(conn)
                TrainImageTags.saveTags(conn, train.id, result["files"])
                return resp
            finally:
                conn.close()
                DataBase.reConnect = True
        else:
            return "error: " + result["message"]


def update_train_tag_comments(train_model_dropdown, train_update_comments):
    conn = DataBase.get_conn()
    train = TrainTag(train_model_dropdown, tags_info="", comments=train_update_comments)
    train.update_comments(conn)
    gr.Info(f"更新{train_model_dropdown}完成")


def get_train_model_tags(train_input_model):
    conn = DataBase.get_conn()
    train = TrainTag.get(conn, train_input_model.strip())

    # dict: filename, content
    source_tag = TrainImageTags.getAllTags(conn, train.id)
    if train is None:
        return [], ""
    tags = json.loads(train.tags_info)
    # 将字典按照值的数值降序排序
    sorted_tags = sorted(tags.items(), key=lambda x: int(x[1]), reverse=True)

    # 将排序后的结果转换为列表
    results = [(key, str(value)) for key, value in sorted_tags]

    html_comments = (
        f"<div style='display: flex; color: aqua; font-size: 14px; font-weight: lighter; text-decoration: underline;'>"
        f"<div style='padding-right: 10px;'>{train.model_name}</div><div>{train.comments}</div>"
        f"</div>")

    table_html = "<table><tr><th>序列</th><th>prompt</th></tr>"
    for index, image_file_tag in enumerate(source_tag):
        table_html += (f"<tr>"
                       f"<td>{index}</td>"
                       f"<td>{create_tag_html(image_file_tag['content'].replace('<', '&lt;').replace('>', '&gt;'), height=None, file_name=image_file_tag['filename'])}</td>"
                       f"</tr>")
    table_html += "</table>"

    return results, html_comments, table_html


def load_train_models(is_flux=True):
    conn = DataBase.get_conn()
    train_models = TrainTag.get_all(conn, is_flux=is_flux)
    names = []
    for train in train_models:
        names.append(train.model_name)
    return names


def reload_train_models(check_flux_flag: bool):
    return gr.update(choices=load_train_models(is_flux=check_flux_flag))


def load_query_tips(check_search_flux=True):
    tags = Tag.get_all_model_tags(DataBase.get_conn(), check_search_flux)
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


def reload_query_tips(check_search_flux: bool):
    return gr.update(choices=load_query_tips(check_search_flux))


def update_lora_score_action(lora_list_dropdown, score_slider):
    Tag.update_tag_score(DataBase.get_conn(), lora_list_dropdown, score_slider)
    return inner_fetch_lora(DataBase.get_conn())


def add_prompt_action(prompt_text, prompt_memo, priority_slider, drop_type):
    conn = DataBase.get_conn()
    pr = PromptRecord(prompt_text, prompt_memo, priority_slider, p_type=drop_type)
    pr.save(conn)
    return "success"


def prompt_search_action(prompt_search_key, prompt_check_meta, drop_type_search):
    conn = DataBase.get_conn()
    prompt_search_result = PromptRecord.search(conn, prompt_search_key, is_meta=prompt_check_meta,
                                               p_type=drop_type_search)

    # 添加 CSS 样式来控制列宽
    table_html = """
    <style>
        .prompt-table {
            width: 100%;
            border-collapse: collapse;
        }
        .prompt-table th, .prompt-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        .prompt-table th {
            
        }
        .priority-col {
            width: 5%;
        }
        .prompt-col {
            width: 80%;
        }
        .type-col {
            width: 5%;
        }
        .comment-col {
            width: 10%;
        }
    </style>
    <table class="prompt-table">
        <tr>
            <th class="priority-col">Priority</th>
            <th class="prompt-col">Prompt</th>
            <th class="type-col">Type</th>
            <th class="comment-col">Comment</th>
        </tr>"""

    for index, prompt in enumerate(prompt_search_result):
        table_html += (f'<tr>'
                       f'<td class="priority-col">{prompt.priority}</td>'
                       f'<td class="prompt-col">{create_tag_html(prompt.prompt_text.replace("<", "&lt;").replace(">", "&gt;"), height=None)}</td>'
                       f'<td class="type-col">{prompt.p_type}</td>'
                       f'<td class="comment-col">{prompt.memo}</td>'
                       f'</tr>')

    table_html += "</table>"
    return table_html


# 获取当前脚本的上级目录
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 拼接文件路径
photoreal_portrait_file_path = os.path.join(current_dir, "flux-prompts-photoreal-portrait.parquet")
prompts_file_path = os.path.join(current_dir, "flux-prompts.parquet")

# 创建数据库连接
con = duckdb.connect()

# 使用计算出的路径创建视图
con.execute(f"CREATE TEMPORARY VIEW train_data_portrait AS SELECT * FROM '{photoreal_portrait_file_path}'")
con.execute(f"CREATE TEMPORARY VIEW train_data_prompt AS SELECT * FROM '{prompts_file_path}'")


def flux_prompt_search_action(flux_prompt_search, flux_dataset_drop):
    # SQL 查询，按 `prompt` 列分组，并计算每组的数量
    if flux_dataset_drop == 'k-mktr/improved-flux-prompts':
        query = "SELECT prompt FROM train_data_prompt WHERE prompt LIKE ? ORDER BY prompt ASC LIMIT 512"

    else:
        query = "SELECT prompt FROM train_data_portrait WHERE prompt LIKE ? ORDER BY prompt ASC LIMIT 512"

    # 执行查询并返回结果
    df = con.execute(query, (f"%{flux_prompt_search}%",)).fetchdf()

    # 添加 CSS 样式来控制列宽
    table_html = """
    <style>
        .flux-prompt-table {
            width: 100%;
            border-collapse: collapse;
        }
        .flux-prompt-table th, .flux-prompt-table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
    </style>
    <table class="flux-prompt-table">
        <tr>
            <th>Prompt</th>
        </tr>"""

    for index, row in df.iterrows():
        table_html += f'<tr><td>{create_tag_html(row["prompt"].replace("<", "&lt;").replace(">", "&gt;"), height=None)}</td></tr>'

    table_html += "</table>"
    return table_html


##### Comfy UI #####

def load_comfyui_loras(lora_path):
    global comfyUI_lora_list
    comfyUI_lora_list = load_comfy_ui_loras(lora_path)
    gr.Info("load comfyUI loras success")


def load_comfyui_wf(workflow_path):
    global comfyUI_curr_workflow
    comfyUI_curr_workflow = load_comfyui_workflow(workflow_path)
    gr.Info("load comfyUI workflow success")


def refresh_comfyui_loras():
    return gr.update(choices=comfyUI_lora_list), gr.update(choices=comfyUI_lora_list)


def start_run_comfyui_wf(prompt, gen_num, lora_first, lora_first_strength, enable_second, lora_second,
                         lora_second_strength, lora_second_clip_strength):
    global comfyUI_curr_workflow
    print(comfyUI_curr_workflow)
    return start_run_comfyui_workflow(comfyUI_curr_workflow, prompt, gen_num, lora_first, lora_first_strength,
                                      enable_second, lora_second, lora_second_strength, lora_second_clip_strength)


######### UI #########
def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as ui_component:
        with gr.Tab('🔍'):
            with gr.Column():
                with gr.Row(variant="panel"):
                    key_dropdown = gr.Dropdown(choices=load_query_tips(), allow_custom_value=True, interactive=True,
                                               type="value", label="🔍", show_label=True)
                with gr.Row():
                    sort_drop = gr.Dropdown(["数量", "时间"], value="数量", type="index", label="排序方式",
                                            interactive=True)
                    check_search_flux = gr.Checkbox(True, label="flux模型", info="是否是flux模型", interactive=True)
                    check_res_show = gr.Checkbox(True, label="分辨率", info="是否显示分辨率", interactive=True)
                    check_adetailer_show = gr.Checkbox(True, label="adetailer", info="显示adetailer提示词",
                                                       interactive=True)
                    check_search_adetailer_prompt = gr.Checkbox(False, label="adetailer prompt", info="搜索adetailer",
                                                                interactive=True)
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
                next_query_button.click(next_search_action,
                                        inputs=[key_dropdown, limit_slider, sort_drop, check_res_show,
                                                check_adetailer_show,
                                                check_search_adetailer_prompt, check_search_flux],
                                        outputs=[search_info, html_table, search_history])
                refresh_dp_button.click(reload_query_tips, inputs=[check_search_flux], outputs=key_dropdown)
        with gr.Tab("Model"):
            with gr.Tab("Tags"):
                with gr.Row():
                    check_flux_flag = gr.Checkbox(True, label="flux模型", info="是否是flux模型", interactive=True)
                with gr.Row(equal_height=False):
                    train_input_model = gr.Dropdown(choices=load_train_models(), allow_custom_value=True,
                                                    interactive=True, type="value", show_label=False)
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
            with gr.Tab("Lora"):
                with gr.Column():
                    with gr.Row(equal_height=False, variant="panel"):
                        fetch_lora_btn = gr.Button("查询lora", variant='primary')
                        delete_lora_input = gr.Textbox("", show_label=False)
                        delete_lora_btn = gr.Button("删除lora", variant='secondary')
                    with gr.Row(equal_height=False):
                        lora_list_dropdown = gr.Dropdown(choices=load_lora_list(), allow_custom_value=True,
                                                         interactive=True, type="value", show_label=False)
                        score_slider = gr.Slider(0, 1, value=0, label="分数", step=0.05, interactive=True)
                        score_btn = gr.Button("更新", variant='primary')
                    html_loras = gr.HTML("", label=None, show_label=False, interactive=False)
                    fetch_lora_btn.click(fetch_lora_action, outputs=html_loras)
                    delete_lora_btn.click(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    delete_lora_input.submit(delete_lora_action, inputs=[delete_lora_input], outputs=html_loras)
                    score_btn.click(update_lora_score_action, inputs=[lora_list_dropdown, score_slider],
                                    outputs=html_loras)
            with gr.Tab("Lyco"):
                fetch_lyco_btn = gr.Button("查询lyco", variant='primary')
                html_lyco = gr.HTML("", label=None, show_label=False, interactive=False)
                fetch_lyco_btn.click(fetch_lyco_action, outputs=html_lyco)

        with gr.Tab('Get Prompt'):
            with gr.Tab("Images"):
                with gr.Column():
                    with gr.Row():
                        file_path = gr.Textbox("/notebooks/", label="文件路径", lines=1,
                                               show_copy_button=True, interactive=True)
                        check_force = gr.Checkbox(label='是否强制', show_label=True, info='')
                        check_flux_flag_2 = gr.Checkbox(True, label="flux模型", info="是否是flux模型",
                                                        interactive=True)
                    extract_btn = gr.Button("提取prompt", variant="primary")
                    with gr.Row():
                        text2 = gr.Textbox(label="状态")
                        img_cnt = gr.Textbox(label="图片数量")
                    extract_btn.click(get_prompts_from_folder, inputs=[file_path, check_force, check_flux_flag_2],
                                      outputs=[text2, img_cnt])
                    file_path.submit(get_prompts_from_folder, inputs=[file_path, check_force, check_flux_flag_2],
                                     outputs=[text2, img_cnt])
            with gr.Tab("Train Source"):
                with gr.Column():
                    with gr.Row():
                        train_source_path = gr.Textbox("/notebooks/", label="训练的tag文件路径", lines=1,
                                                       show_copy_button=True, interactive=True)
                        train_alias = gr.Textbox(None, label="别名", lines=1, interactive=True)
                        train_comments = gr.Textbox(None, label="添加备注，描述模型详情", lines=2, interactive=True)
                        check_is_flux_model = gr.Checkbox(True, label="是否flux模型",
                                                          info="是否是flux模型，不处理tag分组", interactive=True)
                        check_handle_train_folder = gr.Checkbox(False, label="是否处理文件夹",
                                                                info="勾选则处理文件夹下所有子目录", interactive=True)
                    train_result = gr.Textbox("", label="汇总结果", lines=1, show_copy_button=True, interactive=False)
                    with gr.Row():
                        train_tag_btn = gr.Button("汇总tag", variant="primary")
                    train_tag_btn.click(save_train_tag_action, inputs=[train_source_path, train_alias, train_comments,
                                                                       check_handle_train_folder, check_is_flux_model],
                                        outputs=[train_result])
                    train_source_path.submit(save_train_tag_action,
                                             inputs=[train_source_path, train_alias, train_comments,
                                                     check_handle_train_folder, check_is_flux_model],
                                             outputs=[train_result])

                with gr.Column():
                    with gr.Row(equal_height=False):
                        train_model_dropdown = gr.Dropdown(choices=load_train_models(), interactive=True,
                                                           allow_custom_value=True, show_label=False)
                        train_update_comments = gr.Textbox(None, label="添加备注，描述模型详情", lines=2,
                                                           interactive=True)
                    train_update_btn = gr.Button("更新备注", variant="primary")
                    train_update_btn.click(update_train_tag_comments,
                                           inputs=[train_model_dropdown, train_update_comments])

        with gr.Tab('Prompt Record'):
            with gr.Tab("🔍"):
                prompt_search_key = gr.Textbox("", label="搜索", lines=1, interactive=True)
                with gr.Row():
                    prompt_check_meta = gr.Checkbox(False, label="meta", info="是否搜索meta", interactive=True)
                    drop_type_search = gr.Dropdown(["人物", "背景", "姿势", "视角", "光影", "穿搭", "其他", None],
                                                   value=None,
                                                   type="value", label="类型", interactive=True)
                prompt_search_btn = gr.Button("搜索", variant="primary")
                prompt_search_table = gr.HTML("", label=None, show_label=False, interactive=False)
                prompt_search_key.submit(prompt_search_action,
                                         inputs=[prompt_search_key, prompt_check_meta, drop_type_search],
                                         outputs=[prompt_search_table])
                prompt_search_btn.click(prompt_search_action,
                                        inputs=[prompt_search_key, prompt_check_meta, drop_type_search],
                                        outputs=[prompt_search_table])
            with gr.Tab("📜"):
                with gr.Row():
                    prompt_text = gr.Textbox(None, label="prompt", lines=2, interactive=True, min_width=600,
                                             show_copy_button=True)
                    prompt_memo = gr.Textbox(None, label="备注", lines=1, interactive=True)
                with gr.Row():
                    drop_type = gr.Dropdown(["人物", "背景", "姿势", "视角", "光影", "穿搭", "其他"], value="其他",
                                            type="value", label="类型", interactive=True)
                    priority_slider = gr.Slider(1, 500, value=1, label="优先级", step=5, interactive=True)
                add_prompt_btn = gr.Button("添加", variant="primary")
                add_prompt_result = gr.Textbox("", label="添加结果", lines=1, interactive=False)
                add_prompt_btn.click(add_prompt_action, inputs=[prompt_text, prompt_memo, priority_slider, drop_type],
                                     outputs=add_prompt_result)

            with gr.Tab("flux-prompts-dataset"):
                with gr.Row():
                    flux_prompt_search = gr.Textbox("", label="搜索", lines=1, interactive=True)
                    flux_dataset_drop = gr.Dropdown(
                        ['k-mktr/improved-flux-prompts', 'k-mktr/improved-flux-prompts-photoreal-portrait'],
                        value='k-mktr/improved-flux-prompts', type="value", label="数据集", interactive=True)
                flux_prompt_search_btn = gr.Button("搜索", variant="primary")
                flux_search_table = gr.HTML("", label=None, show_label=False, interactive=False)
                flux_prompt_search_btn.click(flux_prompt_search_action, inputs=[flux_prompt_search, flux_dataset_drop],
                                             outputs=[flux_search_table])
                flux_prompt_search.submit(flux_prompt_search_action, inputs=[flux_prompt_search, flux_dataset_drop],
                                          outputs=[flux_search_table])

        with gr.Tab("ComfyUI Api"):
            with gr.Tab("flux dual lora"):
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Column(variant="compact"):
                            dropdown_lora_first = gr.Dropdown(choices=comfyUI_lora_list, interactive=True,
                                                              label="select lora")
                            slider_lora_first = gr.Slider(0, 1, value=1, label="model strength", step=0.1,
                                                          interactive=True)
                        checkbox_enable_second = gr.Checkbox(True, label="enable second lora", interactive=True)
                        with gr.Column():
                            dropdown_lora_second = gr.Dropdown(choices=comfyUI_lora_list, interactive=True,
                                                               label="select lora")
                            slider_lora_second = gr.Slider(0, 1, value=1, label="model strength", step=0.1,
                                                           interactive=True)
                            slider_lora_second_clip = gr.Slider(0, 1, value=1, label="clip strength", step=0.1,
                                                                interactive=True)
                        btn_refresh_comfyui_lora = gr.Button("刷新lora", variant='secondary')
                        btn_refresh_comfyui_lora.click(refresh_comfyui_loras,
                                                       outputs=[dropdown_lora_first, dropdown_lora_second])
                    with gr.Column(scale=2):
                        input_comfyui_prompt = gr.Textbox("", label="prompt", lines=14, interactive=True)
                        slider_gen_num = gr.Slider(1, 512, value=2, label="gen num", step=1, interactive=True)
                        btn_gen_comfyui = gr.Button("gen comfyui", variant='primary')
                        info_run_comfyui = gr.Textbox("", label="run result", lines=1, interactive=False)
                        btn_gen_comfyui.click(start_run_comfyui_wf,
                                              inputs=[input_comfyui_prompt, slider_gen_num, dropdown_lora_first,
                                                      slider_lora_first, checkbox_enable_second, dropdown_lora_second,
                                                      slider_lora_second, slider_lora_second_clip],
                                              outputs=[info_run_comfyui])

            with gr.Tab("load"):
                with gr.Column():
                    input_lora_path = gr.Textbox("/Users/hb/Downloads/notebook/", label="lora folder path", lines=1,
                                                 interactive=True)
                    btn_lora_load = gr.Button("load lora", variant='primary')
                    btn_lora_load.click(load_comfyui_loras, inputs=[input_lora_path])
                with gr.Column():
                    workflow_path = gr.Textbox("/notebooks/", label="workflow path", lines=1, interactive=True)
                    btn_workflow_load = gr.Button("load workflow", variant='primary')
                    btn_workflow_load.click(load_comfyui_wf, inputs=[workflow_path])
            with gr.Tab("Basic"):
                pass

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
