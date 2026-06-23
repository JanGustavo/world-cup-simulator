import numpy as np

class MatchModel:
    """Responsável por simular os gols de uma partida usando Distribuição de Poisson."""
    
    def __init__(self, is_weighted: bool = False) -> None:
        self.is_weighted = is_weighted

    def simulate_goals(self, home_id: int, away_id: int) -> tuple[int, int]:
        # Em uma arquitetura futura com pesos, a média (lam) mudaria dependendo do ID do time.
        # Para manter simples e uniforme: média de 1.35 gols por time.
        home_goals = int(np.random.poisson(lam=1.35))
        away_goals = int(np.random.poisson(lam=1.35))
        return home_goals, away_goals