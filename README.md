# World Cup Simulator

Este projeto é um simulador estatístico para a Copa do Mundo FIFA de 48 seleções utilizando simulações de Monte Carlo. Ele calcula a probabilidade de cada pontuação na fase de grupos resultar em classificação para a fase de mata-mata.

🚀 **Experimente online**: O simulador possui uma versão web interativa executada no Streamlit. Você pode acessar e realizar suas próprias simulações diretamente em: [https://world-cup-simulator-python.streamlit.app](https://simuladordepontoscopadomundo.streamlit.app/)

---

## Estrutura do Projeto

*   **`world_cup_simulator/main.py`**: O orquestrador da aplicação (UI e CLI).
*   **`world_cup_simulator/engine/simulator.py`**: Motor de simulação de partidas vetorizado e eficiente.
*   **`world_cup_simulator/engine/group_resolver.py`**: Algoritmo de classificação dos grupos e repescagem dos terceiros colocados.
*   **`world_cup_simulator/models/match_model.py`**: Modelo matemático para os confrontos.
*   **`world_cup_simulator/ui/display.py`**: Camada de visualização (terminal / Streamlit).

## Como Executar Localmente

Para executar a versão CLI:

```bash
cd world_cup_simulator
python3 main.py
```

Para rodar a versão interativa web localmente:

```bash
streamlit run world_cup_simulator/main.py
```

---

## Modelo Matemático (Explicação Moderada)

O simulador utiliza o método de **Monte Carlo**, que consiste em rodar o torneio inteiro milhares ou milhões de vezes para obter estimativas estatísticas precisas das probabilidades de classificação de cada equipe.

### 1. Geração de Gols (Distribuição de Poisson)
O número de gols marcados por uma equipe em uma partida é modelado seguindo a **Distribuição de Poisson**, que é a distribuição estatística padrão para contagem de eventos independentes em um intervalo fixo (como gols em um jogo de futebol):

$$P(k \text{ gols}) = \frac{\lambda^k e^{-\lambda}}{k!}$$

Onde $\lambda$ (lambda) representa a taxa esperada de gols de uma equipe. A taxa base utilizada é de $1.35$ gols por jogo.

### 2. Ajuste de Força (Fator Ponderado)
Para tornar os jogos realistas, o simulador usa a diferença de **Rating FIFA** entre as duas equipes como fator de ponderação:

*   Se `weight_factor = 0.0` (Modelo Ortogonal): As forças de todas as equipes são consideradas idênticas ($\lambda_{casa} = \lambda_{fora} = 1.35$). Todas as partidas têm chances simétricas de vitória/empate.
*   Se `weight_factor > 0.0` (Modelo Ponderado): A taxa esperada de gols de cada equipe é ajustada exponencialmente com base na diferença de força. Se a Equipe A é mais forte que a Equipe B:
    $$\lambda_A = 1.35 \cdot e^{\text{weight\_factor} \cdot (S_A - S_B)}$$
    $$\lambda_B = 1.35 \cdot e^{-\text{weight\_factor} \cdot (S_A - S_B)}$$
    Onde $S$ é a força normalizada do país (entre $0.0$ e $1.0$) baseada no seu ranking FIFA.

### 3. Classificação e Repescagem
Após simular as 72 partidas da fase de grupos, o simulador ordena as equipes de cada grupo seguindo os critérios oficiais de desempate (Pontos, Saldo de Gols, Gols Pró). Em seguida, agrupa os 12 terceiros colocados e classifica os 8 melhores para a fase de mata-mata.

---

## Resultados de Referência (1.000.000 de Simulações)

Estes são os resultados estatísticos obtidos com **1 milhão de simulações** utilizando o modelo ponderado padrão (`weight_factor = 1.0`).

### Probabilidade de Classificação por Pontos

Esta tabela demonstra a chance histórica de classificação para o mata-mata a partir dos pontos somados por uma seleção na fase de grupos (3 partidas):

| Pontos obtidos | Total de Aparições | Classificações de Sucesso | Chance de Classificação |
|:---:|:---:|:---:|:---:|
| **0** | 4.070.874 | 0 | **0.00%** |
| **1** | 5.475.763 | 257 | **0.00%** |
| **2** | 2.704.689 | 106.791 | **3.95%** |
| **3** | 7.940.190 | 4.131.830 | **52.04%** |
| **4** | 8.275.219 | 8.227.857 | **99.43%** |
| **5** | 2.628.922 | 2.628.922 | **100.00%** |
| **6** | 7.323.888 | 7.323.888 | **100.00%** |
| **7** | 5.382.545 | 5.382.545 | **100.00%** |
| **8** | 0 | 0 | **0.00%** |
| **9** | 4.197.910 | 4.197.910 | **100.00%** |

*Nota: Alcançar 8 pontos na fase de grupos é matematicamente impossível em 3 rodadas.*

### Top 15 Seleções Mais Favoritas à Classificação (Fase de Grupos)

Ao considerarmos o peso da força baseada no Rating FIFA real de cada país, as seleções mais tradicionais e fortes têm chances significativamente maiores de avançar:

| Posição | Seleção | Rating FIFA | Chance de Classificação |
|:---:|:---|:---:|:---:|
| **1** | Argentina | 1855 | **98.22%** |
| **2** | Brasil | 1784 | **96.80%** |
| **3** | França | 1840 | **96.60%** |
| **4** | Espanha | 1820 | **96.55%** |
| **5** | Bélgica | 1795 | **96.02%** |
| **6** | Alemanha | 1690 | **95.64%** |
| **7** | Portugal | 1745 | **94.70%** |
| **8** | Inglaterra | 1800 | **94.68%** |
| **9** | Suíça | 1610 | **89.73%** |
| **10** | Marrocos | 1663 | **89.72%** |
| **11** | Croácia | 1725 | **89.48%** |
| **12** | Países Baixos | 1740 | **88.99%** |
| **13** | Colômbia | 1655 | **88.12%** |
| **14** | Estados Unidos | 1661 | **87.48%** |
| **15** | México | 1650 | **87.15%** |

### Probabilidades no Mata-Mata (Chaveamento Fixo com 1.000.000 de Simulações)

Esta tabela apresenta a probabilidade de progresso de cada seleção no chaveamento fixo do mata-mata (a partir dos 16vos de final), incluindo a probabilidade final de conquistar o **Título** (Campeão):

| Posição | Seleção | Rating FIFA | Oitavas | Quartas | Semis | Final | Campeão (Título) |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **1** | Argentina | 1907.40 | 88.25% | 68.38% | 48.47% | 31.32% | **18.73%** |
| **2** | França | 1906.84 | 81.40% | 57.93% | 38.96% | 24.56% | **14.92%** |
| **3** | Espanha | 1879.58 | 74.35% | 46.25% | 31.47% | 18.25% | **10.62%** |
| **4** | Inglaterra | 1840.46 | 78.99% | 50.61% | 32.19% | 17.84% | **9.59%** |
| **5** | Brasil | 1785.19 | 60.17% | 41.13% | 21.73% | 11.03% | **5.40%** |
| **6** | Marrocos | 1776.40 | 50.06% | 36.59% | 17.47% | 8.96% | **4.40%** |
| **7** | Países Baixos | 1775.50 | 49.94% | 36.45% | 17.35% | 8.96% | **4.39%** |
| **8** | Colômbia | 1729.30 | 78.81% | 46.14% | 20.23% | 9.87% | **4.33%** |
| **9** | Portugal | 1764.86 | 53.92% | 24.82% | 14.43% | 6.86% | **3.31%** |
| **10** | México | 1736.01 | 62.96% | 29.52% | 16.05% | 7.40% | **3.30%** |
| **11** | Bélgica | 1735.41 | 57.51% | 35.23% | 15.72% | 7.09% | **3.23%** |
| **12** | Alemanha | 1726.22 | 68.33% | 27.35% | 14.10% | 6.64% | **2.97%** |
| **13** | Estados Unidos | 1677.17 | 73.40% | 35.12% | 13.83% | 5.54% | **2.24%** |
| **14** | Croácia | 1723.05 | 46.08% | 19.52% | 10.62% | 4.67% | **2.07%** |
| **15** | Suíça | 1676.00 | 58.97% | 30.35% | 11.95% | 5.27% | **2.06%** |
| **16** | Japão | 1673.68 | 39.83% | 23.30% | 9.97% | 4.07% | **1.58%** |
| **17** | Senegal | 1653.43 | 42.49% | 23.00% | 8.61% | 3.28% | **1.26%** |
| **18** | Noruega | 1594.04 | 52.67% | 19.36% | 6.96% | 2.38% | **0.77%** |
| **19** | Egito | 1584.71 | 50.38% | 13.94% | 5.93% | 2.13% | **0.68%** |
| **20** | Austrália | 1581.35 | 49.62% | 13.71% | 5.78% | 2.09% | **0.66%** |
| **21** | Argélia | 1576.80 | 41.03% | 17.50% | 5.44% | 1.93% | **0.60%** |
| **22** | Equador | 1592.59 | 37.04% | 12.87% | 5.33% | 1.81% | **0.59%** |
| **23** | Costa do Marfim | 1565.47 | 47.33% | 16.21% | 5.47% | 1.75% | **0.53%** |
| **24** | Canadá | 1551.07 | 59.08% | 17.81% | 5.12% | 1.62% | **0.49%** |
| **25** | Áustria | 1598.82 | 25.65% | 9.41% | 4.07% | 1.36% | **0.46%** |
| **26** | Paraguai | 1520.59 | 31.67% | 7.65% | 2.58% | 0.77% | **0.22%** |
| **27** | Suécia | 1525.58 | 18.60% | 7.07% | 2.43% | 0.72% | **0.20%** |
| **28** | República Democrática do Congo | 1495.48 | 21.01% | 7.00% | 2.31% | 0.61% | **0.15%** |
| **29** | África do Sul | 1451.24 | 40.92% | 9.15% | 1.99% | 0.49% | **0.11%** |
| **30** | Bósnia e Herzegovina | 1408.93 | 26.60% | 6.65% | 1.25% | 0.24% | **0.05%** |
| **31** | Cabo Verde | 1402.97 | 11.75% | 3.97% | 1.10% | 0.25% | **0.05%** |
| **32** | Gana | 1387.00 | 21.19% | 6.00% | 1.11% | 0.23% | **0.04%** |

---

## Análise de Complexidade (Big O)

A arquitetura do motor de simulação foi desenhada com foco em alta eficiência, utilizando vetorização NumPy para computação em C.

### 1. Complexidade de Tempo: $\mathcal{O}(N)$ (Linear)
O tempo de execução escala de forma estritamente linear com o número total de iterações ($N$):
*   **Simulação de Partidas**: Modelagem e geração de gols via distribuição de Poisson para 72 confrontos por copa: $\mathcal{O}(N \cdot 72) \rightarrow \mathcal{O}(N)$.
*   **Ordenação dos Grupos**: Ordenação de $4$ seleções para cada um dos $12$ grupos de cada copa: $\mathcal{O}(N \cdot 12 \cdot (4 \log 4)) \rightarrow \mathcal{O}(N)$.
*   **Mata-mata (Melhores Terceiros)**: Ordenação e filtragem dos $12$ terceiros colocados: $\mathcal{O}(N \cdot (12 \log 12)) \rightarrow \mathcal{O}(N)$.
*   **Vetorização**: Como todo o loop pesado roda vetorizado através do NumPy, o coeficiente multiplicativo de tempo é extremamente baixo (1 milhão de copas simuladas em apenas ~13 segundos).

### 2. Complexidade de Espaço: $\mathcal{O}(1)$ (Constante)
Graças ao processamento em lotes (*batching*):
*   O simulador quebra a execução em blocos de tamanho controlado de $B = 100.000$ iterações.
*   A memória máxima ativa alocada na RAM permanece constante em $\mathcal{O}(B \cdot \text{constante}) \rightarrow \mathcal{O}(1)$ em relação ao total de iterações $N$, eliminando qualquer risco de estouro de memória (Out of Memory) mesmo para 100 milhões de simulações.
