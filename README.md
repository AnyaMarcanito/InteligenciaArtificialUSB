# InteligenciaArtificialUSB

## Descripción

Este proyecto presenta una serie de demostraciones de algoritmos de inteligencia artificial aplicados a la simulación de comportamientos de personajes en un entorno 2D. Los algoritmos implementados incluyen comportamientos cinemáticos, dinámicos, de variable matching, path following, separate y collision avoiding.

## Contenidos

Esta primera entrega de proyecto está organizado en varias demostraciones, cada una de las cuales ilustra un comportamiento específico:

1. **Comportamientos Cinemáticos**: Simulación de movimientos básicos utilizando algoritmos cinemáticos.
2. **Comportamientos Dinámicos**: Implementación de movimientos más complejos que consideran fuerzas y aceleraciones.
3. **Variable Matching**: Algoritmos que ajustan las variables de movimiento para lograr comportamientos deseados.
4. **Path Following**: Seguimiento de rutas predefinidas por los personajes.
5. **Separate**: Algoritmos que permiten a los personajes mantener una distancia adecuada entre sí.
6. **Collision Avoiding**: Comportamientos que evitan colisiones entre los personajes y con los obstáculos del entorno.
7. **Face**: Algoritmo para modificar la orientacion de los personajes para ver hacia un objetivo especifico.
8. **Evade, Pursue, Look where you're going** Algoritmos que permiten perseguir y evadir manteniendo la orientacion del personaje hacia donde se dirije.

## Uso

Cada demostración se puede ejecutar de manera independiente. A continuación se muestra cómo ejecutar cada una de ellas:

1. **Comportamientos Cinemáticos**:
    ```bash
    python demos/demo_kinematic.py
    ```

2. **Comportamientos Dinámicos**:
    ```bash
    python demos/demo_dynamic.py
    ```

3. **Variable Matching**:
    ```bash
    python demos/demo_variable_matching.py
    ```

4. **Path Following**:
    ```bash
    python demos/demo_path_following.py
    ```

5. **Separate**:
    ```bash
    python demos/demo_separate.py
    ```

6. **Collision Avoiding**:
    ```bash
    python demos/demo_collision_avoiding.py
    ```

7. **Face**:
    ```bash
    python demos/demo_face.py
    ```

8. **Evade, Pursue, Look where you're going**:
    ```bash
    python demos/demo_evade_pursue_look.py
    ```

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:
InteligenciaArtificialUSB/ │ 
├── behaviors/ # Implementaciones de los diferentes comportamientos 
├── demos/ # Scripts de demostración para cada comportamiento 
├── images/ # Imágenes utilizadas en las demostraciones 
├── utils/ # Utilidades y funciones auxiliares 
├── vector.py # Implementación de la clase Vector 
├── kinematic.py # Implementación de la clase Kinematic y sus derivados 
└── README.md # Este archivo 