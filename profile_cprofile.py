import cProfile
import pstats
from game_of_life import GameOfLife, glider_pattern

def run_simulation():
    size = 512
    steps = 100
    initial = glider_pattern(size)
    game = GameOfLife(rows=size, cols=size, initial_state=initial)
    game.run(steps)

if __name__ == "__main__":
    profile_file = "game_profile.pstats"
    output_file = "profile_output.txt"

    # Ejecuta el perfilado y guarda los datos
    cProfile.run('run_simulation()', profile_file)

    # Procesa y escribe un resumen de los 15 métodos que más tiempo consumen
    with open(output_file, "w") as f:
        stats = pstats.Stats(profile_file, stream=f)
        stats.strip_dirs().sort_stats("cumulative").print_stats(15)

    print(f"Perfilado completado. Resultados en '{output_file}'.")