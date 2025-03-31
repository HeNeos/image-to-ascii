import numpy as np
from PIL import Image, ImageDraw, ImageFont
from modules.utils.font import Font

ascii_chars = [chr(i) for i in range(32, 127)]

font_size = Font.Size.value
font_path = "./consolas.ttf"
canvas_size = font_size * 64
canvas_width = int(canvas_size * 6 / 9)
font = ImageFont.truetype(font_path, font_size)

char_luminosities = {}

for char in ascii_chars:
    img = Image.new("L", (canvas_width, canvas_size), color=0)
    draw = ImageDraw.Draw(img)

    for y in range(0, canvas_size, font_size):
        for x in range(0, canvas_width, font_size):
            draw.text((x, y), char, font=font, fill=255)

    pixel_data = np.array(img)
    luminosity = np.mean(pixel_data)

    char_luminosities[char] = luminosity

sorted_chars = sorted(char_luminosities.items(), key=lambda x: x[1])
for char, lum in sorted_chars:
    print(f"'{char}': {lum:.2f}")

print("".join([x[0] for x in sorted_chars]))
