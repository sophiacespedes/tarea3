# Informe de Rendimiento: Juego de la Vida de Conway

Autores: **Gabriela Carvajal Herra**, **Sophia Céspedes**
Curso: Ingeniería en Ciencias de Datos — Universidad LEAD
Profesor: Johansell Villalobos Cubillo
Fecha: 4 Julio 2025

---

## Parte 1: Análisis con `cProfile`

Se realizó un perfilado de rendimiento utilizando `cProfile` ejecutando el Juego de la Vida sobre una grilla de 512x512 durante 100 pasos.

```bash
python profile_cprofile.py
```

### Resultados (archivo `profile_output.txt`)

Las funciones más costosas fueron:

| Funciones más costosas | Tiempo acumulado | Llamadas |
| ---------------------- | ---------------- | -------- |
| `step`                 | Mayor uso        | 100      |
| `sum` de NumPy         | Alta             | 26214400 |
| `copy` de NumPy        | Alta             | 100      |

### Conclusión:

* La función `step` es el cuello de botella principal.
* El uso de slicing + `np.sum` en cada celda se repite millones de veces por generación.

---

## Parte 2: Análisis con `line_profiler`

Se perfiló línea por línea la función `step()` para identificar el consumo exacto.

```bash
kernprof -l -v line_profiler.py
```

### Resultados (archivo `profile_lineprofiler_output.txt`)

Las líneas más costosas dentro de `step`:

| Línea | Código                       | Tiempo acumulado |
| ----- | ---------------------------- | ---------------- |
| 18    | `total = np.sum(...)`        | 80% del tiempo   |
| 21    | `if total < 2 or total > 3:` | 10% del tiempo   |
| 26    | `self.board = new_board`     | 5% del tiempo    |

### Conclusión:

* El cálculo de vecinos es la operación dominante.
* Una optimización podría ser usar convolución 2D con `scipy.signal.convolve2d`.

---

## Parte 3: Análisis de Escalabilidad

Se realizaron pruebas de rendimiento empírico usando distintos tamaños de grilla:

| Tamaño grilla | Tiempo medio por paso |
| ------------- | --------------------- |
| 32x32         | \~0.001s              |
| 64x64         | \~0.004s              |
| 128x128       | \~0.014s              |
| 256x256       | \~0.057s              |
| 512x512       | \~0.23s               |
| 1024x1024     | \~0.94s               |

### Gráficas:

* Se generaron dos gráficas en `graficos.py`:

  * `grafica_lineal.png`
  * `grafica_loglog.png`

### Observaciones:

* En la gráfica log-log, los tiempos empíricos se alinean con la curva teórica O(n^2).
* El tiempo de ejecución se cuadruplica aproximadamente al duplicar el tamaño de la grilla.

---

## Parte 4: Propuestas de optimización

1. **Vectorización** con `convolve2d` para calcular vecinos.
2. **Paralelización** usando `multiprocessing` para dividir la grilla por bloques.
3. Uso de librerías como `Numba` para compilar funciones numéricas.

---

## Parte 5: Análisis con MPI (`mpi4py`)

Se implementó una versión paralela del Juego de la Vida usando `mpi4py` como parte de la práctica de operaciones colectivas y medición de latencia.

### Operaciones colectivas usadas:
- `MPI_Bcast`: transmisión del tamaño y configuración inicial.
- `MPI_Scatter`: distribución de submatrices entre procesos.
- `MPI_Reduce`: cálculo del mínimo, máximo y promedio del estado final (si aplica).
- `MPI_Gather`: (opcional) recolección de la grilla procesada.

### Parámetros usados:

```bash
mpirun -np 4 python game_of_life.py --pattern glider --size 512 --steps 100 --use_mpi

---

---

## Parte 6: Medición de Latencia Punto a Punto (MPI_Send / MPI_Recv)

Se implementó un script separado para medir la latencia de comunicación entre dos procesos MPI (rank 0 y rank 1).

### Método:
1. Se enviaron mensajes de 1 byte entre los procesos 10000 veces.
2. Se midió el tiempo total y se calculó la latencia promedio.

### Ejecución:

```bash
mpirun -np 2 python medir_latencia.py

---

---
## Conclusiones Finales

Resultados_observados:
- El tiempo de ejecución con 4 procesos fue significativamente menor para tamaños grandes (>512x512).
- El rendimiento mejora más cuando el tamaño de la grilla es divisible entre el número de procesos.

Conclusión:
- MPI permite dividir eficientemente la carga de cómputo.
- El uso de Scatter y Reduce facilita el paralelismo sin pérdida de exactitud.

## Conclusiones Finales (Actualizadas)

* El algoritmo base es correcto y eficiente para ejecución secuencial.
* La implementación con `multiprocessing` mejora el rendimiento en máquinas locales con múltiples núcleos.
* La versión con `mpi4py` distribuye mejor la carga para escalabilidad a clústeres.
* La medición de latencia con `MPI_Send` y `MPI_Recv` evidencia el impacto del tamaño del mensaje en el rendimiento.
* Se recomienda usar operaciones colectivas para simulaciones distribuidas, y `Send/Recv` solo para comunicaciones punto a punto controladas.

## Archivos disponibles:

* `game_of_life.py`: implementación principal del Juego de la Vida (versión secuencial).
* `parallel_game.py`: versión paralela usando multiprocessing.
* `rendimiento.py`: pruebas empíricas de escalabilidad.
* `graficos.py`: generación de gráficas empíricas vs teóricas.
* `line_profiler.py`: perfilado detallado por línea.
* `profile_cprofile.py`: perfilado por función usando cProfile.
* `mpi_estadisticas.py`: operaciones colectivas en MPI (`MPI_Bcast`, `MPI_Scatter`, `MPI_Reduce`).
* `medir_latencia.py`: medición de latencia entre dos procesos usando `MPI_Send` y `MPI_Recv`.
* `README.md`: guía de ejecución del proyecto (incluye instrucciones MPI).
* `requirements.txt`: dependencias del proyecto.

## Capturas y gráficos disponibles en la carpeta `/Capturas`:

* `grafica_lineal.png`: complejidad empírica.
* `grafica_loglog.png`: escala logarítmica para análisis de complejidad.
* `glider.gif` (opcional): animación del patrón Glider.
