import os
from PIL import Image

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg'))

def get_image_info(filepath):
    try:
        with Image.open(filepath) as img:
            return {
                "Format": img.format,
                "Mode": img.mode,
                "Size": img.size
            }
    except Exception:
        return {"error": "unable to read image"}
