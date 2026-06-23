"""Módulo responsável por resolver a classificação dos grupos com base nos resultados dos jogos."""
def classify_group(group_tables: dict) -> dict:
    ordered = order_teams(group_tables)
    return {
        "primeiro": ordered[0],
        "segundo": ordered[1],
        "terceiro": ordered[2],
        "quarto": ordered[3]
    }

def get_best_thirds(groups: list[dict]) -> list[dict]:
    """Coleta os terceiros colocados de todos os grupos e retorna os 8 melhores."""
    thirds = [group["terceiro"] for group in groups]
    thirds_dict = {team["id"]: team for team in thirds}
    return order_teams(thirds_dict)[:8]

def order_teams(teams: dict) -> list:
    """Ordena os times seguindo estritamente as regras de pontos, saldo e gols pró."""
    return sorted(
        teams.values(),
        key=lambda time: (
            time["pontos"],
            time["gols_marcados"] - time["gols_sofridos"],
            time["gols_marcados"]
        ),
        reverse=True
    )

def build_table(games: list[dict]) -> dict[int, dict]:
    """Gera a tabela de pontos e gols sem criar estruturas de dados inúteis em memória."""
    table = {}
    for game in games:
        h, a = game["home"], game["away"]
        hg, ag = game["home_goals"], game["away_goals"]

        # Inicialização rápida
        if h not in table: table[h] = {"id": h, "pontos": 0, "gols_marcados": 0, "gols_sofridos": 0}
        if a not in table: table[a] = {"id": a, "pontos": 0, "gols_marcados": 0, "gols_sofridos": 0}

        # Computa gols
        table[h]["gols_marcados"] += hg
        table[h]["gols_sofridos"] += ag
        table[a]["gols_marcados"] += ag
        table[a]["gols_sofridos"] += hg

        # Computa pontos
        if hg > ag:
            table[h]["pontos"] += 3
        elif ag > hg:
            table[a]["pontos"] += 3
        else:
            table[h]["pontos"] += 1
            table[a]["pontos"] += 1

    return table