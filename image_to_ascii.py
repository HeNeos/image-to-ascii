import os
from PIL import Image, ImageDraw, ImageFont
from typing import Optional, Union, Tuple

ascii_chars = " `.',-~:;=+*#%@M"  # black background
# ascii_chars = "M@%#*+=;:~-,'.` "  # white background


def map_to_char_high(gray_scale: float) -> str:
    position: int = int(((len(ascii_chars) - 1) * gray_scale) / 255)
    return ascii_chars[position]


def calculate_scale(
    image_size: Tuple[int, int], scale: Optional[Union[int, float]] = None
) -> int:
    if scale:
        return int(scale)
    max_length = 200
    max_size = max(image_size)
    new_scale: int = (max_size + max_length - 1) // max_length
    return new_scale


def generate_image_text(text):
    font = ImageFont.load_default()
    font = font.font_variant(size=100)
    text_box = font.getbbox(text)
    text_width = abs(text_box[2] - text_box[0])
    text_height = abs(text_box[1] - text_box[3])

    image_size = (int(1.15 * text_width), int(2 * text_height * 1.20))

    image = Image.new("RGB", image_size, color="white")
    draw = ImageDraw.Draw(image)

    x = (image_size[0] - text_width) / 2
    y = (image_size[1] - 2 * text_height) / 2

    draw.text((x, y), text, fill="black", font=font)

    image_name = f"assets/{text}.png"
    image.save(image_name)

    return image_name


def cut_grid(grid):
    resized_grid = []
    for line in grid:
        if not all(column == " " for column in line):
            resized_grid.append(line)
    return resized_grid


def process_image(image, rescale=True, image_path: Optional[str] = None, scale=None):
    width, height = image.size
    if rescale:
        image_name, image_extension = image_path.split(".")
        scale = calculate_scale((width, height), scale)
        resized_width: int = width // scale * 2
        resized_height: int = height // scale
        resized_image_name: str = f"{image_name}_resized"
        image.resize((resized_width, resized_height)).save(
            f"{resized_image_name}.{image_extension}"
        )
        resized_image = Image.open(f"{resized_image_name}.{image_extension}").convert(
            "LA"
        )
    else:
        resized_image = image.convert("LA")
    resized_width, resized_height = resized_image.size

    grid = [["X"] * resized_width for i in range(resized_height)]

    pix = resized_image.load()
    for y in range(resized_height):
        for x in range(resized_width):
            current_char = map_to_char_high(pix[x, y][0])
            grid[y][x] = current_char
    if rescale:
        os.remove(f"{resized_image_name}.{image_extension}")
    return grid


def ascii_convert(
    image_path: Optional[str],
    scale: Optional[Union[int, float]] = None,
    save_image=True,
):

    image_name, image_extension = image_path.split(".")
    image = Image.open(image_path)
    grid = process_image(image, rescale=True, image_path=image_path, scale=scale)

    resized_grid = cut_grid(grid)

    if save_image:
        art = open(f"{image_name}.txt", "w+")
        for row in resized_grid:
            art.write(f"{''.join(row)}\n")
        art.close()
    return resized_grid


def text_to_text(
    text: Optional[str] = None,
    scale: Optional[Union[int, float]] = None,
    save_image=True,
):
    image_path = generate_image_text(text)
    ascii_convert(image_path, scale, save_image)
    os.remove(image_path)
