import numpy as np

"""Registra estatísticas de simulações."""


def consolidate(array: np.ndarray) -> dict:
    """"""
    summary = {}
    for pontos in range(10):
        appearances = len(array[array[:,1] == pontos])
        classifications =  len(array[(array[:, 1] == pontos) & (array[:, 2] == 1.0)])
        probability = classifications / appearances if appearances > 0 else 0
        summary[pontos] = {
            "appearances": appearances,
            "classifications": classifications,
            "probability": probability
        }
    return summary