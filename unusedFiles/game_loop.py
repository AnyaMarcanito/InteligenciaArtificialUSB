import pygame
from visuals import verificar_colisiones

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True

def update_characters(personajes, FPS):
    wander, seek, arrive, flee, wander2, clow, align, player = personajes

    steering_wander = wander.getSteering()
    wander.kinematic.update(steering_wander, 1/FPS)

    steering_seek = seek.getSteering()
    seek.kinematic.update_with_steering(steering_seek, seek.maxAcceleration, 1/FPS)

    steering_arrive = arrive.getSteering()
    if steering_arrive:
        arrive.kinematic.update_with_steering(steering_arrive, arrive.maxAcceleration, 1/FPS)

    steering_flee = flee.getSteering()
    flee.kinematic.update_with_steering(steering_flee, flee.maxAcceleration, 1/FPS)

    steering_wander2 = wander2.getSteering()
    wander2.kinematic.update(steering_wander2, 1/FPS)

    steering_align = align.getSteering()  # Obtener el steering para align
    align.kinematic.update_with_steering(steering_align, align.maxAngularAcceleration, 1/FPS)  # Actualizar align

    # Actualizar la posición del jugador con la entrada del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player.kinematic.position.x = mouse_x
    player.kinematic.position.y = mouse_y

def check_collisions(personajes, width, height, image_width, image_height):
    for personaje in personajes:
        if personaje is None or not hasattr(personaje, 'kinematic'):
            continue

        kinematic = personaje.kinematic
        if kinematic.position.x < 0 or kinematic.position.x + image_width > width:
            kinematic.velocity.x = -kinematic.velocity.x
            kinematic.position.x = max(0, min(kinematic.position.x, width - image_width))

        if kinematic.position.y < 0 or kinematic.position.y + image_height > height:
            kinematic.velocity.y = -kinematic.velocity.y
            kinematic.position.y = max(0, min(kinematic.position.y, height - image_height))

def draw_screen(pantalla, background, personajes, width, height, image_width, image_height, margin):
    wander, seek, arrive, flee, wander2, clow, align, player = personajes

    pantalla.blit(background, (0, 0))

    pantalla.blit(wander.image, (int(wander.kinematic.position.x), int(wander.kinematic.position.y)))
    pantalla.blit(seek.image, (int(seek.kinematic.position.x), int(seek.kinematic.position.y)))
    pantalla.blit(arrive.image, (int(arrive.kinematic.position.x), int(arrive.kinematic.position.y)))
    pantalla.blit(flee.image, (int(flee.kinematic.position.x), int(flee.kinematic.position.y)))
    pantalla.blit(wander2.image, (int(wander2.kinematic.position.x), int(wander2.kinematic.position.y)))
    pantalla.blit(align.image, (int(align.kinematic.position.x), int(align.kinematic.position.y)))  # Dibujar align

    # Dibujar clow en la esquina inferior izquierda
    clow_x = margin
    clow_y = height - image_height - margin
    pantalla.blit(clow, (clow_x, clow_y))

    pantalla.blit(player.image, (int(player.kinematic.position.x), int(player.kinematic.position.y)))

    pygame.display.flip()

def game_loop(pantalla, background, personajes, width, height, image_width, image_height, FPS):
    TIMER = pygame.time.Clock()
    running = True
    margin = 20

    while running:
        running = handle_events()
        update_characters(personajes, FPS)
        check_collisions(personajes, width, height, image_width, image_height)
        draw_screen(pantalla, background, personajes, width, height, image_width, image_height, margin)
        TIMER.tick(FPS)

    pygame.quit()