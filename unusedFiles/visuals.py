import pygame

def inicializar_pygame():
    pygame.init()

def configurar_pantalla(width, height, titulo):
    pantalla = pygame.display.set_mode((width, height))
    pygame.display.set_caption(titulo)
    return pantalla

def cargar_imagen(ruta, width=None, height=None):
    imagen = pygame.image.load(ruta)
    if width and height:
        imagen = pygame.transform.scale(imagen, (width, height))
    return imagen

def obtener_tamano_imagen(imagen):
    return imagen.get_width(), imagen.get_height()

def verificar_colisiones(kinematic, width, height, image_width, image_height):
    if kinematic.position.x < 0 or kinematic.position.x > width - image_width:
        kinematic.velocity.x = -kinematic.velocity.x
        kinematic.position.x = max(0, min(kinematic.position.x, width - image_width))

    if kinematic.position.y < 0 or kinematic.position.y > height - image_height:
        kinematic.velocity.y = -kinematic.velocity.y
        kinematic.position.y = max(0, min(kinematic.position.y, height - image_height))