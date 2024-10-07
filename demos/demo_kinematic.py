import pygame
import sys
import os
import random

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from game_loop import game_loop
from kinematic import KinematicWander, KinematicArrive, KinematicFlee, KinematicSeek, KinematicSeekArrive
from kinematic import Kinematic

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
player_image = imagenes["sakuraFlying"]

# Crear otros personajes con jugador como objetivo
wander_kinematic1 = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
wander_kinematic2 = Kinematic(Vector(150, 150), 0, Vector(0, 0), 0)
wander_kinematic3 = Kinematic(Vector(200, 200), 0, Vector(0, 0), 0)
wander_kinematic4 = Kinematic(Vector(250, 250), 0, Vector(0, 0), 0)
wander_kinematic5 = Kinematic(Vector(300, 300), 0, Vector(0, 0), 0)
wander_image = imagenes["clowCard"]

seek_kinematic = Kinematic(Vector(350, 350), 0, Vector(0, 0), 0)
seek_image = imagenes["yueFlying"]

arrive_kinematic = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)
arrive_image = imagenes["eriolFlying"]

flee_kinematic = Kinematic(Vector(450, 450), 0, Vector(0, 0), 0)
flee_image = imagenes["keroFlying"]

# Nueva instancia para KinematicSeekArrive
seek_arrive_kinematic = Kinematic(Vector(500, 500), 0, Vector(0, 0), 0)
seek_arrive_image = imagenes["spinelFlying"]

# Asignar comportamientos
wander_behavior1 = KinematicWander(wander_kinematic1, maxSpeed=100, maxRotation=1)
wander_behavior2 = KinematicWander(wander_kinematic2, maxSpeed=100, maxRotation=1)
wander_behavior3 = KinematicWander(wander_kinematic3, maxSpeed=100, maxRotation=1)
wander_behavior4 = KinematicWander(wander_kinematic4, maxSpeed=100, maxRotation=1)
wander_behavior5 = KinematicWander(wander_kinematic5, maxSpeed=100, maxRotation=1)
seek_behavior = KinematicSeek(seek_kinematic, player_kinematic, maxSpeed=100)
arrive_behavior = KinematicArrive(arrive_kinematic, player_kinematic, maxSpeed=100, radius=80)
flee_behavior = KinematicFlee(flee_kinematic, player_kinematic, maxSpeed=80, fleeRadius=300)  # Ajustar fleeRadius
# seek_arrive_behavior = KinematicSeekArrive(seek_arrive_kinematic, player_kinematic, maxSpeed=100, arriveRadius=50)  # Ajustar arriveRadius

personajes = [
    (wander_kinematic1, wander_image, wander_behavior1),
    (wander_kinematic2, wander_image, wander_behavior2),
    (wander_kinematic3, wander_image, wander_behavior3),
    (wander_kinematic4, wander_image, wander_behavior4),
    (wander_kinematic5, wander_image, wander_behavior5),
    (seek_kinematic, seek_image, seek_behavior),
    (arrive_kinematic, arrive_image, arrive_behavior),
    (flee_kinematic, flee_image, flee_behavior),
    (player_kinematic, player_image, None)  # El jugador no tiene comportamiento
]

# Función para actualizar la posición del jugador con el mouse
def actualizar_posicion_jugador(evento, jugador):
    if evento.type == pygame.MOUSEMOTION:
        jugador.position = Vector(evento.pos[0], evento.pos[1])

# Función para verificar colisiones con los bordes de la pantalla
def verificar_colisiones_con_bordes(kinematic, width, height):
    if kinematic.position.x < 0:
        kinematic.position.x = 0
        kinematic.velocity.x = -kinematic.velocity.x
    elif kinematic.position.x > width:
        kinematic.position.x = width
        kinematic.velocity.x = -kinematic.velocity.x

    if kinematic.position.y < 0:
        kinematic.position.y = 0
        kinematic.velocity.y = -kinematic.velocity.y
    elif kinematic.position.y > height:
        kinematic.position.y = height
        kinematic.velocity.y = -kinematic.velocity.y

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

        # Dibujar el radio de fuga alrededor del jugador
        flee_radius = 300  # El mismo valor que se usa en KinematicFlee
        pygame.draw.circle(pantalla, (255, 0, 0), (int(player_kinematic.position.x), int(player_kinematic.position.y)), flee_radius, 1)

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update(steering, 1/fps)
            # Verificar colisiones solo para comportamientos de wandering
            if isinstance(behavior, KinematicWander):
                verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 60)