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

def generate_group_games(team_ids: list[int], match_model: MatchModel) -> list[dict]:
    games = []
    for home, away in combinations(team_ids, 2):
        home_goals, away_goals = match_model.simulate_goals(home, away)
        games.append({
            "home": home,
            "away": away,
            "home_goals": home_goals,
            "away_goals": away_goals
        })
    return games

def run_simulation(iterations: int) -> np.ndarray:
    model = MatchModel(is_weighted=False)
    results = []

    for _ in range(iterations):
        groups_results = []
        all_teams = {}
        
        # 1. Simula os 12 grupos de 4 times
        for g in range(12):
            team_ids = [g * 4 + i for i in range(4)]
            games = generate_group_games(team_ids, model)
            table = build_table(games)
            all_teams.update(table)
            groups_results.append(classify_group(table))

        # 2. Define quem avançou
        passed_ids = set()
        for g_res in groups_results:
            passed_ids.add(g_res["primeiro"]["id"])
            passed_ids.add(g_res["segundo"]["id"])
            
        best_thirds = get_best_thirds(groups_results)
        for team in best_thirds:
            passed_ids.add(team["id"])

        # 3. Aloca os resultados da iteração atual
        for t_id in range(48):
            team_data = all_teams[t_id]
            passou = 1.0 if t_id in passed_ids else 0.0
            results.append([float(t_id), float(team_data["pontos"]), passou])

    return np.array(results)