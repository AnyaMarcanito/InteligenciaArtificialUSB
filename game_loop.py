import pygame
from visuals import verificar_colisiones

def game_loop(pantalla, background, personajes, width, height, image_width, image_height, FPS):
    wander, seek, arrive, flee, wander2 = personajes
    TIMER = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener el steering y actualizar la posición de los personajes
        steering_wander = wander.getSteering()
        wander.character.update_with_steering(steering_wander, wander.maxSpeed, 1/FPS)

        steering_seek = seek.getSteering()
        seek.character.update_with_steering(steering_seek, seek.maxAcceleration, 1/FPS)

        steering_arrive = arrive.getSteering()
        if steering_arrive:
            arrive.character.update_with_steering(steering_arrive, arrive.maxAcceleration, 1/FPS)

        steering_flee = flee.getSteering()
        flee.character.update_with_steering(steering_flee, flee.maxAcceleration, 1/FPS)

        steering_wander2 = wander2.getSteering()
        wander2.character.update_with_steering(steering_wander2, wander2.maxSpeed, 1/FPS)


        # Verificar colisiones con los bordes de la pantalla para los personajes
        verificar_colisiones(wander.character, width, height, image_width, image_height)
        verificar_colisiones(seek.character, width, height, image_width, image_height)
        verificar_colisiones(arrive.character, width, height, image_width, image_height)
        verificar_colisiones(flee.character, width, height, image_width, image_height)
        verificar_colisiones(wander2.character, width, height, image_width, image_height)

        # Dibujar la imagen de fondo
        pantalla.blit(background, (0, 0))

        # Dibujar las imágenes de los personajes en sus posiciones actuales
        pantalla.blit(wander.image, (int(wander.character.position.x), int(wander.character.position.y)))
        pantalla.blit(seek.image, (int(seek.character.position.x), int(seek.character.position.y)))
        # pantalla.blit(arrive.image, (int(arrive.character.position.x), int(arrive.character.position.y)))
        pantalla.blit(flee.image, (int(flee.character.position.x), int(flee.character.position.y)))
        pantalla.blit(wander2.image, (int(wander2.character.position.x), int(wander2.character.position.y)))

        pygame.display.flip()
        TIMER.tick(FPS)

    pygame.quit()