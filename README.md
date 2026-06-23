# World Cup Simulator

Este projeto é um simulador estatístico para a Copa do Mundo FIFA de 48 seleções utilizando simulações de Monte Carlo. Ele calcula a probabilidade de cada pontuação na fase de grupos resultar em classificação.

## Estrutura do Projeto

*   **`world_cup_simulator/main.py`**: O orquestrador da simulação.
*   **`world_cup_simulator/engine/simulator.py`**: Motor de simulação de partidas e controle de iterações.
*   **`world_cup_simulator/engine/group_resolver.py`**: Algoritmo otimizado de resolução de classificação de grupos e melhores terceiros.
*   **`world_cup_simulator/models/match_model.py`**: Modelo matemático ponderado e ortogonal para resultados de jogos.
*   **`world_cup_simulator/stats/consolidator.py`**: Consolidador estatístico dos resultados obtidos.
*   **`world_cup_simulator/ui/display.py`**: Camada de visualização no terminal.

## Como Executar

Para executar a simulação:

```bash
cd world_cup_simulator
python3 main.py
```

## Modelo Ponderado Ortogonal

O simulador suporta ponderação através de um único parâmetro ajustável no modelo matemático:
*   `weight_factor = 0.0`: Modelo sem pesos (completamente ortogonal, onde todas as seleções são equivalentes).
*   `weight_factor > 0.0`: Modelo ponderado baseado na força de cada seleção.
