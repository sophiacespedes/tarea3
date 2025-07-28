import numpy as np
import multiprocessing as mp


class ParallelGameOfLife:
    def __init__(self, rows, cols, initial_state=None):
        self.rows = rows
        self.cols = cols
        if initial_state is not None:
            self.board = initial_state
        else:
            self.board = np.random.randint(2, size=(rows, cols), dtype=np.int8)

    def _update_chunk(self, args):
        """
        Calcula la siguiente generación para un subconjunto de filas.
        Usa condiciones de frontera toroidales (bordes envolventes).
        """
        chunk_start, chunk_end, board = args
        new_chunk = np.zeros((chunk_end - chunk_start, self.cols), dtype=np.int8)

        # Para evitar copiar bordes, obtenemos las filas una más arriba y abajo (con wrap)
        extended_rows = np.arange(chunk_start - 1, chunk_end + 1) % self.rows

        # Extraemos la porción extendida del tablero para calcular vecinos
        board_chunk = board[extended_rows, :]

        for i_local, i_global in enumerate(range(chunk_start, chunk_end)):
            for j in range(self.cols):
                # Índices con wrap para columnas
                left = (j - 1) % self.cols
                right = (j + 1) % self.cols

                # Suma de los 8 vecinos con envoltura
                total = (
                    board_chunk[i_local, left] + board_chunk[i_local, right] +
                    board_chunk[i_local + 1, left] + board_chunk[i_local + 1, j] + board_chunk[i_local + 1, right] +
                    board_chunk[i_local + 2, left] + board_chunk[i_local + 2, j] + board_chunk[i_local + 2, right]
                )

                if board_chunk[i_local + 1, j] == 1:
                    # Regla de supervivencia
                    if total < 2 or total > 3:
                        new_chunk[i_local, j] = 0
                    else:
                        new_chunk[i_local, j] = 1
                else:
                    # Regla de nacimiento
                    if total == 3:
                        new_chunk[i_local, j] = 1
                    else:
                        new_chunk[i_local, j] = 0

        return new_chunk

    def step(self):
        """
        Ejecuta un paso del juego dividiendo el tablero en trozos
        que se actualizan en paralelo usando multiprocessing.Pool.
        """
        num_processes = min(mp.cpu_count(), self.rows)
        chunk_size = self.rows // num_processes

        # Crear tareas con (inicio, fin, tablero)
        tasks = []
        for i in range(num_processes):
            start = i * chunk_size
            # Asegurar que la última tarea tome cualquier resto
            end = (i + 1) * chunk_size if i != num_processes - 1 else self.rows
            tasks.append((start, end, self.board))

        with mp.Pool(processes=num_processes) as pool:
            chunks = pool.map(self._update_chunk, tasks)

        # Concatenar resultados verticalmente
        self.board = np.vstack(chunks)

    def run(self, steps):
        """
        Ejecuta varias generaciones del juego.
        """
        for _ in range(steps):
            self.step()

    def get_state(self):
        return self.board


if __name__ == "__main__":
    from game_of_life import glider_pattern
    import time

    size = 512
    steps = 100
    initial = glider_pattern(size)
    game = ParallelGameOfLife(rows=size, cols=size, initial_state=initial)

    print(f"▶️ Ejecutando Game of Life paralelo con size={size}, steps={steps}")
    start = time.perf_counter()
    game.run(steps)
    end = time.perf_counter()
    print(f"✅ Tiempo total (paralelo): {end - start:.4f} segundos")