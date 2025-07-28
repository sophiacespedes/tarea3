# mpi_estadisticas.py
from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def main():
    if len(sys.argv) != 2:
        if rank == 0:
            print("Uso: mpirun -np <n_procesos> python mpi_estadisticas.py <tamano_total>")
        exit()

    N = int(sys.argv[1])

    # Validar que el tamaño sea divisible entre los procesos
    if N % size != 0:
        if rank == 0:
            print(f"⚠️ El tamaño N={N} no es divisible entre {size} procesos.")
        exit()

    sub_N = N // size
    sub_arreglo = np.empty(sub_N, dtype='f')

    if rank == 0:
        arreglo_completo = np.random.uniform(0, 100, N).astype('f')
        print(f"[Proceso 0] Arreglo inicial (primeros 10): {arreglo_completo[:10]}")
    else:
        arreglo_completo = None

    # Enviar tamaño N a todos
    N = comm.bcast(N, root=0)

    # Scatter: dividir el arreglo
    comm.Scatter(arreglo_completo, sub_arreglo, root=0)

    # Cada proceso calcula sus estadísticas locales
    min_local = np.min(sub_arreglo)
    max_local = np.max(sub_arreglo)
    prom_local = np.mean(sub_arreglo)

    # Reduce: calcular valores globales
    min_global = comm.reduce(min_local, op=MPI.MIN, root=0)
    max_global = comm.reduce(max_local, op=MPI.MAX, root=0)
    prom_global = comm.reduce(prom_local, op=MPI.SUM, root=0)

    if rank == 0:
        prom_global /= size
        print(f"\n📊 Resultados Globales (usando MPI):")
        print(f"🔻 Mínimo: {min_global:.2f}")
        print(f"🔺 Máximo: {max_global:.2f}")
        print(f"📉 Promedio: {prom_global:.2f}")

if __name__ == "__main__":
    main()