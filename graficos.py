import numpy as np
import matplotlib.pyplot as plt
import os

def graficar(tamanos, tiempos, titulo_extra=""):
    """
    Genera gráficos lineales y log-log comparando el tiempo empírico contra funciones teóricas.
    """
    teoricos = {
        "O(n)": tiempos[0] * (tamanos / tamanos[0]),
        "O(n log n)": tiempos[0] * (tamanos * np.log(tamanos) / (tamanos[0] * np.log(tamanos[0]))),
        "O(n²)": tiempos[0] * (tamanos**2 / tamanos[0]**2)
    }

    # Lineal
    plt.figure(figsize=(10, 5))
    plt.plot(tamanos, tiempos, 'o-', label='Empírico')
    for label, curve in teoricos.items():
        plt.plot(tamanos, curve, '--', label=label)
    plt.xlabel('n (lado de la grilla)')
    plt.ylabel('Tiempo medio por iteración (s)')
    plt.title(f'Rendimiento vs complejidad teórica {titulo_extra}')
    plt.grid(True)
    plt.legend()
    os.makedirs("Capturas", exist_ok=True)
    plt.savefig(f"Capturas/grafica_lineal{titulo_extra}.png")
    plt.show()

    # Log-Log
    plt.figure(figsize=(10, 5))
    plt.loglog(tamanos, tiempos, 'o-', label='Empírico')
    for label, curve in teoricos.items():
        plt.loglog(tamanos, curve, '--', label=label)
    plt.xlabel('n (log scale)')
    plt.ylabel('Tiempo medio (log scale)')
    plt.title(f'Complejidad empírica (log-log) {titulo_extra}')
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.savefig(f"Capturas/grafica_loglog{titulo_extra}.png")
    plt.show()

if __name__ == "__main__":
    # Verificación básica para evitar errores si los archivos no existen
    if os.path.exists("datos_tiempos.npy") and os.path.exists("datos_tamanos.npy"):
        tiempos = np.load("datos_tiempos.npy")
        tamanos = np.load("datos_tamanos.npy")
        graficar(tamanos, tiempos, titulo_extra="_MPI") 
    else:
        print("❌ No se encontraron archivos 'datos_tiempos.npy' y 'datos_tamanos.npy'.")