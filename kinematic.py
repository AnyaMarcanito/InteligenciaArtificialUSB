import random
import math
from vector import Vector

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

    def newOrientation(self, current, velocity):
        if velocity.length() > 0:
            return math.atan2(-velocity.x, velocity.y)
        else:
            return current

    @staticmethod
    def orientationToVector(orientation):
        return Vector(math.cos(orientation), math.sin(orientation))

class KinematicSteeringOutput:
    def __init__(self, velocity=None, rotation=0):
        self.velocity = velocity if velocity is not None else Vector(0, 0)
        self.rotation = rotation

class SteeringOutput:
    def __init__(self, linear=None, angular=0):
        self.linear = linear if linear is not None else Vector(0, 0)
        self.angular = angular

class Seek:
    def __init__(self, character, target, maxAcceleration):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration

    def getSteering(self):
        result = SteeringOutput()
        # Get the direction to the target.
        result.linear = self.target.position - self.character.position

        # Give full acceleration along this direction.
        result.linear.normalize()
        result.linear *= self.maxAcceleration

        result.angular = 0
        return result

class Arrive:
    def __init__(self, character, target, maxAcceleration, maxSpeed, targetRadius, slowRadius, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.maxSpeed = maxSpeed
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()

        # Get the direction to the target.
        direction = self.target.position - self.character.position
        distance = direction.length()

        # Check if we are there, return no steering.
        if distance < self.targetRadius:
            return None

        # If we are outside the slowRadius, then move at max speed.
        if distance > self.slowRadius:
            targetSpeed = self.maxSpeed
        # Otherwise calculate a scaled speed.
        else:
            targetSpeed = self.maxSpeed * distance / self.slowRadius

        # The target velocity combines speed and direction.
        targetVelocity = direction
        targetVelocity.normalize()
        targetVelocity *= targetSpeed

        # Acceleration tries to get to the target velocity.
        result.linear = targetVelocity - self.character.velocity
        result.linear /= self.timeToTarget

        # Check if the acceleration is too fast.
        if result.linear.length() > self.maxAcceleration:
            result.linear.normalize()
            result.linear *= self.maxAcceleration

        result.angular = 0
        return result

class Flee:
    def __init__(self, character, target, maxAcceleration):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration

    def getSteering(self):
        result = SteeringOutput()
        # Get the direction away from the target.
        result.linear = self.character.position - self.target.position

        # Give full acceleration along this direction.
        result.linear.normalize()
        result.linear *= self.maxAcceleration

        result.angular = 0
        return result
    
class KinematicSeek:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = SteeringOutput()
        result.linear = self.target.position - self.character.position
        result.linear.normalize()
        result.linear *= self.maxSpeed
        result.angular = 0
        return result

class KinematicArrive:
    def __init__(self, character, target, maxSpeed, radius):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed
        self.radius = radius

    def getSteering(self):
        result = SteeringOutput()
        direction = self.target.position - self.character.position
        distance = direction.length()

        if distance < self.radius:
            return None

        result.linear = direction
        result.linear.normalize()
        result.linear *= self.maxSpeed * (distance / self.radius)
        result.angular = 0
        return result

class KinematicWander:
    def __init__(self, character, maxSpeed, maxRotation):
        self.character = character
        self.maxSpeed = maxSpeed
        self.maxRotation = maxRotation

    def getSteering(self):
        result = SteeringOutput()
        result.linear = self.character.orientationToVector(self.character.orientation) * self.maxSpeed
        result.angular = (random.random() - 0.5) * self.maxRotation
        return result

class KinematicFlee:
    def __init__(self, character, target, maxSpeed):
        self.character = character
        self.target = target
        self.maxSpeed = maxSpeed

    def getSteering(self):
        result = SteeringOutput()
        result.linear = self.character.position - self.target.position
        result.linear.normalize()
        result.linear *= self.maxSpeed
        result.angular = 0
        return result