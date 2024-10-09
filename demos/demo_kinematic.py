import pygame
import sys
import os
import random
# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector import Vector
from images import cargar_imagenes
from kinematic import KinematicWander, KinematicArrive, KinematicFlee, KinematicSeek
from kinematic import Kinematic
from utils.utils import verificar_colisiones_con_bordes, actualizar_posicion_jugador

# Esta demo muestra cómo fueron implementados los comportamientos de Wander, Seek, Arrive y Flee
# en la clase Kinematic. Para ello, se crean varios personajes que se mueven de forma aleatoria,
# siguen al jugador, se acercan a él o se alejan de él, respectivamente.

# Función para inicializar el juego
def inicializar_juego():
    # Variables
    width, height = 1280, 720
    # Inicialización de Pygame y configuración de la pantalla
    pygame.init()
    pantalla = pygame.display.set_mode((width, height))
    return pantalla, width, height

def crear_personajes(width, height):
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
        wander_kinematic = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)
        wander_kinematics.append(wander_kinematic)

    seek_kinematic = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0)
    arrive_kinematic = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0)
    flee_kinematic = Kinematic(Vector(width // 2, height // 2), 0, Vector(0, 0), 0)

    # Asignar comportamientos
    wander_behaviors = [KinematicWander(wander_kinematic, maxSpeed=50, maxRotation=1) for wander_kinematic in wander_kinematics]
    seek_behavior = KinematicSeek(seek_kinematic, player_kinematic, maxSpeed=100)
    arrive_behavior = KinematicArrive(arrive_kinematic, player_kinematic, maxSpeed=10, radius=50)
    flee_behavior = KinematicFlee(flee_kinematic, player_kinematic, maxSpeed=40, fleeRadius=300)

    # Añadir los personajes a la lista de personajes
    personajes = [
        (wander_kinematics[i], wander_image, wander_behaviors[i]) for i in range(5)
    ] + [
        (seek_kinematic, seek_image, seek_behavior),
        (arrive_kinematic, arrive_image, arrive_behavior),
        (flee_kinematic, flee_image, flee_behavior),
        (player_kinematic, player_image, None)
    ]

    return background, frame, personajes, player_kinematic

# Función para el bucle principal del juego
def game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)
        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))
        # Actualizar la posición de los personajes -------------------------------------------
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

#  Ejecutar el demo de movimientos cinemáticos:
if __name__ == "__main__":
    pantalla, width, height = inicializar_juego()
    background, frame, personajes, player_kinematic = crear_personajes(width, height)
    game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, 60)