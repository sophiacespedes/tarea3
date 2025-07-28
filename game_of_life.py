from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

class GameOfLife:
    def __init__(self, rows, cols, initial_state=None):
        self.rows = rows
        self.cols = cols
        if initial_state is not None:
            self.board = np.array(initial_state)
        else:
            self.board = np.random.randint(2, size=(rows, cols))

    def step(self):
        new_board = np.copy(self.board)
        for i in range(self.rows):
            for j in range(self.cols):
                total = np.sum(
                    self.board[max(i-1, 0):min(i+2, self.rows),
                               max(j-1, 0):min(j+2, self.cols)]
                ) - self.board[i, j]

                if self.board[i, j] == 1:
                    if total < 2 or total > 3:
                        new_board[i, j] = 0
                else:
                    if total == 3:
                        new_board[i, j] = 1
        self.board = new_board

    def run(self, steps):
        for _ in range(steps):
            self.step()

    def get_state(self):
        return self.board

# === PATRONES ===
def glider_pattern(size=32):
    pattern = np.zeros((size, size), int)
    g = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
    pattern[1:4, 1:4] = g
    return pattern

def blinker_pattern(size=32):
    pattern = np.zeros((size, size), int)
    mid = size // 2
    pattern[mid, mid-1:mid+2] = 1
    return pattern

def toad_pattern(size=32):
    pattern = np.zeros((size, size), int)
    mid = size // 2
    pattern[mid, mid-2:mid+1] = 1
    pattern[mid+1, mid-1:mid+2] = 1
    return pattern

def block_pattern(size=32):
    pattern = np.zeros((size, size), int)
    mid = size // 2
    pattern[mid:mid+2, mid:mid+2] = 1
    return pattern

# === MPI RUNNER ===
def mpi_game_of_life(initial_board, steps):
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    rows = initial_board.shape[0]
    if rows % size != 0:
        if rank == 0:
            print(f"El número de filas ({rows}) debe ser divisible entre procesos ({size})")
        return

    local_rows = rows // size
    local_board = np.empty((local_rows, rows), dtype=int)

    # Scatter la matriz
    comm.Scatter(initial_board, local_board, root=0)

    local_game = GameOfLife(local_rows, rows, initial_state=local_board)

    for _ in range(steps):
        local_game.step()

    # Gather resultados
    final_board = None
    if rank == 0:
        final_board = np.empty((rows, rows), dtype=int)
    comm.Gather(local_game.get_state(), final_board, root=0)

    return final_board if rank == 0 else None

# === ANIMACIÓN ===
def animate_game(game, steps=100, interval=200):
    fig, ax = plt.subplots()
    img = ax.imshow(game.get_state(), cmap='binary', interpolation='nearest')

    def update(_):
        game.step()
        img.set_data(game.get_state())
        return [img]

    ani = animation.FuncAnimation(fig, update, frames=steps, interval=interval, blit=True)
    plt.show()

# === MAIN ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Juego de la Vida de Conway con o sin MPI")
    parser.add_argument("--pattern", choices=["glider", "blinker", "toad", "block"], default="glider")
    parser.add_argument("--size", type=int, default=32)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--interval", type=int, default=200)
    parser.add_argument("--use_mpi", action="store_true", help="Usar MPI para ejecución paralela")

    args = parser.parse_args()

    patterns = {
        "glider": glider_pattern,
        "blinker": blinker_pattern,
        "toad": toad_pattern,
        "block": block_pattern
    }

    initial = patterns[args.pattern](args.size)

    if args.use_mpi:
        result = mpi_game_of_life(initial, args.steps)
        if MPI.COMM_WORLD.Get_rank() == 0:
            print("Simulación finalizada en paralelo.")
            print(result)
    else:
        game = GameOfLife(rows=args.size, cols=args.size, initial_state=initial)
        animate_game(game, steps=args.steps, interval=args.interval)