from mpi4py import MPI
import numpy as np
import sys
import time

# Inicializar el comunicador
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Proceso raíz obtiene N desde la terminal
if rank == 0:
    if len(sys.argv) != 2:
        print("Uso: mpirun -np <numero de procesos> python estadisticas_mpi.py <tamaño del arreglo>")
        sys.exit(1)
    N = int(sys.argv[1])
    if N % size != 0:
        print(f"El tamaño del arreglo N={N} debe ser divisible entre el número de procesos={size}")
        sys.exit(1)
else:
    N = None

# MPI_Bcast: enviar N a todos los procesos
N = comm.bcast(N, root=0)

# Tamaño del subarreglo que cada proceso manejará
chunk_size = N // size


if rank == 0:
    data = np.random.uniform(0, 100, N).astype('f')  
else:
    data = None

# Crear buffer para recibir los subarreglos
sub_array = np.empty(chunk_size, dtype='f')

# MPI_Scatter: para distribuir partes del arreglo entre los procesos
comm.Scatter(data, sub_array, root=0)

# Cada proceso calcula min, max, promedio local
local_min = np.min(sub_array)
local_max = np.max(sub_array)
local_sum = np.sum(sub_array)
local_avg = local_sum / chunk_size

# MPI_Reduce: para calcular los valores globales
global_min = comm.reduce(local_min, op=MPI.MIN, root=0)
global_max = comm.reduce(local_max, op=MPI.MAX, root=0)
global_sum = comm.reduce(local_sum, op=MPI.SUM, root=0)

# El proceso raíz calcula promedio global e imprime los resultados
if rank == 0:
    global_avg = global_sum / N
    print("Resultados Estadísticos Globales:")
    print(f"Mínimo global:  {global_min:.4f}")
    print(f"Máximo global:  {global_max:.4f}")
    print(f"Promedio global: {global_avg:.4f}")
