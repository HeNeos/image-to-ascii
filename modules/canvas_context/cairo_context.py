from abc import ABC, abstractmethod

from cairo import Context, ImageSurface

from modules.save.formats import DisplayFormats
from modules.utils.custom_types import Color


class CairoContext(ABC, Context):
    def __init__(self, surface: ImageSurface):
        self.context = Context(surface)

    @abstractmethod
    def set_color(self, color: Color, luminance: float) -> None:
        pass


class CairoColorContext(CairoContext):
    def set_color(self, color: Color, luminance: float) -> None:
        self.context.set_source_rgb(color[0] / 255, color[1] / 255, color[2] / 255)


class CairoGrayContext(CairoContext):
    def set_color(self, color: Color, luminance: float) -> None:
        self.context.set_source_rgb(luminance / 255, luminance / 255, luminance / 255)


class CairoContextFactory:
    @staticmethod
    def create(display_format: DisplayFormats, surface: ImageSurface) -> CairoContext:
        if display_format is DisplayFormats.COLOR:
            return CairoColorContext(surface)
        if display_format is DisplayFormats.GRAY_SCALE:
            return CairoGrayContext(surface)
