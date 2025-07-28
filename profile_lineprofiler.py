import numpy as np
from game_of_life import GameOfLife, glider_pattern
from line_profiler import LineProfiler

def profile_step_function():
    size = 512
    steps = 100
    initial = glider_pattern(size)
    game = GameOfLife(rows=size, cols=size, initial_state=initial)

    lp = LineProfiler()
    lp.add_function(game.step)

    # Ejecutar profiling solo sobre game.step en el bucle
    lp.enable()
    for _ in range(steps):
        game.step()
    lp.disable()

    lp.print_stats()

if __name__ == "__main__":
    profile_step_function()