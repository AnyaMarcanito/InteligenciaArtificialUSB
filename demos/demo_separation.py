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
from behaviors.combine import CombinedBehavior
from utils.utils import actualizar_posicion_jugador, verificar_colisiones_con_bordes

# Esta demo muestra el comportamiento de Separation, que permite a los personajes mantener una
# distancia mínima entre ellos. En este caso, se crean varios personajes que siguen al jugador
# y evitan colisionar entre sí.

# Función para inicializar el juego
def inicializar_juego():
    pygame.init()
    width, height = 1270, 720
    pantalla = pygame.display.set_mode((width, height))
    imagenes = cargar_imagenes()
    background = imagenes["background6"]
    frame = imagenes["frame"]
    return pantalla, background, imagenes, width, height, frame

# Función para crear los personajes del juego
def crear_personajes(imagenes):
    player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)
    player_image = imagenes["sakuraFlying"]
    personajes = []
    # Crear otros personajes con jugador como objetivo
    for i in range(10):
        kinematic = Kinematic(Vector(random.randint(0, width), random.randint(0, height)), 0, Vector(0, 0), 0)
        image = imagenes["clowCard"]
        separation_behavior = Separation(kinematic, [p[0] for p in personajes if p[0] != kinematic], player_kinematic, maxAcceleration=1000, threshold=50, decayCoefficient=1)        
        arrive_behavior = Arrive(kinematic, player_kinematic, maxAcceleration=20, maxSpeed=500, targetRadius=50, slowRadius=200, timeToTarget=0.1)
        combined_behavior = CombinedBehavior([separation_behavior, arrive_behavior])
        personajes.append((kinematic, image, combined_behavior))
    # Añadir el jugador a la lista de personajes
    personajes.append((player_kinematic, player_image, None))
    return personajes, player_kinematic

#  Función para el bucle principal del juego
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
        #  Actualizar la posición de los personajes -------------------------------------------
        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed=100, time=1/fps)
            # Verificar colisiones
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

# Ejecutar demo para Separation
if __name__ == "__main__":
    pantalla, background, imagenes, width, height, frame = inicializar_juego()
    center_x, center_y = width // 2, height // 2
    personajes, player_kinematic = crear_personajes(imagenes)
    game_loop(pantalla, background, frame, personajes, player_kinematic, width, height, 60)