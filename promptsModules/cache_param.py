# -*- coding:utf-8 -*-
import json
import os

# Global variable for cache file name
CACHE_FILE = 'cache_params.json'
_cache = None  # 全局变量，用于缓存内存中的数据

KEY_IMAGE_GET_PROMPT = 'image_get_prompt'
KEY_TRAIN_TAGS_PROMPT = 'train_tags_prompt'

KEY_COMFYUI_PROMPT = 'comfyui_prompt'
KEY_COMFYUI_SELECT_FIRST_LORA = 'comfyui_select_first_lora'
KEY_COMFYUI_STRENGTH_FIRST_LORA = 'comfyui_strength_first_lora'
KEY_COMFYUI_ENABLE_SECOND = 'comfyui_enable_second'
KEY_COMFYUI_SELECT_SECOND_LORA = 'comfyui_select_second_lora'
KEY_COMFYUI_STRENGTH_SECOND_LORA = 'comfyui_strength_second_lora'
KEY_COMFYUI_STRENGTH_CLIP_SECOND_LORA = 'comfyui_strength_clip_second_lora'
KEY_COMFYUI_IMAGE_SIZE = 'comfyui_image_size'

KEY_PATH_LORA_LOAD = 'path_lora_load'
KEY_PATH_WORKFLOW = 'path_workflow'

KEY_DATA_LORA_LIST = 'data_lora_list'
KEY_DATA_WORKFLOW_JSON = 'data_workflow_json'

def ensure_cache_file():
    """
    Ensure the cache file exists. If not, create an empty JSON file.
    """
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as f:
            json.dump({}, f)


def load_cache():
    """
    Load the cache into memory if not already loaded.
    """
    global _cache
    if _cache is None:
        ensure_cache_file()
        with open(CACHE_FILE, 'r') as f:
            _cache = json.load(f)


def save_cache():
    """
    Save the in-memory cache to the file.
    """
    global _cache
    with open(CACHE_FILE, 'w') as f:
        json.dump(_cache, f, indent=4)


def cache_param(cache_key: str, cache_value):

    global _cache

    # Validate input type
    if cache_value is None:
        return
    if not isinstance(cache_value, (str, int, bool, float, list, dict)):
        raise ValueError("Cache value must be a string, integer, float, boolean, list, or dict")

    # Load cache into memory if not loaded
    load_cache()

    # Update cache in memory
    _cache[cache_key] = cache_value

    # Persist changes to file
    save_cache()


def load_cache_param(cache_key: str, default=None):
    """
    Load a parameter from the cache.

    Args:
        cache_key (str): The key to retrieve
        default: The default value if the key does not exist

    Returns:
        The value associated with the key, or the default if key doesn't exist
    """
    # Load cache into memory if not loaded
    load_cache()

    # Return value from in-memory cache
    return _cache.get(cache_key, default)
