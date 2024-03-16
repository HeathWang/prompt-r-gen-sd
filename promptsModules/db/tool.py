from datetime import datetime
import os
import platform
import re
import tempfile
import imghdr
import subprocess
from typing import Dict, List
import sys
import piexif
import piexif.helper
import json
import zipfile
from PIL import Image

sd_img_dirs = [
    "outdir_txt2img_samples",
    "outdir_img2img_samples",
    "outdir_save",
    "outdir_extras_samples",
    "outdir_grids",
    "outdir_img2img_grids",
    "outdir_samples",
    "outdir_txt2img_grids",
]


is_dev = os.getenv("APP_ENV") == "dev"
is_nuitka = "__compiled__" in globals()
cwd = os.getcwd() if is_nuitka else os.path.normpath(os.path.join(__file__, "../../../"))
is_win = platform.system().lower().find("windows") != -1



def normalize_paths(paths: List[str], base = cwd):
    """
    Normalize a list of paths, ensuring that each path is an absolute path with no redundant components.

    Args:
        paths (List[str]): A list of paths to be normalized.

    Returns:
        List[str]: A list of normalized paths.
    """
    res: List[str] = []
    for path in paths:
        # Skip empty or blank paths
        if not path or len(path.strip()) == 0:
            continue
        # If the path is already an absolute path, use it as is
        if os.path.isabs(path):
            abs_path = path
        # Otherwise, make the path absolute by joining it with the current working directory
        else:
            abs_path = os.path.join(base, path)
        # If the absolute path exists, add it to the result after normalizing it
        if os.path.exists(abs_path):
            res.append(os.path.normpath(abs_path))
    return res

def to_abs_path(path):
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    return os.path.normpath(path)


def get_valid_img_dirs(
    conf,
    keys=sd_img_dirs,
):
    # Get the configuration item
    paths = [conf.get(key) for key in keys]

    # Determine whether the path is valid and converted to the absolute path
    abs_paths = []
    for path in paths:
        if not path or len(path.strip()) == 0:
            continue
        if os.path.isabs(path):  # Already absolute path
            abs_path = path
        else:  # Turn to absolute path
            abs_path = os.path.join(os.getcwd(), path)
        if os.path.exists(abs_path):  # Determine whether the path exists
            abs_paths.append(os.path.normpath(abs_path))

    return abs_paths


def human_readable_size(size_bytes):
    """
    Converts bytes to a human-readable format.
    """
    # define the size units
    units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    # calculate the logarithm of the input value with base 1024
    size = int(size_bytes)
    if size == 0:
        return "0B"
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    # round the result to two decimal points and return as a string
    return "{:.2f} {}".format(size, units[i])


def get_windows_drives():
    drives = []
    for drive in range(ord("A"), ord("Z") + 1):
        drive_name = chr(drive) + ":/"
        if os.path.exists(drive_name):
            drives.append(drive_name)
    return drives


pattern = re.compile(r"(\d+\.?\d*)([KMGT]?B)", re.IGNORECASE)


def convert_to_bytes(file_size_str):
    match = re.match(pattern, file_size_str)
    if match:
        size_str, unit_str = match.groups()
        size = float(size_str)
        unit = unit_str.upper()
        if unit == "KB":
            size *= 1024
        elif unit == "MB":
            size *= 1024**2
        elif unit == "GB":
            size *= 1024**3
        elif unit == "TB":
            size *= 1024**4
        return int(size)
    else:
        raise ValueError(f"Invalid file size string '{file_size_str}'")


def is_valid_image_path(path):
    """
    Determine whether the given path is an image file
    """
    abs_path = os.path.abspath(path)  # Turn to absolute path
    if not os.path.exists(abs_path):  # Determine whether the path exists
        return False
    if not os.path.isfile(abs_path):  # Determine whether it is a file
        return False
    if not imghdr.what(abs_path):  # Determine whether it is image file
        return False
    return True



