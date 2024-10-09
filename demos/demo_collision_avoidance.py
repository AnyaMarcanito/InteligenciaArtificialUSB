import pygame
import sys
import os

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.collision_avoidance import CollisionAvoidance
from behaviors.wander import Wander
from behaviors.combine import CombinedBehavior
from utils.utils import actualizar_posicion_jugador, verificar_colisiones_con_bordes

def inicializar_juego():
    pygame.init()
    width, height = 1270, 720
    pantalla = pygame.display.set_mode((width, height))
    imagenes = cargar_imagenes()
    background = imagenes["background"]
    return pantalla, background, imagenes, width, height

def crear_personajes(imagenes):
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
    player_image = imagenes["sakuraFlying"]
    personajes = []

    for i in range(10):
        kinematic = Kinematic(Vector(center_x, center_y), 0, Vector(0, 0), 0)
        image = imagenes["clowCard"]
        wander_behavior = Wander(kinematic, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=1000)
        avoidance_behavior = CollisionAvoidance(kinematic, [p[0] for p in personajes], maxAcceleration=1000, radius=10)
        combined_behavior = CombinedBehavior([wander_behavior, avoidance_behavior])
        personajes.append((kinematic, image, combined_behavior))

    personajes.append((player_kinematic, player_image, None))
    return personajes, player_kinematic

def game_loop(pantalla, background, personajes, player_kinematic, width, height, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        pantalla.blit(background, (0, 0))

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed=80, time=1/fps)
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    pantalla, background, imagenes, width, height = inicializar_juego()
    center_x, center_y = width // 2, height // 2
    personajes, player_kinematic = crear_personajes(imagenes)
    game_loop(pantalla, background, personajes, player_kinematic, width, height, 60)