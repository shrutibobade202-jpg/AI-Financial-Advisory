import base64
from io import BytesIO
from PIL import Image
import os 

IMAGE_DIR = "./generated_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def render_image_payload(payload: dict):
    """
    Unified renderer for all image tool outputs.
    Supports:
    - base64
    - raw bytes
    - URLs (future-proof)
    """
    if not payload or payload.get("type") != "image":

        return None

    fmt = payload.get("format")
    data = payload.get("data")

    if fmt == "base64":
        img_bytes = base64.b64decode(data)
        image = Image.open(BytesIO(img_bytes))
        filename = "generated.png"
        filepath = os.path.join(IMAGE_DIR, filename)
        image.save(filepath, format="PNG")
        return filepath


    if fmt == "bytes":
        image = Image.open(BytesIO(data))
        filename = "generated.png"
        filepath = os.path.join(IMAGE_DIR, filename)
        image.save(filepath, format="PNG")
        return filepath
        
    if fmt == "url":
        # Future extension
        return payload["url"]

    raise ValueError(f"Unsupported image format: {fmt}")