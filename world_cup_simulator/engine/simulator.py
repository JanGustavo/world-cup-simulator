import numpy as np
from engine.group_resolver import build_table, classify_group, get_best_thirds
from itertools import combinations
from models.match_model import MatchModel

# Entrada: lista de dicionários de partidas simuladas.
# Cada jogo tem o formato:
# {
#     "home": 0,
#     "away": 1,
#     "home_goals": 2,
#     "away_goals": 1,
# }

def generate_group_games(team_ids: list[int], model: MatchModel) -> list[dict]:
    games = []
    for home, away in combinations(team_ids, 2):
        home_goals, away_goals = model.simulate_goals(home, away)
        games.append({
            "home": home,
            "away": away,
            "home_goals": home_goals,
            "away_goals": away_goals
        })
    return games


""" devolve um array NumPy com shape (N×48, 3)"""
def run_simulation(iterations: int, model: MatchModel = None) -> np.ndarray:
    if model is None:
        model = MatchModel(weight_factor=0.0)
        
    results = []
    for _ in range(iterations):
        groups_results = []
        all_teams = {}
        for g in range(12):
            team_ids = [g * 4 + i for i in range(4)]
            games = generate_group_games(team_ids, model)
            table = build_table(games)
            classified = classify_group(table)
            groups_results.append(classified)
            all_teams.update(table)

        best_thirds = get_best_thirds(groups_results)
        passed_ids = set()
        for classified in groups_results:
            passed_ids.add(classified["primeiro"]["id"])
            passed_ids.add(classified["segundo"]["id"])
        for team in best_thirds:
            passed_ids.add(team["id"])

        for t in range(48):
            team_data = all_teams[t]
            pontos = team_data["pontos"]
            passou = 1.0 if t in passed_ids else 0.0
            results.append([float(t), float(pontos), passou])

    return np.array(results)