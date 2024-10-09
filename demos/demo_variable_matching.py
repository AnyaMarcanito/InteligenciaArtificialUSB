import pygame
import sys
import os
import math
# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.align import Align
from behaviors.velocity_match import VelocityMatch
from behaviors.seek import Seek
from behaviors.arrive import Arrive
from behaviors.combine import CombinedBehavior
from utils.utils import verificar_colisiones_con_bordes, actualizar_posicion_jugador

# Esta demo muestra cómo se pueden combinar varios comportamientos para que los personajes
# realicen diferentes acciones en función de la situación. En este caso, se crean varios
# personajes que siguen al jugador, usando dos combinaciones de comportamientos: Align y 
# Velocity Match.

# Función para inicializar el juego
def inicializar_juego():
    # Variables
    width, height = 1280, 720
    # Inicialización de Pygame y configuración de la pantalla
    pygame.init()
    pantalla = pygame.display.set_mode((width, height))
    return pantalla, width, height

# Función para cargar las imágenes y crear los personajes
def crear_personajes():
    # Cargar las imágenes
    imagenes = cargar_imagenes()
    background = imagenes["background3"]
    frame = imagenes["frame"]

    # Crear el personaje del jugador
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
    player_image = imagenes["sakuraFlying"]

    # Crear otros personajes con jugador como objetivo
    align_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
    align_image = imagenes["eriolFlying"]

    velocity_match_kinematic = Kinematic(Vector(150, 150), 0, Vector(0, 0), 0)
    velocity_match_image = imagenes["spinelFlying"]

    # Asignar comportamientos
    # Eriol
    align_behavior = Align(align_kinematic, player_kinematic, maxAngularAcceleration=100, maxRotation=5, targetRadius=0.1, slowRadius=1, timeToTarget=0.5)
    seek_behavior = Seek(align_kinematic, player_kinematic, maxAcceleration=100)
    combined_behavior_align = CombinedBehavior([seek_behavior, align_behavior])

    # Spinel
    velocity_match_behavior_2 = VelocityMatch(velocity_match_kinematic, player_kinematic, maxAcceleration=100)
    arrive_behavior_2 = Arrive(velocity_match_kinematic, player_kinematic, maxAcceleration=100, maxSpeed=500, targetRadius=0.1, slowRadius=1, timeToTarget=0.5)
    combined_behavior_velocity_match = CombinedBehavior([velocity_match_behavior_2, arrive_behavior_2])

    personajes = [
        (align_kinematic, align_image, combined_behavior_align),
        (velocity_match_kinematic, velocity_match_image, combined_behavior_velocity_match),
        (player_kinematic, player_image, None)
    ]
    return background, frame, personajes, player_kinematic

# Funcion para dibujar triangulos
def dibujar_triangulo(pantalla, color, kinematic, size=10):
    # Calcular los vértices del triángulo isósceles
    p1 = (kinematic.position.x + size * math.cos(kinematic.orientation),
          kinematic.position.y + size * math.sin(kinematic.orientation))
    p2 = (kinematic.position.x + size * math.cos(kinematic.orientation + 5 * math.pi / 6),
          kinematic.position.y + size * math.sin(kinematic.orientation + 5 * math.pi / 6))
    p3 = (kinematic.position.x + size * math.cos(kinematic.orientation - 5 * math.pi / 6),
          kinematic.position.y + size * math.sin(kinematic.orientation - 5 * math.pi / 6))
    pygame.draw.polygon(pantalla, color, [p1, p2, p3])

# Función para el bucle principal del juego
def game_loop(pantalla, background, frame, personajes, width, height, fps, player_kinematic):
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
                    kinematic.update_with_steering(steering, maxSpeed=100, time=1/fps)
            # Verificar colisiones
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x - image.get_width() // 2, kinematic.position.y - image.get_height() // 2))
            dibujar_triangulo(pantalla, (0, 0, 0), kinematic)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

# Ejecutamos la demo de los comportamientos Align y Velocity Match
if __name__ == "__main__":
    pantalla, width, height = inicializar_juego()
    background, frame, personajes, player_kinematic = crear_personajes()
    game_loop(pantalla, background, frame, personajes, width, height, 60, player_kinematic)
