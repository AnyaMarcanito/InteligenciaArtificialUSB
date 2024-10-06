import pygame
import math
import random

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector(self.x / scalar, self.y / scalar)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        length = self.length()
        if length > 0:
            self.x /= length
            self.y /= length

    def asVector(self):
        return Vector(math.cos(self.x), math.sin(self.y))

class Kinematic:
    def __init__(self, position, orientation, velocity, rotation):
        self.position = position
        self.orientation = orientation
        self.velocity = velocity
        self.rotation = rotation

    def update(self, steering, time):
        self.position += self.velocity * time
        self.orientation += self.rotation * time
        self.velocity += steering.velocity * time
        self.rotation += steering.rotation * time

    def newOrientation(self, current, velocity):
        if velocity.length() > 0:
            return math.atan2(-velocity.x, velocity.y)
        else:
            return current

    @staticmethod
    def orientationToVector(orientation):
        return Vector(math.cos(orientation), math.sin(orientation))

class SteeringOutput:
    def __init__(self, linear, angular):
        self.linear = linear
        self.angular = angular

class KinematicSteeringOutput:
    def __init__(self, velocity=None, rotation=0):
        self.velocity = velocity if velocity else Vector(0, 0)
        self.rotation = rotation

class KinematicSeek:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = KinematicSteeringOutput()

        # Get the direction to the target.
        result.velocity = self.target.position - self.character.position

        # The velocity is along this direction, at full speed.
        result.velocity.normalize()
        result.velocity *= self.maxSpeed

        # Face in the direction we want to move.
        self.character.orientation = self.character.newOrientation(
            self.character.orientation,
            result.velocity
        )

        result.rotation = 0
        return result

class KinematicArrive:
    def __init__(self, character, target, maxSpeed, radius, timeToTarget=0.25):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = KinematicSteeringOutput()

        # Get the direction to the target.
        result.velocity = self.target.position - self.character.position

        # Check if we’re within radius.
        if result.velocity.length() < self.radius:
            # Request no steering.
            return None

        # We need to move to our target, we’d like to get there in timeToTarget seconds.
        result.velocity /= self.timeToTarget

        # If this is too fast, clip it to the max speed.
        if result.velocity.length() > self.maxSpeed:
            result.velocity.normalize()
            result.velocity *= self.maxSpeed

        # Face in the direction we want to move.
        self.character.orientation = self.character.newOrientation(
            self.character.orientation,
            result.velocity
        )

        result.rotation = 0
        return result

class KinematicWander:
    def __init__(self, character, maxSpeed, maxRotation):
        self.character = character
        self.maxSpeed = maxSpeed
        self.maxRotation = maxRotation

    def getSteering(self):
        result = KinematicSteeringOutput()

        # Get velocity from the vector form of the orientation.
        result.velocity = Kinematic.orientationToVector(self.character.orientation) * self.maxSpeed

        # Change our orientation randomly but gradually.
        self.character.orientation += (random.random() - 0.5) * self.maxRotation

        # Vary the speed randomly within a range.
        result.velocity *= random.uniform(0.5, 1.5)

        return result

    def randomBinomial(self):
        return random.random() - random.random()

class KinematicFlee:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = KinematicSteeringOutput()

        # Get the direction away from the target.
        result.velocity = self.character.position - self.target.position

        # The velocity is along this direction, at full speed.
        result.velocity.normalize()
        result.velocity *= self.maxSpeed

        # Face in the direction we want to move.
        self.character.orientation = self.character.newOrientation(
            self.character.orientation,
            result.velocity
        )

        result.rotation = 0
        return result

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla y el reloj
width, height = 800, 600
pantalla = pygame.display.set_mode((width, height))
FPS = 60
TIMER = pygame.time.Clock()
pygame.display.set_caption('Cardcaptor Sakura')

# Cargar la imagen de fondo
background = pygame.image.load('D:/Desktop/IA/Proyectos/assets/background.jpg')  # Reemplaza con la ruta a tu imagen de fondo
background = pygame.transform.scale(background, (width, height))  # Ajustar la imagen al tamaño de la ventana

# Cargar las imágenes de los personajes
sakuraFlying = pygame.image.load('D:/Desktop/IA/Proyectos/assets/SakuritaVolando.png') 
sakuraSeek = pygame.image.load('D:/Desktop/IA/Proyectos/assets/yueFlying.png') 
sakuraArrive = pygame.image.load('D:/Desktop/IA/Proyectos/assets/eriolFlying.png') 
sakuraFlee = pygame.image.load('D:/Desktop/IA/Proyectos/assets/kerberosFlying.png') 

