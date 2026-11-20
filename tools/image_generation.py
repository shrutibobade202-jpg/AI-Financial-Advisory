from langchain.tools import tool
import base64
from openai import OpenAI
from utils.central_logging import setup_logging,get_logger
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from pathlib import Path
import os


setup_logging()
logger = get_logger("image_generation")

load_dotenv('./.env',override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    logger.info("Openai api key has been set")
else:
    logger.error("No openai api key found")

client = OpenAI()

IMAGE_DIR = "./generated_images"
os.makedirs(IMAGE_DIR, exist_ok=True)

def _generate_image_b64(query: str):
    response = client.images.generate(
        model="gpt-image-1",
        prompt=query,
        size="1024x1024"
    )
    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))
    filename = "generated.png"
    filepath = (Path(IMAGE_DIR) / filename).resolve()
    image.save(filepath, format="PNG")
    return filepath.as_posix()

@tool(description="""
Generate a base64-encoded image from a financial text query.
Use this tool to create educational or explanatory visuals such as:
- portfolio allocation diagrams
- retirement timelines
- diversification illustrations
- financial concept graphics
- retirement timelines
- diversification illustrations
Do NOT use for non-financial or unrelated imagery.
""")
def generate_image(query:str):
    """
    Generate a base64-encoded image from a text query.
    Use this tool to create educational or explanatory visuals such as:
    - portfolio allocation diagrams, retirement timelines, diversification illustrations
    - financial concept graphics
     portfolio allocation diagrams
    - retirement timelines
    - diversification illustrations    
    - charts
    - diagrams
    - infographics
    - visuals
    - illustrations

    The query must describe:
    - the financial concept
    - layout (pie chart, timeline, bar chart, etc.)
    - labels and style

    Do NOT use for non-financial or unrelated imagery.    
    """
    image_path = _generate_image_b64(query)
    return image_path
"""
    return {
        "type": "image",
        "format": "base64",
        "mime": "image/png",
        "data": b64,
        "source": "openai",
        "prompt": query
    }
"""

#path_res = _generate_image_b64("Can you generate a pie chart showing a diversified portfolio with 50% stocks, 30% bonds, and 20% cash?")
#print(path_res)