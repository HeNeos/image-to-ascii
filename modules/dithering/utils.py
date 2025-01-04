from functools import lru_cache
from typing import cast
from importlib import import_module
from ..dithering import DitheringStrategy


class DitheringLoader:
    @staticmethod
    def _get_module_and_class(strategy_name: str) -> tuple[str, str]:
        module_name = f".{strategy_name}"

        class_parts = strategy_name.split("_")
        class_name = f"Dithering{''.join(part.capitalize() for part in class_parts)}"

        return module_name, class_name

    @staticmethod
    @lru_cache(maxsize=None)
    def get_strategy(name: str) -> DitheringStrategy | None:
        try:
            module_name, class_name = DitheringLoader._get_module_and_class(name)
            module = import_module(module_name, package=__package__)
            return cast(DitheringStrategy, getattr(module, class_name))
        except (ImportError, AttributeError):
            return None


def get_dithering_strategy(name: str) -> DitheringStrategy | None:
    return DitheringLoader.get_strategy(name)
