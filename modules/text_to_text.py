import os

from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from modules.image_to_ascii import ascii_convert
from modules.save import SaveFormats
from modules.types import Scale


def generate_image_text(text: str) -> str:
    font = ImageFont.load_default()
    font = font.font_variant(size=100)
    text_box = font.getbbox(text)
    text_width = abs(text_box[2] - text_box[0])
    text_height = abs(text_box[1] - text_box[3])

    image_size = (int(1.15 * text_width), int(2 * text_height * 1.20))

    image: Image.Image = Image.new("RGB", image_size, color="white")
    draw = ImageDraw.Draw(image)

    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - 2 * text_height) / 2

    draw.text((x, y), text, fill="black", font=font)

    image_name = f"assets/{text}.png"
    image.save(image_name)

    return image_name


def text_to_text(
    text: Optional[str] = None,
    scale: Optional[Scale] = None,
    save_image=SaveFormats.Show,
):
    image_path = generate_image_text(text)
    ascii_convert(image_path, scale, save_image)
    os.remove(image_path)
