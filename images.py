import pygame
from visuals import cargar_imagen

def cargar_imagenes():
    sakuraFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/SakuritaVolando.png')
    yueFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/yueFlying.png')
    eriolFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/eriolFlying.png')
    keroFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/kerberosFlying.png')
    background = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background.jpg', 960, 540) 
    clowCard = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCard.png')
    clowCard = pygame.transform.scale(clowCard, (clowCard.get_width() // 2, clowCard.get_height() // 2))
    clow = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clow.png')
    return {
        "sakuraFlying": sakuraFlying,
        "yueFlying": yueFlying,
        "eriolFlying": eriolFlying,
        "keroFlying": keroFlying,
        "background": background,
        "clowCard": clowCard,
        "clow": clow
    }