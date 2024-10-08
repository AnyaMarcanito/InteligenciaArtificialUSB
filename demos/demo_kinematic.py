import pygame
import sys
import os
import random

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from game_loop import game_loop
from kinematic import KinematicWander, KinematicArrive, KinematicFlee, KinematicSeek
from kinematic import Kinematic
from utils.utils import verificar_colisiones_con_bordes, actualizar_posicion_jugador

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
center_x, center_y = width // 2, height // 2
center = Vector(center_x, center_y)
flee_radius = 300
arrive_radius = 50
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background"]
frame = imagenes["frame"]
player_image = imagenes["sakuraFlying"]
wander_image = imagenes["clowCard"]
seek_image = imagenes["yueFlying"]
arrive_image = imagenes["eriolFlying"]
flee_image = imagenes["keroFlying"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

# Crear otros personajes con jugador como objetivo
wander_kinematics = []
for _ in range(5):
    random_x = random.randint(0, width - 1)
    random_y = random.randint(0, height - 1)
    wander_kinematic = Kinematic(Vector(random_x, random_y), 0, Vector(0, 0), 0)
    wander_kinematics.append(wander_kinematic)

seek_kinematic = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0)
arrive_kinematic = Kinematic(Vector(width-100, 0), 0, Vector(0, 0), 0)
flee_kinematic = Kinematic(center, 0, Vector(0, 0), 0)

# Asignar comportamientos
wander_kinematic1 = wander_kinematics[0]
wander_kinematic2 = wander_kinematics[1]
wander_kinematic3 = wander_kinematics[2]
wander_kinematic4 = wander_kinematics[3]
wander_kinematic5 = wander_kinematics[4]

wander_behavior1 = KinematicWander(wander_kinematic1, maxSpeed=50, maxRotation=1)
wander_behavior2 = KinematicWander(wander_kinematic2, maxSpeed=50, maxRotation=1)
wander_behavior3 = KinematicWander(wander_kinematic3, maxSpeed=50, maxRotation=1)
wander_behavior4 = KinematicWander(wander_kinematic4, maxSpeed=50, maxRotation=1)
wander_behavior5 = KinematicWander(wander_kinematic5, maxSpeed=50, maxRotation=1)
seek_behavior = KinematicSeek(seek_kinematic, player_kinematic, maxSpeed=40)
arrive_behavior = KinematicArrive(arrive_kinematic, player_kinematic, maxSpeed=40, radius=arrive_radius)
flee_behavior = KinematicFlee(flee_kinematic, player_kinematic, maxSpeed=40, fleeRadius=flee_radius)

personajes = [
    (wander_kinematic1, wander_image, wander_behavior1),
    (wander_kinematic2, wander_image, wander_behavior2),
    (wander_kinematic3, wander_image, wander_behavior3),
    (wander_kinematic4, wander_image, wander_behavior4),
    (wander_kinematic5, wander_image, wander_behavior5),
    (seek_kinematic, seek_image, seek_behavior),
    (arrive_kinematic, arrive_image, arrive_behavior),
    (flee_kinematic, flee_image, flee_behavior),
    (player_kinematic, player_image, None)
]

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

        # Dibujar el radio de fuga alrededor del jugador
        # pygame.draw.circle(pantalla, (0, 0, 0), (int(player_kinematic.position.x), int(player_kinematic.position.y)), flee_radius-50, 1)

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update(steering, 1/fps)
            # Verificar colisiones 
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 60)