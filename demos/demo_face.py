import pygame
import sys
import os

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.face import Face
from behaviors.pursue import Pursue
from behaviors.combine import CombinedBehavior

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background4"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
player_image = imagenes["sakuraFlying"]

# Crear personajes que usarán los comportamientos Face y Pursue
face_kinematics = [
    Kinematic(Vector(0, 0), 0, Vector(0, 0), 0),
    Kinematic(Vector(1200, 650), 0, Vector(0, 0), 0),
    Kinematic(Vector(0, 650), 0, Vector(0, 0), 0),
    Kinematic(Vector(1200, 0), 0, Vector(0, 0), 0),
    Kinematic(Vector(1200, 300), 0, Vector(0, 0), 0)
]

face_images = [
    imagenes["yueFlying"],
    imagenes["yueFlying"],
    imagenes["yueFlying"],
    imagenes["yueFlying"],
    imagenes["yueFlying"]
]

face_behaviors = [
    CombinedBehavior([Pursue(face_kinematics[0], player_kinematic, maxAcceleration=100, maxPrediction=1), Face(face_kinematics[0], player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)]),
    CombinedBehavior([Pursue(face_kinematics[1], player_kinematic, maxAcceleration=100, maxPrediction=1), Face(face_kinematics[1], player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)]),
    CombinedBehavior([Pursue(face_kinematics[2], player_kinematic, maxAcceleration=100, maxPrediction=1), Face(face_kinematics[2], player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)]),
    CombinedBehavior([Pursue(face_kinematics[3], player_kinematic, maxAcceleration=100, maxPrediction=1), Face(face_kinematics[3], player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)]),
    CombinedBehavior([Pursue(face_kinematics[4], player_kinematic, maxAcceleration=100, maxPrediction=1), Face(face_kinematics[4], player_kinematic, maxAngularAcceleration=10, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.1)])
]

personajes = [
    (face_kinematics[0], face_images[0], face_behaviors[0]),
    (face_kinematics[1], face_images[1], face_behaviors[1]),
    (face_kinematics[2], face_images[2], face_behaviors[2]),
    (face_kinematics[3], face_images[3], face_behaviors[3]),
    (face_kinematics[4], face_images[4], face_behaviors[4]),
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
                    kinematic.update_with_steering(steering, maxSpeed=500, time=1/fps)  # Asegúrate de pasar maxSpeed
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 60)