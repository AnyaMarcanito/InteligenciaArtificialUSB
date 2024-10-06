from visuals import cargar_imagen

def cargar_imagenes():
    sakuraFlying = cargar_imagen('D:/Desktop/IA/Proyectos/assets/SakuritaVolando.png')
    sakuraSeek = cargar_imagen('D:/Desktop/IA/Proyectos/assets/yueFlying.png')
    sakuraArrive = cargar_imagen('D:/Desktop/IA/Proyectos/assets/eriolFlying.png')
    sakuraFlee = cargar_imagen('D:/Desktop/IA/Proyectos/assets/kerberosFlying.png')
    background = cargar_imagen('D:/Desktop/IA/Proyectos/assets/background.jpg', 800, 600)  # Ajustar la imagen al tamaño de la ventana

    return {
        "sakuraFlying": sakuraFlying,
        "sakuraSeek": sakuraSeek,
        "sakuraArrive": sakuraArrive,
        "sakuraFlee": sakuraFlee,
        "background": background
    }