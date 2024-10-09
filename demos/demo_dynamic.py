import pygame
import sys
import os
import random
import math

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.wander import Wander
from behaviors.seek import Seek
from behaviors.arrive import Arrive
from behaviors.flee import Flee
from utils.utils import verificar_colisiones_con_bordes, actualizar_posicion_jugador

def inicializar_juego():
    # Inicialización de Pygame y configuración de la pantalla
    pygame.init()
    width, height = 1280, 720
    pantalla = pygame.display.set_mode((width, height))
    return pantalla, width, height

def crear_personajes(width, height):
    # Cargar las imágenes
    imagenes = cargar_imagenes()
    background2 = imagenes["background2"]
    frame = imagenes["frame"]
    player_image = imagenes["sakuraFlying"]
    wander_image_light = imagenes["clowCardTheLight"]
    wander_image_dark = imagenes["clowCardTheDark"]
    wander_image_shadow = imagenes["clowCardTheShadow"]
    wander_image_sleep = imagenes["clowCardTheSleep"]
    wander_image_flower = imagenes["clowCardTheFlower"]
    seek_image = imagenes["yueFlying"]
    arrive_image = imagenes["eriolFlying"]
    flee_image = imagenes["keroFlying"]

    # Crear el personaje del jugador
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

    # Crear otros personajes con jugador como objetivo
    wander_kinematic_light = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)
    wander_kinematic_dark = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)
    wander_kinematic_shadow = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)
    wander_kinematic_sleep = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)
    wander_kinematic_flower = Kinematic(Vector(random.randint(0, width - 1), random.randint(0, height - 1)), 0, Vector(0, 0), 0)

    seek_kinematic = Kinematic(Vector(350, 350), 0, Vector(0, 0), 0)
    arrive_kinematic = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)
    flee_kinematic = Kinematic(Vector(450, 450), 0, Vector(0, 0), 0)

    # Asignar comportamientos
    wander_behavior_light = Wander(wander_kinematic_light, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
    wander_behavior_dark = Wander(wander_kinematic_dark, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
    wander_behavior_shadow = Wander(wander_kinematic_shadow, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
    wander_behavior_sleep = Wander(wander_kinematic_sleep, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
    wander_behavior_flower = Wander(wander_kinematic_flower, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=100)
    seek_behavior = Seek(seek_kinematic, player_kinematic, maxAcceleration=100)
    arrive_behavior = Arrive(arrive_kinematic, player_kinematic, maxAcceleration=100, maxSpeed=50, targetRadius=10, slowRadius=50)
    flee_behavior = Flee(flee_kinematic, player_kinematic, maxAcceleration=80, fleeRadius=300)

    personajes = [
        (wander_kinematic_light, wander_image_light, wander_behavior_light),
        (wander_kinematic_dark, wander_image_dark, wander_behavior_dark),
        (wander_kinematic_shadow, wander_image_shadow, wander_behavior_shadow),
        (wander_kinematic_sleep, wander_image_sleep, wander_behavior_sleep),
        (wander_kinematic_flower, wander_image_flower, wander_behavior_flower),
        (seek_kinematic, seek_image, seek_behavior),
        (arrive_kinematic, arrive_image, arrive_behavior),
        (flee_kinematic, flee_image, flee_behavior),
        (player_kinematic, player_image, None) 
    ]

    return background2, frame, personajes, player_kinematic

def dibujar_triangulo(pantalla, color, kinematic, size=15):
    angle = kinematic.orientation
    p1 = (kinematic.position.x + size * math.cos(angle), kinematic.position.y + size * math.sin(angle))
    p2 = (kinematic.position.x + size * math.cos(angle + 2.5), kinematic.position.y + size * math.sin(angle + 2.5))
    p3 = (kinematic.position.x + size * math.cos(angle - 2.5), kinematic.position.y + size * math.sin(angle - 2.5))
    pygame.draw.polygon(pantalla, color, [p1, p2, p3])

def game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, fps):
    clock = pygame.time.Clock()
    running = True
    maxSpeed = 200

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed, 1/fps)
            # Verificar colisiones
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))
            if isinstance(behavior, Wander):
                dibujar_triangulo(pantalla, (0, 0, 0), kinematic)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    pantalla, width, height = inicializar_juego()
    background, frame, personajes, player_kinematic = crear_personajes(width, height)
    game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, 60)