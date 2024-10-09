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

# Esta demo muestra cómo se puede combinar el comportamiento de evasión de colisiones 
# con el comportamiento de diambulación para que los personajes eviten colisionar entre sí.
# Para ello, se crean varios personajes que se mueven aleatoriamente por la pantalla.

# Función para inicializar el juego
def inicializar_juego():
    # Variables
    width, height = 1270, 720
    # Inicialización de Pygame y configuración de la pantalla
    pygame.init()
    pantalla = pygame.display.set_mode((width, height))
    # Cargar las imágenes
    imagenes = cargar_imagenes()
    background = imagenes["background"]
    frame = imagenes["frame"]
    return pantalla, background, frame, imagenes, width, height

# Función para crear los personajes del juego
def crear_personajes(imagenes):
    personajes = []
    # Crear el personaje del jugador
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
    player_image = imagenes["sakuraFlying"]
    personajes.append((player_kinematic, player_image, None))

    # Crear otros personajes con jugador como objetivo
    for i in range(10):
        kinematic = Kinematic(Vector(center_x, center_y), 0, Vector(0, 0), 0)
        image = imagenes["clowCard"]
        # Combinar comportamientos de diambulación y evasión de colisiones
        wander_behavior = Wander(kinematic, wanderOffset=5, wanderRadius=10, wanderRate=1, maxAcceleration=1000)
        avoidance_behavior = CollisionAvoidance(kinematic, [p[0] for p in personajes if p[0] != kinematic], maxAcceleration=1000, radius=10)
        combined_behavior = CombinedBehavior([wander_behavior, avoidance_behavior])
        # Añadir el personaje a la lista de personajes
        personajes.append((kinematic, image, combined_behavior))
    return personajes, player_kinematic

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
        # Actualizar la posición de los personajes-------------------------------------------
        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed=80, time=1/fps)
            verificar_colisiones_con_bordes(kinematic, width-50, height-50)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

# Ejecutar el demo de evasión de colisiones:
if __name__ == "__main__":
    pantalla, background, frame, imagenes, width, height = inicializar_juego()
    center_x, center_y = width // 2, height // 2
    personajes, player_kinematic = crear_personajes(imagenes)
    game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, 60)