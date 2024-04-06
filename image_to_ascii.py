import os
import sys
import argparse

from PIL import Image
from typing import Optional, Union, Tuple

char_ranges = {
    1: "#",
    100: "X",
    200: "%",
    300: "&",
    400: "*",
    500: "+",
    600: "/",
    700: "(",
    750: "'"
}

ascii_chars = '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,"^`\\' + "'. "

def map_to_char_low(pixel_sum: int) -> str:
    keys = sorted(list(char_ranges.keys()))
    for key in keys:
        if pixel_sum < key:
            return char_ranges[key]
    return " "

def map_to_char_high(gray_scale: float) -> str:
    position: int = int(((len(ascii_chars) - 1) * gray_scale + (255-1)) // 255)
    return ascii_chars[position]

def calculate_scale(image_size: Tuple[int, int], scale: Optional[Union[int, float]] = None) -> int:
    if scale:
        return int(scale)
    max_length = (1<<7)
    max_size = max(image_size)
    scale: int = (max_size + max_length - 1) // max_length
    return scale


def asciiConvert(image_path: str, scale: Optional[Union[int, float]] = None):
    image_name, image_extension = image_path.split(".")

    image = Image.open(image_path)
    width, height = image.size
    scale = calculate_scale((width, height), scale)

    resized_width: int = width//scale
    resized_height: int = height//scale
    resized_image_name: str = f"{image_name}_resized"
    image.resize((resized_width, resized_height)).save(f"{resized_image_name}.{image_extension}")

    resized_image = Image.open(f"{resized_image_name}.{image_extension}")
    resized_width, resized_height = resized_image.size


    grid = [["X"] * resized_width for i in range(resized_height)]

    pix = resized_image.load()
    for y in range(resized_height):
        for x in range(resized_width):
            if max(resized_width, resized_height) > 160:
                red, green, blue = pix[x,y][:3]
                grid[y][x] = map_to_char_high(0.21*red + 0.72*green + 0.07*blue)
            else:
                grid[y][x] = map_to_char_low(sum(pix[x,y]))

    art = open(f"{image_name}.txt", "w+")
    for row in grid:
        art.write(f"{''.join(row)}\n")
    art.close()

    os.remove(f"{resized_image_name}.{image_extension}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog = "ImageToAscii",
        description = "Convert an image to text",
        epilog = ":)"
    )
    parser.add_argument("filename", type=str, nargs=1, help="image filename/path")
    parser.add_argument("-s", "--scale", nargs="?", type=int, help="scale to resize the image", default=argparse.SUPPRESS)
    args = parser.parse_args()
    if "scale" not in args:
        args.scale = None
    asciiConvert(args.filename[0], args.scale)
