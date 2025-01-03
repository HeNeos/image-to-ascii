import argparse
from typing import Type, cast

from modules.dithering import DitheringStrategy
from modules.dithering.atkinson import DitheringAtkinson
from modules.dithering.floyd_steinberg import DitheringFloydSteinberg
from modules.dithering.jarvis_judice_ninke import DitheringJarvisJudiceNinke
from modules.dithering.riemersma_naive import DitheringRiemersmaNaive
from modules.dithering.riemersma import DitheringRiemersma
from modules.image_to_ascii import run
from modules.text_to_text import text_to_text
from modules.video_to_ascii import video_image_convert
from modules.save.formats import DisplayFormats

valid_formats = ["image", "text", "video"]

dithering_strategy: dict[str, Type[DitheringStrategy]] = {
    DitheringAtkinson.name: DitheringAtkinson,
    DitheringFloydSteinberg.name: DitheringFloydSteinberg,
    DitheringJarvisJudiceNinke.name: DitheringJarvisJudiceNinke,
    DitheringRiemersmaNaive.name: DitheringRiemersmaNaive,
    DitheringRiemersma.name: DitheringRiemersma,
}

display_formats: dict[str, "DisplayFormats"] = {
    DisplayFormats.BLACK_AND_WHITE.name: DisplayFormats.BLACK_AND_WHITE,
    DisplayFormats.COLOR.name: DisplayFormats.COLOR,
    DisplayFormats.GRAY_SCALE.name: DisplayFormats.GRAY_SCALE,
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
        help=f"{', '.join(valid_formats)}",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-s",
        "--height",
        nargs="?",
        type=int,
        help="output height",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-t",
        "--text",
        nargs="?",
        type=str,
        help="text to ascii",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-d",
        "--dithering",
        nargs="?",
        type=str,
        help=f"{', '.join(dithering_strategy.keys())}",
        default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-df",
        "--display_format",
        nargs="?",
        type=str,
        help=f"{', '.join(display_formats.keys())}",
        default=argparse.SUPPRESS,
    )
    args: argparse.Namespace = parser.parse_args()

    if "format" not in args:
        args.format = ""
    if args.format not in valid_formats:
        print(f"{args.format} is not a valid format: {','.join(valid_formats)}")
        raise Exception

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
        args.dithering = ""

    if "display_format" not in args:
        args.display_format = ""

    dithering: type[DitheringStrategy] | None = dithering_strategy.get(args.dithering)
    display_format: DisplayFormats = display_formats.get(
        args.display_format, DisplayFormats.COLOR
    )

    if args.format == "video":
        video_image_convert(
            video=cast(str, args.filename),
            height=args.height,
            dithering_strategy=dithering,
            display_format=display_format,
        )
    elif args.format == "text":
        text_to_text(
            text=args.text,
            height=args.height,
            dithering_strategy=dithering,
            display_format=display_format,
        )
    elif args.format == "image":
        run(
            image_path=cast(str, args.filename),
            height=args.height,
            dithering_strategy=dithering,
            display_formats=[display_format],
        )
