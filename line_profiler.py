import numpy as np
from game_of_life import GameOfLife, glider_pattern

# Verifica si está ejecutando con kernprof o no
try:
    profile
except NameError:
    def profile(func): return func

@profile
def run_simulation(size=512, steps=100):
    """
    Ejecuta el Juego de la Vida con un patrón glider y mide su rendimiento.
    Esta función puede ser analizada con line_profiler.
    """
    initial = glider_pattern(size)
    game = GameOfLife(rows=size, cols=size, initial_state=initial)
    game.run(steps)

if __name__ == "__main__":
    import time

    size = 512
    steps = 100

    print(f"▶️ Ejecutando simulación para size={size}, steps={steps}...")
    start_time = time.time()
    run_simulation(size, steps)
    duration = time.time() - start_time
    print(f"✅ Simulación completada en {duration:.4f} segundos.")