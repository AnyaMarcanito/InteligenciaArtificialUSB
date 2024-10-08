import pygame
import sys
import os
import math
import random  # Importar el módulo random

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.face import Face
from utils.utils import actualizar_posicion_jugador

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
center_x, center_y = width // 2, height // 2
center = Vector(center_x, center_y)
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background4"]
player_image = imagenes["sakuraFlying"]
frame = imagenes["frame"]
sakura_card_image = imagenes["sakuraCard"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

# Crear otros personajes con jugador como objetivo
all_kinematics = []
face_behaviors = []
maxAngularAcceleration = 10
maxRotation = 5
targetRadius = 0.1
slowRadius = 1

for i in range(10):
    # Generar posiciones aleatorias dentro de los límites de la ventana
    random_x = random.randint(0, width - 50)
    random_y = random.randint(0, height - 50)
    kinematic = Kinematic(Vector(random_x, random_y), 0, Vector(0, 0), 0)
    face_behavior = Face(kinematic, player_kinematic, maxAngularAcceleration, maxRotation, targetRadius, slowRadius)
    all_kinematics.append(kinematic)
    face_behaviors.append(face_behavior)

# Función para dibujar un triángulo representando la orientación
def dibujar_triangulo(pantalla, color, kinematic, size=15):
    angle = kinematic.orientation
    p1 = (kinematic.position.x + size * math.cos(angle), kinematic.position.y + size * math.sin(angle))
    p2 = (kinematic.position.x + size * math.cos(angle + 2.5), kinematic.position.y + size * math.sin(angle + 2.5))
    p3 = (kinematic.position.x + size * math.cos(angle - 2.5), kinematic.position.y + size * math.sin(angle - 2.5))
    pygame.draw.polygon(pantalla, color, [p1, p2, p3])

# Iniciar el bucle del juego
def game_loop(pantalla, background, player_image, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        # Actualizar el comportamiento de Face de todos los personajes adicionales
        for i, kinematic in enumerate(all_kinematics):
            steering = face_behaviors[i].getSteering()
            if steering:
                kinematic.update_with_steering(steering, maxSpeed=0, time=1/fps)

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))
        pantalla.blit(player_image, (player_kinematic.position.x - player_image.get_width() // 2, player_kinematic.position.y - player_image.get_height() // 2))

        # Dibujar los personajes adicionales con rotación
        for kinematic in all_kinematics:
            dibujar_triangulo(pantalla, (0, 0, 0), kinematic)
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

game_loop(pantalla, background, player_image, 60)