import typer
from typing import Optional, cast
from pathlib import Path

from modules.dithering import DitheringStrategy
from modules.dithering.utils import get_dithering_strategy
from modules.save.formats import DisplayFormats

valid_formats: list[str] = ["image", "text", "video"]

display_formats: dict[str, "DisplayFormats"] = {
    DisplayFormats.BLACK_AND_WHITE.name: DisplayFormats.BLACK_AND_WHITE,
    DisplayFormats.COLOR.name: DisplayFormats.COLOR,
    DisplayFormats.GRAY_SCALE.name: DisplayFormats.GRAY_SCALE,
}

app = typer.Typer(help="Convert an image/video/text to ASCII art")


@app.command()
def convert(
    filename: str | None = typer.Option(
        None, "-f", "--filename", help="Image filename/path"
    ),
    format: str = typer.Option(
        ..., "--format", help=f"One of: {', '.join(valid_formats)}"
    ),
    height: int = typer.Option(720, "-s", "--height", help="Output height"),
    text: str | None = typer.Option(None, "-t", "--text", help="Text to convert"),
    dithering: str | None = typer.Option(
        None, "-d", "--dithering", help="Dithering strategy"
    ),
    display_format: str = typer.Option(
        DisplayFormats.COLOR.name,
        "-df",
        "--display-format",
        help=f"Display format: {', '.join(display_formats.keys())}",
    ),
    edges: bool = typer.Option(False, "--edges", help="Activate edge detection"),
) -> None:
    """
    Convert an image, video, or text to ASCII art.
    """
    if format not in valid_formats:
        typer.echo(
            f"Invalid format '{format}'. Must be one of {', '.join(valid_formats)}."
        )
        raise typer.Exit(code=1)

    if format == "text":
        if not text:
            typer.echo("Missing text for 'text' format.")
            raise typer.Exit(code=1)
    elif format == "image" and not filename:
        typer.echo("Missing filename for 'image' format.")
        raise typer.Exit(code=1)
    elif format == "video" and not filename:
        typer.echo("Missing filename for 'video' format.")
        raise typer.Exit(code=1)
        # filename = "0"  # Default to webcam

    if filename is not None:
        path_filename = Path(filename)

    dithering_strategy: Optional[DitheringStrategy] = get_dithering_strategy(
        dithering or ""
    )
    selected_display_format: DisplayFormats = display_formats.get(
        display_format, DisplayFormats.COLOR
    )

    if format == "video":
        from modules.video_to_ascii import video_image_convert

        video_image_convert(
            video=path_filename,
            height=height,
            dithering_strategy=dithering_strategy,
            display_format=selected_display_format,
            edge_detection=edges,
        )
    elif format == "text":
        from modules.text_to_text import text_to_text

        text_to_text(
            text=cast(str, text),
            height=height,
            dithering_strategy=dithering_strategy,
            display_format=selected_display_format,
            edge_detection=edges,
        )
    elif format == "image":
        from modules.image_to_ascii import run

        run(
            image_path=path_filename,
            height=height,
            dithering_strategy=dithering_strategy,
            display_formats=[selected_display_format],
            edge_detection=edges,
        )


if __name__ == "__main__":
    app()
