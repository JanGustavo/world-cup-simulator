import numpy as np

class MatchModel:
    """Contrato para geração de resultados de partida."""

    def __init__(self, weight_factor: float = 0.0) -> None:
        # weight_factor = 0.0 significa sem pesos (ortogonal), > 0.0 significa ponderado
        self.weight_factor = weight_factor
        
        # Força padrão dos times de 0 a 47 (0 é o mais forte [1.0], 47 é o mais fraco [0.0])
        self.strengths = {t: (47 - t) / 47 for t in range(48)}

    def simulate_goals(self, home_team: int, away_team: int) -> tuple[int, int]:
        s_home = self.strengths.get(home_team, 0.5)
        s_away = self.strengths.get(away_team, 0.5)
        
        # Fórmula exponencial ortogonal: se weight_factor == 0.0, exp(0) = 1.0 (taxa de 1.35)
        lam_home = 1.35 * np.exp(self.weight_factor * (s_home - s_away))
        lam_away = 1.35 * np.exp(self.weight_factor * (s_away - s_home))
        
        home_goals = np.random.poisson(lam=lam_home)
        away_goals = np.random.poisson(lam=lam_away)
        return int(home_goals), int(away_goals)