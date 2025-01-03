# ImageToAscii

Convert an image, video, or text to ASCII text.

## Description

This project allows you to convert images, videos, or text into ASCII art. It supports different dithering strategies and display formats such as color, grayscale, and black-and-white. The output can be saved as an image, video, or text file.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Dithering Strategies](#dithering-strategies)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/image-to-ascii.git
    ```
2. Navigate to the project directory:
    ```bash
    cd image-to-ascii
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To convert an image, video, or text to ASCII text, run the `run.py` script with the appropriate parameters:

```bash
python run.py --filename path/to/your/file --format image --dithering FloydSteinberg
```

## Parameters

- `--filename`: Path to the input file (image, video, or text).
- `--format`: Input format (image, video, text).
- `--dithering`: Dithering strategy (Atkinson, FloydSteinberg, JarvisJudiceNinke, RiemersmaNaive, Riemersma).

## Features

- Convert images, videos, or text to ASCII art.
- Support for different display formats:
  - Color
  - Grayscale
  - Black-and-white
- Save output as:
  - Image
  - Video
  - Text file

## Dithering Strategies
- Atkinson: Atkinson dithering algorithm.
- FloydSteinberg: Floyd-Steinberg dithering algorithm.
- JarvisJudiceNinke: Jarvis, Judice, and Ninke dithering algorithm.
- RiemersmaNaive: Naive Riemersma dithering algorithm.
- Riemersma: Riemersma dithering algorithm.