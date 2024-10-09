import pygame
from unusedFiles.visuals import cargar_imagen

def cargar_imagenes():
    # Versiones de Sakura
    sakuraFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/SakuritaVolando.png')
    sakuraFlying2 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/SakuraFlying2.png')
    # Versiones de Kerberos
    keroFollow = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/keroFollow.png')
    keroFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/kerberosFlying.png')
    # Otros personajes
    yueFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/yueFlying.png')
    eriolFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/eriolFlying.png')
    spinelFlying = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/spinelFlying.png')

    # Imagenes para fondos
    frame = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/frame.png', 1280, 720)
    background = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background.jpg', 1280, 720) 
    background2 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background2.jpg', 1280, 720)
    background3 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background3.jpg', 1280, 720)
    background4 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background4.png', 1280, 720)
    background5 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background5.jpg', 1280, 720)
    background6 = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/background6.jpg', 1280, 720)
    
    # Cartas de Clow
    clowCard = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCard.png')
    clowCard = pygame.transform.scale(clowCard, (clowCard.get_width() // 2, clowCard.get_height() // 2))
    
    clowCardTheLight = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCardTheLight.png')
    clowCardTheLight = pygame.transform.scale(clowCardTheLight, (clowCardTheLight.get_width() // 2, clowCardTheLight.get_height() // 2))

    clowCardTheDark = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCardTheDark.png')
    clowCardTheDark = pygame.transform.scale(clowCardTheDark, (clowCardTheDark.get_width() // 2, clowCardTheDark.get_height() // 2))

    clowCardTheSleep = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCardTheSleep.png')
    clowCardTheSleep = pygame.transform.scale(clowCardTheSleep, (clowCardTheSleep.get_width() // 2, clowCardTheSleep.get_height() // 2))

    clowCardTheFlower = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCardTheFlower.png')
    clowCardTheFlower = pygame.transform.scale(clowCardTheFlower, (clowCardTheFlower.get_width() // 2, clowCardTheFlower.get_height() // 2))

    clowCardTheShadow = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clowCardTheShadow.png')
    clowCardTheShadow = pygame.transform.scale(clowCardTheShadow, (clowCardTheShadow.get_width() // 2, clowCardTheShadow.get_height() // 2))

    # Cartas de Sakura
    sakuraCard = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/sakuraCard.png')
    sakuraCard = pygame.transform.scale(sakuraCard, (sakuraCard.get_width() // 2, sakuraCard.get_height() // 2))

    # Imagenes varias
    clow = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/clow.png')
    symbol = cargar_imagen('D:/Desktop/IA/Proyectos/Proyecto1/InteligenciaArtificialUSB/assets/SakuraSymbol.png')
    symbol = pygame.transform.scale(symbol, (symbol.get_width() // 5, symbol.get_height() // 5))
        
    return {
        "sakuraFlying": sakuraFlying,
        "yueFlying": yueFlying,
        "eriolFlying": eriolFlying,
        "keroFlying": keroFlying,
        "background": background,
        "clowCard": clowCard,
        "clow": clow,
        "spinelFlying": spinelFlying,
        "clowCardTheLight": clowCardTheLight,
        "clowCardTheDark": clowCardTheDark,
        "clowCardTheSleep": clowCardTheSleep,
        "clowCardTheFlower": clowCardTheFlower,
        "clowCardTheShadow": clowCardTheShadow,
        "background2": background2,
        "background3": background3,
        "keroFollow": keroFollow,
        "sakuraCard": sakuraCard,
        "sakuraFlying2": sakuraFlying2,
        "background4": background4,
        "symbol": symbol,
        "frame": frame,
        "background5": background5,
        "background6": background6
    }