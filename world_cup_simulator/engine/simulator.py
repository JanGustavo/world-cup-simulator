import numpy as np
from models.match_model import MatchModel

def run_simulation(iterations: int, model: MatchModel = None) -> np.ndarray:
    N = iterations
    base_lam = 1.35
    
    # 1. Configurar as forças das equipes de forma vetorizada (Shape: 48)
    if model is None:
        weight_factor = 0.0
        strengths_arr = np.full(48, 0.5)
    else:
        weight_factor = model.weight_factor
        strengths_arr = np.array([model.strengths.get(i, 0.5) for i in range(48)])

    # Índices locais das 6 partidas possíveis dentro de um grupo de 4 times
    home_idx_local = np.array([0, 0, 0, 1, 1, 2])
    away_idx_local = np.array([1, 2, 3, 2, 3, 3])
    
    # Expandir para os IDs globais dos 72 jogos da fase de grupos (12 grupos x 6 jogos)
    group_offsets = np.arange(12)[:, np.newaxis] * 4
    all_home_ids = (group_offsets + home_idx_local).reshape(12, 6)
    all_away_ids = (group_offsets + away_idx_local).reshape(12, 6)
    
    # Calcular os lambdas de Poisson para os 72 confrontos de uma vez (exponencial ortogonal)
    if weight_factor > 0.0:
        diff = strengths_arr[all_home_ids] - strengths_arr[all_away_ids]
        lam_home = base_lam * np.exp(weight_factor * diff)
        lam_away = base_lam * np.exp(-weight_factor * diff)
    else:
        lam_home = np.full((12, 6), base_lam)
        lam_away = np.full((12, 6), base_lam)
        
    # Broadcast dos lambdas para cobrir todas as N iterações de forma tridimensional (Shape: N, 12, 6)
    lam_home_3d = np.tile(lam_home, (N, 1, 1))
    lam_away_3d = np.tile(lam_away, (N, 1, 1))
    
    # 2. GERAR TODOS OS GOLS DA COPA DE UMA SÓ VEZ EM MEMÓRIA C
    home_goals = np.random.poisson(lam=lam_home_3d)
    away_goals = np.random.poisson(lam=lam_away_3d)
    
    # 3. Mapeamento de pontos por partida (Shape: N, 12, 6)
    pts_home_games = np.where(home_goals > away_goals, 3, np.where(home_goals == away_goals, 1, 0))
    pts_away_games = np.where(away_goals > home_goals, 3, np.where(home_goals == away_goals, 1, 0))
    
    # 4. Construção das Tabelas dos Grupos (Shape: N, 12, 4)
    pontos = np.zeros((N, 12, 4), dtype=int)
    gols_marcados = np.zeros((N, 12, 4), dtype=int)
    gols_sofridos = np.zeros((N, 12, 4), dtype=int)
    
    # Loop fixo de 6 iterações (tamanho constante das partidas do grupo, não escala com N)
    for i in range(6):
        h = home_idx_local[i]
        a = away_idx_local[i]
        
        pontos[:, :, h] += pts_home_games[:, :, i]
        pontos[:, :, a] += pts_away_games[:, :, i]
        
        gols_marcados[:, :, h] += home_goals[:, :, i]
        gols_marcados[:, :, a] += away_goals[:, :, i]
        
        gols_sofridos[:, :, h] += away_goals[:, :, i]
        gols_sofridos[:, :, a] += home_goals[:, :, i]
        
    saldo = gols_marcados - gols_sofridos
    
    # 5. O TRUQUE ARQUITETURAL: Sorting de múltiplos critérios sem loops (Score Combinado)
    # Codificamos pontos, saldo e gols marcados em um único número inteiro para ordenação estável
    # pontos max=9 (peso 10k), saldo max/min ajustado com offset (+50 para evitar negativos, peso 100)
    score = pontos * 10000 + (saldo + 50) * 100 + gols_marcados
    rankings = np.argsort(-score, axis=2) # Retorna os índices locais ordenados do 1º ao 4º lugar
    
    # Criar mapeamento de IDs globais (0 a 47) tridimensional
    global_ids_3d = np.tile(np.arange(48).reshape(12, 4), (N, 1, 1))
    
    # Indexação avançada para reordenar todas as matrizes conforme o ranking real
    grid_n, grid_g = np.meshgrid(np.arange(N), np.arange(12), indexing='ij')
    grid_n = grid_n[:, :, np.newaxis]
    grid_g = grid_g[:, :, np.newaxis]
    
    sorted_global_ids = global_ids_3d[grid_n, grid_g, rankings]
    sorted_pontos = pontos[grid_n, grid_g, rankings]
    sorted_saldo = saldo[grid_n, grid_g, rankings]
    sorted_gols_marcados = gols_marcados[grid_n, grid_g, rankings]
    
    # 6. Definir Classificados Diretos (G2)
    passed = np.zeros((N, 48), dtype=float)
    grid_n_2d = np.arange(N)[:, np.newaxis]
    
    passed[grid_n_2d, sorted_global_ids[:, :, 0]] = 1.0 # 1º Colocado
    passed[grid_n_2d, sorted_global_ids[:, :, 1]] = 1.0 # 2º Colocado
    
    # 7. Resolução Vetorizada da Repescagem dos 12 Terceiros Colocados
    thirds_ids = sorted_global_ids[:, :, 2]
    thirds_points = sorted_pontos[:, :, 2]
    thirds_saldo = sorted_saldo[:, :, 2]
    thirds_goals = sorted_gols_marcados[:, :, 2]
    
    # Aplica o Score Combinado para classificar a tabela dos terceiros
    thirds_score = thirds_points * 10000 + (thirds_saldo + 50) * 100 + thirds_goals
    thirds_rankings = np.argsort(-thirds_score, axis=1)
    
    # Extrai os 8 melhores terceiros de cada uma das N iterações de uma vez
    best_thirds_ids = thirds_ids[grid_n_2d, thirds_rankings[:, :8]]
    passed[grid_n_2d, best_thirds_ids] = 1.0
    
    # 8. Montar o Output de dados linearizado esperado pelo Consolidador
    flat_points = pontos.reshape(N, 48) # O layout do array mapeia perfeitamente de 0 a 47
    team_ids_flat = np.tile(np.arange(48), (N, 1))
    
    final_array = np.stack([team_ids_flat, flat_points, passed], axis=-1).reshape(-1, 3)
    return final_array