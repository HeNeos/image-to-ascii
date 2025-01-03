from ..dithering import DitheringStrategy


def get_dithering_strategy(name: str) -> type[DitheringStrategy] | None:
    if name == "riemersma":
        from .riemersma import DitheringRiemersma

        return DitheringRiemersma
    elif name == "floyd_steinberg":
        from .floyd_steinberg import DitheringFloydSteinberg

        return DitheringFloydSteinberg
    elif name == "jarvis_judice_ninke":
        from .jarvis_judice_ninke import DitheringJarvisJudiceNinke

        return DitheringJarvisJudiceNinke
    elif name == "riemersma_naive":
        from .riemersma_naive import DitheringRiemersmaNaive

        return DitheringRiemersmaNaive
    elif name == "atkinson":
        from .atkinson import DitheringAtkinson

        return DitheringAtkinson
    else:
        return None
