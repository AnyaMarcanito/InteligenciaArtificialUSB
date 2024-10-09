import pygame
import sys
import os
import math

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.pursue import Pursue
from behaviors.evade import Evade
from behaviors.look_where_youre_going import LookWhereYoureGoing
from behaviors.combine import CombinedBehavior
from utils.utils import verificar_colisiones_con_bordes, actualizar_posicion_jugador

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background5"]
frame = imagenes["frame"]
player_image = imagenes["sakuraFlying"]
pursue_image = imagenes["keroFollow"]
evade_image = imagenes["spinelFlying"]
new_pursue_image = imagenes["sakuraFlying2"]
new_evade_image = imagenes["sakuraCard"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

pursue_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
evade_kinematic = Kinematic(Vector(300, 300), 0, Vector(0, 0), 0)

# Crear nuevas instancias de Kinematic
new_pursue_kinematic = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0)
new_evade_kinematic = Kinematic(Vector(200, 200), 0, Vector(0, 0), 0)

# Asignar comportamientos de movimiento
pursue_behavior = Pursue(pursue_kinematic, player_kinematic, maxAcceleration=500, maxPrediction=100)
evade_behavior = Evade(evade_kinematic, player_kinematic, maxAcceleration=500, maxPrediction=100, fleeRadius=300)
new_pursue_behavior = Pursue(new_pursue_kinematic, new_evade_kinematic, maxAcceleration=500, maxPrediction=0.5)
new_evade_behavior = Evade(new_evade_kinematic, new_pursue_kinematic, maxAcceleration=500, maxPrediction=0.5, fleeRadius=300)

# Asignar comportamientos de orientación
pursue_look_behavior = LookWhereYoureGoing(pursue_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, maxSpeed=100, timeToTarget=0.1)
evade_look_behavior = LookWhereYoureGoing(evade_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, maxSpeed=100, timeToTarget=0.1)
new_pursue_look_behavior = LookWhereYoureGoing(new_pursue_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, maxSpeed=100, timeToTarget=0.1)
new_evade_look_behavior = LookWhereYoureGoing(new_evade_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, maxSpeed=100, timeToTarget=0.1)

# Combinar comportamientos de movimiento y orientación
pursue_combined_behavior = CombinedBehavior([pursue_behavior, pursue_look_behavior])
evade_combined_behavior = CombinedBehavior([evade_behavior, evade_look_behavior])
new_pursue_combined_behavior = CombinedBehavior([new_pursue_behavior, new_pursue_look_behavior])
new_evade_combined_behavior = CombinedBehavior([new_evade_behavior, new_evade_look_behavior])

personajes = [
    (pursue_kinematic, pursue_image, pursue_combined_behavior, '#ffb700'),
    (evade_kinematic, evade_image, evade_combined_behavior, '#0e1cb1'),
    (new_pursue_kinematic, new_pursue_image, new_pursue_combined_behavior, (0, 0, 255)),
    (new_evade_kinematic, new_evade_image, new_evade_combined_behavior, '#ff00d9'), 
    (player_kinematic, player_image, None, None) 
]

# Función para dibujar un triángulo isósceles
def dibujar_triangulo(pantalla, color, kinematic):
    # Si el color es None, no dibujar nada
    if color is None:
        return

    x, y = kinematic.position.x, kinematic.position.y
    orientation = kinematic.orientation

    # Definir los vértices del triángulo
    size = 20
    half_size = size / 2
    points = [
        (x + math.cos(orientation) * size, y + math.sin(orientation) * size),
        (x + math.cos(orientation + 2.5) * half_size, y + math.sin(orientation + 2.5) * half_size),
        (x + math.cos(orientation - 2.5) * half_size, y + math.sin(orientation - 2.5) * half_size)
    ]

    # Dibujar el triángulo
    pygame.draw.polygon(pantalla, color, points)

# Iniciar el bucle del juego
def game_loop(pantalla, background, personajes, width, height, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))

        for kinematic, image, behavior, color in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed=500, time=1/fps)  # Asegúrate de pasar maxSpeed
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))
            dibujar_triangulo(pantalla, color, kinematic)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 60)