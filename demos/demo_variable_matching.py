import pygame
import sys
import os

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.align import Align
from behaviors.velocity_match import VelocityMatch
from behaviors.face import Face
from behaviors.pursue import Pursue
from behaviors.evade import Evade
from behaviors.look_where_youre_going import LookWhereYoureGoing
from behaviors.seek import Seek
from behaviors.arrive import Arrive
from behaviors.combine import CombinedBehavior

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background3"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
player_image = imagenes["sakuraFlying"]

# Crear otros personajes con jugador como objetivo
align_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
align_image = imagenes["eriolFlying"]

velocity_match_kinematic = Kinematic(Vector(150, 150), 0, Vector(0, 0), 0)
velocity_match_image = imagenes["spinelFlying"]

face_kinematic = Kinematic(Vector(200, 200), 0, Vector(0, 0), 0)
face_image = imagenes["keroFlying"]

pursue_kinematic = Kinematic(Vector(250, 250), 0, Vector(0, 0), 0)
pursue_image = imagenes["yueFlying"]

evade_kinematic = Kinematic(Vector(300, 300), 0, Vector(0, 0), 0)
evade_image = imagenes["clowCard"]

look_where_youre_going_kinematic = Kinematic(Vector(350, 350), 0, Vector(0, 0), 0)
look_where_youre_going_image = imagenes["clowCard"]

# Asignar comportamientos
align_behavior = Align(align_kinematic, player_kinematic, maxAngularAcceleration=100, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.5)
seek_behavior = Seek(align_kinematic, player_kinematic, maxAcceleration=1000)
combined_behavior = CombinedBehavior([seek_behavior, align_behavior])

velocity_match_behavior = VelocityMatch(velocity_match_kinematic, player_kinematic, maxAcceleration=10)
face_behavior = Face(face_kinematic, player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)
pursue_behavior = Pursue(pursue_kinematic, player_kinematic, maxAcceleration=10, maxPrediction=1)
evade_behavior = Evade(evade_kinematic, player_kinematic, maxAcceleration=10, maxPrediction=1, fleeRadius=300)
look_where_youre_going_behavior = LookWhereYoureGoing(look_where_youre_going_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)

personajes = [
    (align_kinematic, align_image, combined_behavior),
    (velocity_match_kinematic, velocity_match_image, velocity_match_behavior),
    (face_kinematic, face_image, face_behavior),
    (pursue_kinematic, pursue_image, pursue_behavior),
    (evade_kinematic, evade_image, evade_behavior),
    (look_where_youre_going_kinematic, look_where_youre_going_image, look_where_youre_going_behavior),
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

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 60)