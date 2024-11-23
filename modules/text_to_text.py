import os
from typing import Type

from PIL import Image, ImageDraw, ImageFont

from modules.dithering import DitheringStrategy
from modules.image_to_ascii import run
from modules.save.formats import DisplayFormats
from modules.utils.font import Font


def generate_image_text(text: str) -> str:
    font = ImageFont.truetype(Font.Name.value, 256)
    text_box = font.getbbox(text)
    text_width: int = abs(text_box[2] - text_box[0])
    text_height: int = abs(text_box[1] - text_box[3])
    image_size: tuple[int, int] = (int(1.15 * text_width), int(2 * text_height))

    image: Image.Image = Image.new("RGB", image_size, color="black")
    draw = ImageDraw.Draw(image)

    x: int = (image_size[0] - text_width) // 2
    y: int = int((image_size[1] - 1.2 * text_height) // 2)
    draw.text((x, y), text, fill="white", font=font)

    image_name: str = f"assets/{text}.png"
    image.save(image_name)

    return image_name


def text_to_text(
    text: str, height: int, dithering_strategy: Type[DitheringStrategy]
) -> None:
    image_path = generate_image_text(text)
    run(image_path, height, dithering_strategy, [DisplayFormats.GRAY_SCALE])
    os.remove(image_path)
