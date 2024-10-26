from modules.utils.custom_types import AsciiImage
from enum import Enum


class SaveFormats(Enum):
    Show = "show"
    Text = "text"
    Image = "image"
    Video = "video"


def save_ascii_text(ascii_art: AsciiImage, image_name: str) -> None:
    art = open(f"{image_name}.txt", "w+")
    for row in ascii_art:
        art.write(f"{''.join(row)}\n")
    art.close()
