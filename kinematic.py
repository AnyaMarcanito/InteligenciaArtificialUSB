import random
from vector import Vector
from steering_output import SteeringOutput
import math

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

    def update_with_steering(self, steering, maxSpeed, time):
        # Update the position and orientation.
        self.position += self.velocity * time
        self.orientation += self.rotation * time

        # Update the velocity and rotation.
        self.velocity += steering.linear * time
        self.rotation += steering.angular * time

        # Check for speeding and clip.
        if self.velocity.length() > maxSpeed:
            self.velocity.normalize()
            self.velocity *= maxSpeed

        # Actualizar la orientación del personaje
        self.orientation = self.newOrientation(self.orientation, self.velocity)

    @staticmethod
    def newOrientation(current, velocity):
        if velocity.length() > 0:
            return math.atan2(velocity.y, velocity.x)
        else:
            return current

    @staticmethod
    def orientationToVector(orientation):
        return Vector(math.cos(orientation), math.sin(orientation))

class KinematicSteeringOutput:
    def __init__(self, velocity=None, rotation=0):
        self.velocity = velocity if velocity is not None else Vector(0, 0)
        self.rotation = rotation

class KinematicSeek:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = KinematicSteeringOutput()
        result.velocity = self.target.position - self.character.position
        result.velocity.normalize()
        result.velocity *= self.maxSpeed
        self.character.orientation = Kinematic.newOrientation(self.character.orientation, result.velocity)
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
        result.velocity = self.target.position - self.character.position
        if result.velocity.length() < self.radius:
            return None
        result.velocity /= self.timeToTarget
        if result.velocity.length() > self.maxSpeed:
            result.velocity.normalize()
            result.velocity *= self.maxSpeed
        self.character.orientation = Kinematic.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        return result

class KinematicWander:
    def __init__(self, character, maxSpeed, maxRotation):
        self.character = character
        self.maxSpeed = maxSpeed
        self.maxRotation = maxRotation

    def getSteering(self):
        result = KinematicSteeringOutput()
        result.velocity = Kinematic.orientationToVector(self.character.orientation) * self.maxSpeed
        self.character.orientation += (random.random() - 0.5) * self.maxRotation
        result.velocity *= random.uniform(0.5, 1.5)
        return result

    def randomBinomial(self):
        return random.random() - random.random()

class KinematicFlee:
    def __init__(self, character, target, maxSpeed, fleeRadius):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.fleeRadius = fleeRadius

    def getSteering(self):
        result = KinematicSteeringOutput()
        direction = self.character.position - self.target.position
        distance = direction.length()
        if distance > self.fleeRadius:
            result.velocity = Vector(0, 0)  # Detener el movimiento si está fuera del fleeRadius
            self.character.velocity = Vector(0, 0)  # Asegurarse de que la velocidad del personaje sea cero
        else:
            direction.normalize()
            result.velocity = direction * self.maxSpeed
            self.character.orientation = Kinematic.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        return result

class KinematicSeekArrive:
    def __init__(self, character, target, maxSpeed, arriveRadius):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.arriveRadius = arriveRadius

    def getSteering(self):
        result = KinematicSteeringOutput()
        direction = self.target.position - self.character.position
        distance = direction.length()
        if distance < self.arriveRadius:
            result.velocity = direction * (self.maxSpeed * (distance / self.arriveRadius))
        else:
            direction.normalize()
            result.velocity = direction * self.maxSpeed
        self.character.orientation = Kinematic.newOrientation(self.character.orientation, result.velocity)
        result.rotation = 0
        return result