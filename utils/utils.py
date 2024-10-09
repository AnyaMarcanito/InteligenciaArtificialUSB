import math
import pygame
from vector import Vector

# Función para mapear un valor a un rango específico (entre -pi y pi)
def mapToRange(rotation):
    rotation = rotation % (2 * math.pi)
    if rotation > math.pi:
        rotation -= 2 * math.pi
    return rotation

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