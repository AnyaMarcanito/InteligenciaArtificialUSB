import pygame
import sys
import os
import math
import random
# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.face import Face
from utils.utils import actualizar_posicion_jugador

# Esta demo muestra cómo es el comportamiento de Face en varios personajes que siguen al jugador.
# Para ello, se crean varios personajes que siguen al jugador con un comportamiento de rotación en 
# posciones aleatorias de la pantalla.

# Función para inicializar el juego
def inicializar_juego():
    # Variables
    width, height = 1280, 720
    # Inicialización de Pygame y configuración de la pantalla
    pygame.init()
    pantalla = pygame.display.set_mode((width, height))
    return pantalla, width, height

# Función para cargar las imágenes y crear los personajes
def crear_personajes(width, height):
    # Cargar las imágenes
    imagenes = cargar_imagenes()
    background = imagenes["background4"]
    player_image = imagenes["sakuraFlying"]
    frame = imagenes["frame"]

    # Crear el personaje del jugador
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

    # Crear otros personajes con jugador como objetivo
    all_kinematics = []
    face_behaviors = []
    maxAngularAcceleration = 10
    maxRotation = 5
    targetRadius = 0.1
    slowRadius = 1

    # Crear personajes adicionales
    for i in range(10):
        kinematic = Kinematic(Vector(random.randint(0, width - 50), random.randint(0, height - 50)), 0, Vector(0, 0), 0)
        face_behavior = Face(kinematic, player_kinematic, maxAngularAcceleration, maxRotation, targetRadius, slowRadius)
        all_kinematics.append(kinematic)
        face_behaviors.append(face_behavior)

    return background, frame, player_image, player_kinematic, all_kinematics, face_behaviors

# Función para dibujar un triángulo isósceles
def dibujar_triangulo(pantalla, color, kinematic, size=15):
    angle = kinematic.orientation
    p1 = (kinematic.position.x + size * math.cos(angle), kinematic.position.y + size * math.sin(angle))
    p2 = (kinematic.position.x + size * math.cos(angle + 2.5), kinematic.position.y + size * math.sin(angle + 2.5))
    p3 = (kinematic.position.x + size * math.cos(angle - 2.5), kinematic.position.y + size * math.sin(angle - 2.5))
    pygame.draw.polygon(pantalla, color, [p1, p2, p3])

# Función para el bucle principal del juego
def game_loop(pantalla, background, frame, player_image, player_kinematic, all_kinematics, face_behaviors, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)
        # Actualizar el comportamiento -------------------------------------------
        for i, kinematic in enumerate(all_kinematics):
            steering = face_behaviors[i].getSteering()
            if steering:
                kinematic.update_with_steering(steering, maxSpeed=50, time=1/fps)

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))
        pantalla.blit(player_image, (player_kinematic.position.x - player_image.get_width() // 2, player_kinematic.position.y - player_image.get_height() // 2))
        for kinematic in all_kinematics:
            dibujar_triangulo(pantalla, (0, 0, 0), kinematic)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

# Ejecutar el demo de Face:
if __name__ == "__main__":
    pantalla, width, height = inicializar_juego()
    background, frame, player_image, player_kinematic, all_kinematics, face_behaviors = crear_personajes(width, height)
    game_loop(pantalla, background, frame, player_image, player_kinematic, all_kinematics, face_behaviors, 60)