# medir_latencia.py
from mpi4py import MPI
import numpy as np
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def medir_latencia(N=10000, tamanio_mensaje=1):
    mensaje = np.zeros(tamanio_mensaje, dtype='b')

    if rank == 0:
        inicio = MPI.Wtime()
        for _ in range(N):
            comm.Send(mensaje, dest=1)
            comm.Recv(mensaje, source=1)
        fin = MPI.Wtime()

        tiempo_total = fin - inicio
        latencia_ida_y_vuelta = (tiempo_total / N) * 1e6  # microsegundos
        latencia_unidireccional = latencia_ida_y_vuelta / 2

        print(f"📨 Mensaje de {tamanio_mensaje} bytes transmitido {N} veces.")
        print(f"⏱️ Latencia promedio (ida y vuelta): {latencia_ida_y_vuelta:.3f} μs")
        print(f"➡️ Latencia estimada unidireccional: {latencia_unidireccional:.3f} μs")

    elif rank == 1:
        for _ in range(N):
            comm.Recv(mensaje, source=0)
            comm.Send(mensaje, dest=0)

if __name__ == "__main__":
    if comm.Get_size() != 2:
        if rank == 0:
            print("⚠️ Este script requiere exactamente 2 procesos (np=2).")
        exit()

    N = 10000
    tamanio_mensaje = 1 
    medir_latencia(N, tamanio_mensaje)