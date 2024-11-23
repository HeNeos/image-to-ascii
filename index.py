import argparse
from typing import Type, cast

from modules.dithering import DitheringStrategy
from modules.dithering.atkinson import DitheringAtkinson
from modules.dithering.floyd_steinberg import DitheringFloydSteinberg
from modules.image_to_ascii import run
from modules.text_to_text import text_to_text
from modules.video_to_ascii import video_image_convert

valid_formats = ["image", "text", "video"]

# save_formats = {
#     "show": SaveFormats.Show,
#     "text": SaveFormats.Text,
#     "image": SaveFormats.Image,
# }

dithering_strategy: dict[str, Type[DitheringStrategy]] = {
    DitheringAtkinson.name: DitheringAtkinson,
    DitheringFloydSteinberg.name: DitheringFloydSteinberg,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ImageToAscii", description="Convert an image/video/text to text"
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        nargs="?",
        help="image filename/path",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--format",
        nargs="?",
        type=str,
        help="input format",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-s",
        "--height",
        nargs="?",
        type=int,
        help="height to resize",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-t",
        "--text",
        nargs="?",
        type=str,
        help="text to image",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-d",
        "--dithering",
        nargs="?",
        type=str,
        help="dithering strategy",
        default=argparse.SUPPRESS,
    )
    # parser.add_argument("--save", nargs="?", type=str, default=argparse.SUPPRESS)
    args: argparse.Namespace = parser.parse_args()

    if "format" not in args:
        args.format = ""
    if args.format not in valid_formats:
        print(f"{args.format} is not a valid format: {','.join(valid_formats)}")
        raise Exception

    # if "save" not in args:
    #     args.save = "show"
    # if args.save not in save_formats.keys():
    #     print(
    #         f"{args.save} is not a valid save format: {','.join(save_formats.keys())}"
    #     )
    #     raise Exception

    if args.format == "text":
        if "text" not in args:
            args.text = ""
        if not isinstance(args.text, str) or len(args.text) == 0:
            print(f"{args.text} is not a valid text")
            raise Exception
    elif args.format == "image":
        if "filename" not in args:
            print("Missing filename")
            raise Exception
    elif args.format == "video":
        if "filename" not in args:
            args.filename = 0

    if "height" not in args:
        args.height = 720

    if "dithering" not in args:
        args.dithering = "atkinson"

    if args.format == "video":
        video_image_convert(
            video=cast(str, args.filename),
            height=args.height,
            dithering_strategy=dithering_strategy.get(
                args.dithering, DitheringAtkinson
            ),
        )
    elif args.format == "text":
        text_to_text(
            text=args.text,
            height=args.height,
            dithering_strategy=dithering_strategy.get(
                args.dithering, DitheringAtkinson
            ),
        )
    elif args.format == "image":
        run(
            image_path=cast(str, args.filename),
            height=args.height,
            dithering_strategy=dithering_strategy.get(
                args.dithering, DitheringAtkinson
            ),
        )