# Obtener el tamaño de las imágenes de los personajes
image_width = sakuraFlying.get_width()
image_height = sakuraFlying.get_height()

# Crear instancias de Kinematic para los personajes
position_wander = Vector(100, 100)
velocity_wander = Vector(5, 0)
kinematic_wander = Kinematic(position_wander, 0, velocity_wander, 0)

position_seek = Vector(200, 200)
velocity_seek = Vector(0, 0)
kinematic_seek = Kinematic(position_seek, 0, velocity_seek, 0)

position_arrive = Vector(300, 300)
velocity_arrive = Vector(0, 0)
kinematic_arrive = Kinematic(position_arrive, 0, velocity_arrive, 0)

position_flee = Vector(400, 400)
velocity_flee = Vector(0, 0)
kinematic_flee = Kinematic(position_flee, 0, velocity_flee, 0)

# Crear instancias de los algoritmos de movimiento
wander = KinematicWander(kinematic_wander, 10, 0.5)
seek_target = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)  # Objetivo para Seek
seek = KinematicSeek(kinematic_seek, seek_target, 15)
arrive_target = Kinematic(Vector(500, 500), 0, Vector(0, 0), 0)  # Objetivo para Arrive
arrive = KinematicArrive(kinematic_arrive, arrive_target, 5, 50)
flee_target = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)  # Objetivo para Flee
flee = KinematicFlee(kinematic_flee, flee_target, 20)

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Actualizar la posición del objetivo del seek para que sea el personaje que está huyendo (flee)
    seek.target.position = kinematic_flee.position
    # Obtener el steering y actualizar la posición de los personajes
    steering_wander = wander.getSteering()
    kinematic_wander.update(steering_wander, 1/FPS)

    steering_seek = seek.getSteering()
    kinematic_seek.update(steering_seek, 1/FPS)

    steering_arrive = arrive.getSteering()
    if steering_arrive:
        kinematic_arrive.update(steering_arrive, 1/FPS)

    steering_flee = flee.getSteering()
    kinematic_flee.update(steering_flee, 1/FPS)

    # Verificar colisiones con los bordes de la pantalla para el personaje wander
    if kinematic_wander.position.x < 0 or kinematic_wander.position.x > width - image_width:
        kinematic_wander.velocity.x = -kinematic_wander.velocity.x
        kinematic_wander.position.x = max(0, min(kinematic_wander.position.x, width - image_width))

    if kinematic_wander.position.y < 0 or kinematic_wander.position.y > height - image_height:
        kinematic_wander.velocity.y = -kinematic_wander.velocity.y
        kinematic_wander.position.y = max(0, min(kinematic_wander.position.y, height - image_height))

    # Verificar colisiones con los bordes de la pantalla para el personaje seek
    if kinematic_seek.position.x < 0 or kinematic_seek.position.x > width - image_width:
        kinematic_seek.velocity.x = -kinematic_seek.velocity.x
        kinematic_seek.position.x = max(0, min(kinematic_seek.position.x, width - image_width))

    if kinematic_seek.position.y < 0 or kinematic_seek.position.y > height - image_height:
        kinematic_seek.velocity.y = -kinematic_seek.velocity.y
        kinematic_seek.position.y = max(0, min(kinematic_seek.position.y, height - image_height))

    # Verificar colisiones con los bordes de la pantalla para el personaje flee
    if kinematic_flee.position.x < 0 or kinematic_flee.position.x > width - image_width:
        kinematic_flee.velocity.x = -kinematic_flee.velocity.x
        kinematic_flee.position.x = max(0, min(kinematic_flee.position.x, width - image_width))

    if kinematic_flee.position.y < 0 or kinematic_flee.position.y > height - image_height:
        kinematic_flee.velocity.y = -kinematic_flee.velocity.y
        kinematic_flee.position.y = max(0, min(kinematic_flee.position.y, height - image_height))

    # Dibujar la imagen de fondo
    pantalla.blit(background, (0, 0))

    # Dibujar las imágenes de los personajes en sus posiciones actuales
    # pantalla.blit(sakuraFlying, (int(kinematic_wander.position.x), int(kinematic_wander.position.y)))
    pantalla.blit(sakuraSeek, (int(kinematic_seek.position.x), int(kinematic_seek.position.y)))
    # pantalla.blit(sakuraArrive, (int(kinematic_arrive.position.x), int(kinematic_arrive.position.y)))
    pantalla.blit(sakuraFlee, (int(kinematic_flee.position.x), int(kinematic_flee.position.y)))

    pygame.display.flip()
    TIMER.tick(FPS)

pygame.quit()