def create_zip_file(file_paths: List[str], zip_file_name: str):
    """
    Packing the file into a compressed package

    Args:
        file_paths: List of file path
        zip_file_name: The file name of the compressed package

    Returns:
        No return value
    """
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            if os.path.isfile(file_path):
                zip_file.write(file_path, os.path.basename(file_path))
            elif os.path.isdir(file_path):
                for root, _, files in os.walk(file_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        zip_file.write(full_path, os.path.relpath(full_path, file_path))

def get_temp_path():
    """Get cross -platform temporary file directory path"""
    temp_path = None
    try:
        # Try to obtain temporary file directory path in the system environment variable
        temp_path = (
            os.environ.get("TMPDIR") or os.environ.get("TMP") or os.environ.get("TEMP")
        )
    except Exception as e:
        print("Get the system environment variable temporary file directory path of the directory path, error message:", e)

    # If there is no temporary file directory path in the system environment variables, use it Python of tempfile Module Create temporary file directory
    if not temp_path:
        try:
            temp_path = tempfile.gettempdir()
        except Exception as e:
            Print ("" Use Python's TEMPFILE module to create a temporary file directory failed, error information: ", e)
    # Make sure that the temporary file directory exists
    if not os.path.exists(temp_path):
        try:
            os.makedirs(temp_path)
        except Exception as e:
            print("Failure to create a temporary file directory, error message:", e)

    return temp_path


temp_path = get_temp_path()

def get_formatted_date(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def get_modified_date(folder_path: str):
    return get_formatted_date(os.path.getmtime(folder_path))


def get_created_date(folder_path: str):
    return get_formatted_date(os.path.getctime(folder_path))


def unique_by(seq, key_func=lambda x: x):
    seen = set()
    return [x for x in seq if not (key := key_func(x)) in seen and not seen.add(key)]


def find(lst, comparator):
    return next((item for item in lst if comparator(item)), None)


def findIndex(lst, comparator):
    return next((i for i, item in enumerate(lst) if comparator(item)), -1)


def get_img_geninfo_txt_path(path: str):
    txt_path = re.sub(r"\.\w+$", ".txt", path)
    if os.path.exists(txt_path):
        return txt_path

def is_img_created_by_comfyui(img: Image):
    return img.info.get('prompt') and img.info.get('workflow')

def is_img_created_by_comfyui_with_webui_gen_info(img: Image):
    return img.info.get('parameters')

def read_sd_webui_gen_info_from_image(image: Image, path="") -> str:
    """
    Reads metadata from an image file.

    Args:
        image (PIL.Image.Image): The image object to read metadata from.
        path (str): Optional. The path to the image file. Used to look for a .txt file with additional metadata.

    Returns:
        str: The metadata as a string.
    """
    items = image.info or {}
    geninfo = items.pop("parameters", None)

    if "exif" in items:
        exif = piexif.load(items["exif"])
        exif_comment = (exif or {}).get("Exif", {}).get(piexif.ExifIFD.UserComment, b"")

        try:
            exif_comment = piexif.helper.UserComment.load(exif_comment)
        except ValueError:
            exif_comment = exif_comment.decode("utf8", errors="ignore")

        if exif_comment:
            items["exif comment"] = exif_comment
            geninfo = exif_comment

    if not geninfo and path:
        try:
            txt_path = get_img_geninfo_txt_path(path)
            if txt_path:
                with open(txt_path) as f:
                    geninfo = f.read()
        except Exception as e:
            pass

    return geninfo


re_param_code = r'\s*([\w ]+):\s*("(?:\\"[^,]|\\"|\\|[^\"])+"|[^,]*)(?:,|$)'
re_param = re.compile(re_param_code)
re_imagesize = re.compile(r"^(\d+)x(\d+)$")
re_lora_prompt = re.compile(r'<lora:(.*?):\d+(\.\d+)?>', re.IGNORECASE)
re_lora_extract = re.compile(r"([\w_\s.]+)(?:\d+)?")
re_lyco_prompt = re.compile(r'<lyco:(.*?):\d+(\.\d+)?>', re.IGNORECASE)
re_parens = re.compile(r"[\\/\[\](){}]+")


def lora_extract(lora: str):
    """
    Proposal Yoshino yoshino(2a79aa5adc4a)
    """
    res = re_lora_extract.match(lora)
    return res.group(1) if res else lora


def parse_prompt(x: str):
    x = re.sub(
        re_parens, "", x.replace("，", ",")
    )
    tag_list = [x.strip() for x in x.split(",")]
    res = []
    lora_list = []
    lyco_list = []
    for tag in tag_list:
        if len(tag) == 0:
            continue
        idx_colon = tag.find(":")
        if idx_colon != -1:
            if re.search(re_lora_prompt, tag):
                lora_res = re.search(re_lora_prompt, tag)
                lora_list.append(
                    {"name": lora_res.group(1), "value": float(lora_res.group(2))}
                )
            elif re.search(re_lyco_prompt, tag):
                lyco_res = re.search(re_lyco_prompt, tag)
                lyco_list.append(
                    {"name": lyco_res.group(1), "value": float(lyco_res.group(2))}
                )
            else:
                tag = tag[0:idx_colon]
                if len(tag):
                    res.append(tag.lower())
        else:
            res.append(tag.lower())
    return {"pos_prompt": res, "lora": lora_list, "lyco": lyco_list}


def parse_generation_parameters(x: str):
    res = {}
    prompt = ""
    negative_prompt = ""
    done_with_prompt = False
    if not x:
        return {"meta": {}, "pos_prompt": [], "pos_all": prompt, "lora": [], "lyco": []}
    *lines, lastline = x.strip().split("\n")
    if len(re_param.findall(lastline)) < 3:
        lines.append(lastline)
        lastline = ""
    if len(lines) == 1 and lines[0].startswith("Postprocess"):  # Change the above to <2 should be okay, I dare not move at that time
        lastline = lines[
            0
        ]  # Push PostProcess Upscale by: 4, PostProcess UPSCALER: R-ESRGAN 4X+ Anime6b
        lines = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("Negative prompt:"):
            done_with_prompt = True
            line = line[16:].strip()

        if done_with_prompt:
            negative_prompt += ("" if negative_prompt == "" else "\n") + line
        else:
            prompt += ("" if prompt == "" else "\n") + line

    for k, v in re_param.findall(lastline):
        v = v[1:-1] if v[0] == '"' and v[-1] == '"' else v
        m = re_imagesize.match(v)
        if m is not None:
            res[k + "-1"] = m.group(1)
            res[k + "-2"] = m.group(2)
        else:
            res[k] = v
    prompt_parse_res = parse_prompt(prompt)
    lora = prompt_parse_res["lora"]
    for k in res:
        k_s = str(k)
        if k_s.startswith("AddNet Module") and str(res[k]).lower() == "lora":
            model = res[k_s.replace("Module", "Model")]
            value = res.get(k_s.replace("Module", "Weight A"), "1")
            lora.append({"name": lora_extract(model), "value": float(value)})
    return {
        "meta": res,
        "pos_all": prompt,
        "pos_prompt": unique_by(prompt_parse_res["pos_prompt"]),
        "lora": unique_by(lora, lambda x: x["name"].lower()),
        "lyco": unique_by(prompt_parse_res["lyco"], lambda x: x["name"].lower()),
    }


tags_translate: Dict[str, str] = {}
try:
    import codecs

    with codecs.open(os.path.join(cwd, "tags-translate.csv"), "r", "utf-8") as tag:
        tags_translate_str = tag.read()
        for line in tags_translate_str.splitlines():
            en, mapping = line.split(",")
            tags_translate[en.strip()] = mapping.strip()
except Exception as e:
    pass


def open_folder(folder_path, file_path=None):
    folder = os.path.realpath(folder_path)
    if file_path:
        file = os.path.join(folder, file_path)
        if os.name == "nt":
            subprocess.run(["explorer", "/select,", file])
        elif sys.platform == "darwin":
            subprocess.run(["open", "-R", file])
        elif os.name == "posix":
            subprocess.run(["xdg-open", file])
    else:
        if os.name == "nt":
            subprocess.run(["explorer", folder])
        elif sys.platform == "darwin":
            subprocess.run(["open", folder])
        elif os.name == "posix":
            subprocess.run(["xdg-open", folder])


