# Juego de la Vida de Conway

Este proyecto es una implementación del **Juego de la Vida**, un autómata celular propuesto por John Conway en 1970. Simula la evolución de una población en una grilla bidimensional, siguiendo reglas locales simples que producen comportamientos emergentes complejos.

---

## ¿Qué incluye este proyecto?

- Implementación orientada a objetos en Python (versión secuencial y paralela).
- Animaciones de patrones clásicos: **Glider**, **Blinker**, **Toad**, **Block**.
- Visualización de la evolución del sistema con `matplotlib.animation`.
- Pruebas de rendimiento empíricas variando el tamaño de la grilla.
- Análisis de rendimiento con `cProfile` y `line_profiler`.
- Gráficas de escalabilidad fuerte y débil.
- Análisis crítico y propuesta de mejoras.

---

## Requisitos

- Python 3.10 o superior
- Librerías:
  - `numpy`
  - `matplotlib`
  - `line_profiler`
  - `pillow`

### Instalación rápida

```bash
pip install -r requirements.txt
```

---

## Cómo ejecutar la simulación:

```bash
python game_of_life.py --pattern glider --size 64 --steps 100 --interval 200
```

Parámetros disponibles:

- `--pattern`: Patrón inicial (glider, blinker, toad, block)
- `--size`: Tamaño de la grilla (ej: 32, 128, 512)
- `--steps`: Número de generaciones
- `--interval`: Velocidad de la animación en milisegundos

---

## Visualización del rendimiento:

```bash
python graficos.py
```

Se generarán dos gráficas:

- Tiempo promedio por iteración según el tamaño de la grilla.
- Gráfica log-log comparando el rendimiento empírico con complejidades teóricas:
  - O(n)
  - O(n log n)
  - O(n²)

---

## Análisis con cProfile:

```bash
python profile_cprofile.py
```

Genera el archivo `profile_output.txt` y `game_profile.pstats`.

---

## Análisis con line_profiler:

```bash
kernprof -l -v profile_lineprofiler.py
```

Perfilado línea por línea del método `step()`.

---

## Versión paralela:

```bash
python parallel_game.py
```

Ejecuta el juego de la vida usando `multiprocessing` para acelerar el procesamiento.

---

## Capturas y animaciones:

Puedes guardar tus animaciones como GIF dentro de la carpeta `Capturas/`.

Ejemplo:
```python
ani.save("Capturas/glider.gif", writer='pillow')
```

---

## Resultados y conclusiones:

- El método `step()` es el cuello de botella principal.
- La complejidad empírica se alinea con O(n²).
- La paralelización mejora significativamente el rendimiento en grillas grandes.
- Las herramientas de perfilado ayudan a enfocar la optimización.

---

---

## Sophi nota para ejecutar los arquivos tienes que instalar esto primero 

Paso 1: Descargar Microsoft MPI

Descargá:
- Microsoft MPI Redistributable Package
- Microsoft MPI SDK

Están al final de la página, donde dice "Download MS-MPI vX.X".

⚙️ Paso 2: Instalar
- Ejecutá primero el .msi del Redistributable (esto te da el mpiexec y mpirun).
- Luego el .msi del SDK (opcional pero útil si programás en C/C++).

---

## Autores

- Gabriela Carvajal Herra
- Sophia Céspedes

Ingeniería en Ciencias de Datos — Universidad LEAD

---