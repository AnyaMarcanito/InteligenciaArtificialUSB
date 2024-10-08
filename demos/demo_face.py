import pygame
import sys
import os
import math

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from kinematic import Kinematic
from behaviors.face import Face
from images import cargar_imagenes
from utils.utils import actualizar_posicion_jugador

# Inicialización de Pygame y configuración de la pantalla
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))
pygame.display.set_caption("Demo Face Behavior")

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background2"]
player_image = imagenes["sakuraFlying"]
card_image = imagenes["clowCard"]
frame = imagenes["frame"]

# Crear el personaje del jugador
player_kinematic = Kinematic(Vector(600, 600), 0, Vector(0, 0), 0)

# Crear personajes adicionales cercanos a las esquinas
corner_positions = [
    Vector(200, 200),
    Vector(width - 200, 200),
    Vector(200, height - 200),
    Vector(width - 200, height - 200)
]
corner_kinematics = [Kinematic(pos, 0, Vector(0, 0), 0) for pos in corner_positions]

# Crear personajes adicionales
inner_positions = [
    Vector(width / 2, 100),         # Esquina Norte
    Vector(width / 2, height - 100), # Esquina Sur
    Vector(100, height / 2),         # Esquina Oeste
    Vector(width - 100, height / 2)  # Esquina Este
]
inner_kinematics = [Kinematic(pos, 0, Vector(0, 0), 0) for pos in inner_positions]

all_kinematics = corner_kinematics + inner_kinematics

# Crear comportamientos Face para todos los personajes adicionales
face_behaviors = [Face(kinematic, player_kinematic, maxAngularAcceleration=5, maxRotation=math.pi, targetRadius=0.1, slowRadius=math.pi / 4) for kinematic in all_kinematics]

# Función para rotar una imagen
def rotar_imagen(image, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=(0, 0)).center)
    return rotated_image, new_rect

# Función para dibujar un triángulo isósceles que representa al personaje
def dibujar_triangulo(pantalla, color, kinematic, size=10):
    # Calcular los vértices del triángulo isósceles
    p1 = (kinematic.position.x + size * math.cos(kinematic.orientation),
          kinematic.position.y + size * math.sin(kinematic.orientation))
    p2 = (kinematic.position.x + size * math.cos(kinematic.orientation + 5 * math.pi / 6),
          kinematic.position.y + size * math.sin(kinematic.orientation + 5 * math.pi / 6))
    p3 = (kinematic.position.x + size * math.cos(kinematic.orientation - 5 * math.pi / 6),
          kinematic.position.y + size * math.sin(kinematic.orientation - 5 * math.pi / 6))
    pygame.draw.polygon(pantalla, color, [p1, p2, p3])

# Iniciar el bucle del juego
def game_loop(pantalla, background, player_image, card_image, fps):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            actualizar_posicion_jugador(event, player_kinematic)

        # Actualizar el comportamiento de Face de todos los personajes adicionales
        for i, kinematic in enumerate(all_kinematics):
            steering = face_behaviors[i].getSteering()
            if steering:
                kinematic.update_with_steering(steering, maxSpeed=0, time=1/fps)

        pantalla.blit(background, (0, 0))
        pantalla.blit(frame, (0, 0))
        pantalla.blit(player_image, (player_kinematic.position.x - player_image.get_width() // 2, player_kinematic.position.y - player_image.get_height() // 2))

        # Dibujar los personajes adicionales con rotación
        for kinematic in all_kinematics:
            angle = -math.degrees(kinematic.orientation)
            rotated_image, new_rect = rotar_imagen(card_image, angle)
            pantalla.blit(rotated_image, (kinematic.position.x - new_rect.width // 2, kinematic.position.y - new_rect.height // 2))
            dibujar_triangulo(pantalla, (0, 0, 0), kinematic)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

# Ejecutar el bucle del juego
game_loop(pantalla, background, player_image, card_image, 60)