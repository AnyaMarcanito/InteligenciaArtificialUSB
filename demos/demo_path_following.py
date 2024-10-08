import pygame
import sys
import os
import math

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.path_following import FollowPath
from behaviors.path import Path
from utils.utils import verificar_colisiones_con_bordes

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background3"]
symbol_image = imagenes["symbol"]
frame = imagenes["frame"]

# Crear el personaje
character_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
character_image = imagenes["keroFollow"]

# Definir la ruta (circunferencia centrada)
circle_radius = 200
center_x, center_y = width // 2, height // 2
num_points = 100

path_points = [
    Vector(
        center_x + circle_radius * math.cos(2 * math.pi * i / num_points)-50,
        center_y + circle_radius * math.sin(2 * math.pi * i / num_points)
    )
    for i in range(num_points)
]

path = Path(path_points)

# Asignar el comportamiento FollowPath
path_following_behavior = FollowPath(character_kinematic, path, pathOffset=1, maxAcceleration=100)

personajes = [
    (character_kinematic, character_image, path_following_behavior)
]

# Iniciar el bucle del juego
def game_loop(pantalla, background, personajes, symbol_image, width, height, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))

        # Dibujar la imagen symbol en el centro de la ventana
        symbol_rect = symbol_image.get_rect(center=(width // 2 , height // 2 ))
        pantalla.blit(symbol_image, symbol_rect.topleft)

        for kinematic, image, behavior in personajes:
            if behavior:
                steering = behavior.getSteering()
                if steering:
                    kinematic.update_with_steering(steering, maxSpeed=50, time=1/fps)
            verificar_colisiones_con_bordes(kinematic, width, height)
            pantalla.blit(image, (kinematic.position.x, kinematic.position.y))

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, personajes, symbol_image, width, height, 60)