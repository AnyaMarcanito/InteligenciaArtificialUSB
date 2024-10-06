from visuals import inicializar_pygame, configurar_pantalla, obtener_tamano_imagen
from images import cargar_imagenes
from game_loop import game_loop
from characters import crear_personajes

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

# Obtener el tamaño de las imágenes de los personajes
image_width, image_height = obtener_tamano_imagen(sakuraFlying)

# Crear personajes y asignar imágenes
wander, seek, arrive, flee = crear_personajes()
wander.image = sakuraFlying
seek.image = sakuraSeek
arrive.image = sakuraArrive
flee.image = sakuraFlee

# Ejecutar el bucle principal del juego
personajes = (wander, seek, arrive, flee)
game_loop(pantalla, background, personajes, width, height, image_width, image_height, FPS)