import pygame
import sys
import os

# Añadir el directorio principal al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from vector import Vector
from images import cargar_imagenes
from kinematic import Kinematic
from behaviors.pursue import Pursue
from behaviors.evade import Evade

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
pursue_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
pursue_image = imagenes["keroFollow"]

evade_kinematic = Kinematic(Vector(300, 300), 0, Vector(0, 0), 0)
evade_image = imagenes["spinelFlying"]

# Crear nuevas instancias de Kinematic
new_pursue_kinematic = Kinematic(Vector(200, 200), 0, Vector(0, 0), 0)
new_pursue_image = imagenes["sakuraFlying2"]

new_evade_kinematic = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)
new_evade_image = imagenes["sakuraCard"]

# Asignar comportamientos
pursue_behavior = Pursue(pursue_kinematic, player_kinematic, maxAcceleration=1000, maxPrediction=100)
evade_behavior = Evade(evade_kinematic, player_kinematic, maxAcceleration=1000, maxPrediction=100, fleeRadius=300)

# Asignar nuevos comportamientos
new_pursue_behavior = Pursue(new_pursue_kinematic, new_evade_kinematic, maxAcceleration=500, maxPrediction=0.5)
new_evade_behavior = Evade(new_evade_kinematic, new_pursue_kinematic, maxAcceleration=500, maxPrediction=0.5, fleeRadius=300)
personajes = [
    (pursue_kinematic, pursue_image, pursue_behavior),
    (evade_kinematic, evade_image, evade_behavior),
    (new_pursue_kinematic, new_pursue_image, new_pursue_behavior),
    (new_evade_kinematic, new_evade_image, new_evade_behavior),
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

        # Dibujar el círculo alrededor del jugador
        pygame.draw.circle(pantalla, (255, 0, 0), (int(player_kinematic.position.x), int(player_kinematic.position.y)), 300, 1)

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