"""Application orchestrator: wires models, engine, stats, and UI."""

from engine.simulator import run_simulation
from stats.consolidator import consolidate
from ui.display import show
iteracoes = 10_000

def main() -> None:
    raw_results = run_simulation(iterations=iteracoes)
    summary = consolidate(raw_results)
    show(summary)

if __name__ == "__main__":
    main()