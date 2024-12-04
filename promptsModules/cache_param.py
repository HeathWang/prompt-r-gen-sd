# -*- coding:utf-8 -*-

import json
import os

# Global variable for cache file name
CACHE_FILE = 'cache_params.json'

KEY_IMAGE_GET_PROMPT = 'image_get_prompt'
KEY_TRAIN_TAGS_PROMPT = 'train_tags_prompt'
KEY_COMFYUI_PROMPT = 'comfyui_prompt'


def ensure_cache_file():
    """
    Ensure the cache file exists. If not, create an empty JSON file.
    """
    if not os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'w') as f:
            json.dump({}, f)


def cache_param(cache_key: str, cache_value):
    """
    Store a parameter in the cache file.

    Args:
        cache_key (str): The key under which to store the value
        cache_value (str or int): The value to store (must be string or int)
    """
    # Validate input type
    if not isinstance(cache_value, (str, int)):
        raise ValueError("Cache value must be a string or integer")

    # Ensure cache file exists
    ensure_cache_file()

    # Read existing cache
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    # Update cache with new key-value pair
    cache[cache_key] = cache_value

    # Write updated cache back to file
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)


def load_cache_param(cache_key: str, default=None):
    """
    Load a parameter from the cache file.

    Args:
        cache_key (str): The key to retrieve

    Returns:
        The value associated with the key, or None if key doesn't exist
        :param cache_key:
        :param default:
    """
    # Ensure cache file exists
    ensure_cache_file()

    # Read cache file
    with open(CACHE_FILE, 'r') as f:
        cache = json.load(f)

    # check if key exists in cache
    if cache_key not in cache:
        return default

    # Return value if key exists, otherwise return None
    return cache.get(cache_key)
