# Parte A: Operaciones Colectivas en MPI

## Descripción
Este programa en Python utiliza "mpi4py" para calcular estadísticas globales (mínimo, máximo y promedio) de un arreglo de números reales. Implementa las operaciones colectivas de MPI: "MPI_Bcast", "MPI_Scatter" y "MPI_Reduce".

## Requisitos

- Python 3.x
- mpi4py: pip install mpi4py
- Instalar MPI (por ejemplo, OpenMPI): brew install open-mpi

## Para correr el código

mpirun -np 4 python estadisticas_mpi.py 1000000

Donde 4 es el número de procesos y 1000000 es el tamaño total del arreglo. El valor debe ser divisible entre el número de procesos.

## Resultados

Resultados Estadísticos Globales:
Mínimo global:  0.0001
Máximo global:  99.9999
Promedio global: 49.9808

El uso de operaciones colectivas en MPI representa una forma más eficiente de coordinar la comunicación entre múltiples procesos en entornos de la computación paralela. 