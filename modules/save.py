from PIL import Image, ImageDraw, ImageFont
from modules.font import Font
from modules.types import AsciiImage, AsciiColors
from enum import Enum


class SaveFormats(Enum):
    Show = "show"
    Text = "text"
    Image = "image"
    Video = "video"


def save_ascii_text(ascii_art: AsciiImage, image_name: str, **kwargs):
    art = open(f"{image_name}.txt", "w+")
    for row in ascii_art:
        art.write(f"{''.join(row)}\n")
    art.close()


def save_ascii_image(ascii_art: AsciiImage, image_name: str, **kwargs):
    image: Image.Image = Image.new(
        "RGBA",
        (Font.Width.value * len(ascii_art[0]), Font.Height.value * len(ascii_art)),
        "black",
    )
    image_colors = kwargs["image_colors"]
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("consolas.ttf", 14)
    x, y = 0, 0
    for row in range(len(ascii_art)):
        for column in range(len(ascii_art[row])):
            color = image_colors[row][column]
            draw.text((x, y), ascii_art[row][column], font=font, fill=color)
            x += Font.Width.value
        x = 0
        y += Font.Height.value
    image.save(f"{image_name}_ascii.png")


map_save_formats = {
    SaveFormats.Text: save_ascii_text,
    SaveFormats.Image: save_ascii_image,
}


def save_ascii(
    ascii_art: AsciiImage,
    save_format: SaveFormats,
    image_name: str,
    image_colors: AsciiColors,
):
    save_function = map_save_formats[save_format]
    save_function(ascii_art, image_name, image_colors=image_colors)
