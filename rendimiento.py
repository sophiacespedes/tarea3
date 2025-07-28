import time
import numpy as np
from game_of_life import GameOfLife

def medir_rendimiento(tamanos, pasos=10):
    """
    Mide el tiempo promedio por paso para distintos tamaños de grilla.

    Parámetros:
    - tamanos: lista o array con tamaños de grilla (int)
    - pasos: número de generaciones a ejecutar por tamaño

    Retorna:
    - numpy array con tiempos promedio por paso para cada tamaño
    """
    tiempos = []

    for n in tamanos:
        juego = GameOfLife(rows=n, cols=n)
        start = time.perf_counter()
        juego.run(pasos)
        end = time.perf_counter()

        tiempo_promedio = (end - start) / pasos
        print(f"Tamaño: {n}x{n} | Tiempo promedio por paso: {tiempo_promedio:.6f} s")
        tiempos.append(tiempo_promedio)

    return np.array(tiempos)

if __name__ == "__main__":
    tamanos = [32, 64, 128, 256, 512, 1024]
    pasos = 10

    print("Iniciando medición de rendimiento...")
    tiempos = medir_rendimiento(tamanos, pasos=pasos)

    np.save("datos_tiempos.npy", tiempos)
    np.save("datos_tamanos.npy", np.array(tamanos))
    print("Medición completada. Datos guardados en 'datos_tiempos.npy' y 'datos_tamanos.npy'.")