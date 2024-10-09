import pygame
import sys
import os
import random

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.separation import Separation
from behaviors.arrive import Arrive
from behaviors.velocity_match import VelocityMatch
from behaviors.combine import CombinedBehavior
from utils.utils import actualizar_posicion_jugador, verificar_colisiones_con_bordes

def inicializar_juego():
    pygame.init()
    width, height = 1270, 720
    pantalla = pygame.display.set_mode((width, height))
    imagenes = cargar_imagenes()
    background = imagenes["background6"]
    return pantalla, background, imagenes, width, height

def crear_personajes(imagenes):
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
    player_image = imagenes["sakuraFlying"]
    personajes = []

    for i in range(10):
        kinematic = Kinematic(Vector(random.randint(0, width), random.randint(0, height)), 0, Vector(0, 0), 0)
        image = imagenes["clowCard"]
        separation_behavior = Separation(kinematic, [p[0] for p in personajes], player_kinematic, maxAcceleration=100, threshold=100, decayCoefficient=0.5)
        seek_behavior = Arrive(kinematic, player_kinematic, maxAcceleration=100, maxSpeed=80, targetRadius=100, slowRadius=200, timeToTarget=0.1)
        velocity_matching_behavior = VelocityMatch(kinematic, player_kinematic, maxAcceleration=100)
        combined_behavior = CombinedBehavior([separation_behavior, seek_behavior, velocity_matching_behavior])
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
                    kinematic.update_with_steering(steering, maxSpeed=100, time=1/fps)
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