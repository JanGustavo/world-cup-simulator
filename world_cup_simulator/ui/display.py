"""Display layer.

Can be CLI or Streamlit, interchangeable.
"""


def show(summary: dict) -> None:
    # Cabeçalho com alinhamento e larguras fixas
    header = f"{'Pontos':^6} | {'Aparições':^12} | {'Classificações':^16} | {'Probabilidade':^13}"
    divider = "-" * len(header)
    print(header)
    print(divider)
    for pontos, dados in summary.items():
        appearances = dados['appearances']
        classifications = dados['classifications']
        probability = dados['probability']
        print(f"{pontos:^6} | {appearances:>12,} | {classifications:>16,} | {probability:>13.2%}")
