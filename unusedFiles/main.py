import pygame
from characters import crear_personaje
from vector import Vector
from images import cargar_imagenes
from game_loop import game_loop

# Inicialización de Pygame y creación de personajes
pygame.init()
width, height = 1280, 720
pantalla = pygame.display.set_mode((width, height))

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background"]

# Crear el personaje del jugador
player = crear_personaje(Vector(600, 600), Vector(0, 0), 'player', imagenes["sakuraFlying"])

# Crear otros personajes con jugador como objetivo
wander = crear_personaje(Vector(100, 100), Vector(0, 0), 'wander', imagenes["clowCard"])
seek = crear_personaje(Vector(200, 200), Vector(0, 0), 'seek', imagenes["yueFlying"], player)
arrive = crear_personaje(Vector(300, 300), Vector(0, 0), 'arrive', imagenes["eriolFlying"], player)
flee = crear_personaje(Vector(400, 400), Vector(0, 0), 'flee', imagenes["keroFlying"], player)
wander2 = crear_personaje(Vector(500, 500), Vector(0, 0), 'wander', imagenes["clowCard"])
align = crear_personaje(Vector(600, 100), Vector(0, 0), 'align', imagenes["spinelFlying"], player)  # Nueva instancia de align
clow = imagenes["clow"]

personajes = [wander, seek, arrive, flee, wander2, clow, align, player]

# Iniciar el bucle del juego
game_loop(pantalla, background, personajes, width, height, 50, 50, 60)