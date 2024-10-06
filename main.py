from visuals import inicializar_pygame, configurar_pantalla, obtener_tamano_imagen
from images import cargar_imagenes
from game_loop import game_loop
from characters import crear_personaje
from vector import Vector

# Inicialización de Pygame
inicializar_pygame()

# Configuración de la pantalla y el reloj
width, height = 800, 600
pantalla = configurar_pantalla(width, height, 'Cardcaptor Sakura')
FPS = 60

# Cargar las imágenes
imagenes = cargar_imagenes()
background = imagenes["background"]
sakuraFlying = imagenes["sakuraFlying"]
sakuraSeek = imagenes["sakuraSeek"]
sakuraArrive = imagenes["sakuraArrive"]
sakuraFlee = imagenes["sakuraFlee"]
clowCard = imagenes["clowCard"]

# Obtener el tamaño de las imágenes de los personajes
image_width, image_height = obtener_tamano_imagen(sakuraFlying)

# Crear personajes
wander = crear_personaje(Vector(100, 100), Vector(5, 0), 'wander', sakuraFlying)
seek = crear_personaje(Vector(200, 200), Vector(10, 0), 'seek', sakuraSeek)
arrive = crear_personaje(Vector(300, 300), Vector(0, 0), 'arrive', sakuraArrive)
flee = crear_personaje(Vector(400, 400), Vector(20, 0), 'flee', sakuraFlee)
wander2 = crear_personaje(Vector(400, 300), Vector(5, 0), 'wander', clowCard)

# Ejecutar el bucle principal del juego
personajes = (wander, seek, arrive, flee, wander2)
game_loop(pantalla, background, personajes, width, height, image_width, image_height, FPS)