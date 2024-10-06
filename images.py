import pygame
from visuals import cargar_imagen

def cargar_imagenes():
    sakuraFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/SakuritaVolando.png')
    sakuraSeek = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/yueFlying.png')
    sakuraArrive = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/eriolFlying.png')
    sakuraFlee = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/kerberosFlying.png')
    background = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background.jpg', 800, 600) 
    clowCard = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCard.png')
    clowCard = pygame.transform.scale(clowCard, (clowCard.get_width() // 2, clowCard.get_height() // 2))
    
    return {
        "sakuraFlying": sakuraFlying,
        "sakuraSeek": sakuraSeek,
        "sakuraArrive": sakuraArrive,
        "sakuraFlee": sakuraFlee,
        "background": background,
        "clowCard": clowCard
    }