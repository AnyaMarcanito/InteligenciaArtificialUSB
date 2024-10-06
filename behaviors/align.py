from vector import Vector
from steering_output import SteeringOutput
from utils.utils import mapToRange

class Align:
    def __init__(self, character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAngularAcceleration = maxAngularAcceleration
        self.maxRotation = maxRotation
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()

        # Get the naive direction to the target.
        rotation = self.target.orientation - self.character.orientation
        # Map the result to the (-pi, pi) interval.
        rotation = mapToRange(rotation)
        rotationSize = abs(rotation)

        # Check if we are there, return no steering.
        if rotationSize < self.targetRadius:
            return result

        # If we are outside the slowRadius, then use maximum rotation.
        if rotationSize > self.slowRadius:
            targetRotation = self.maxRotation
        # Otherwise calculate a scaled rotation.
        else:
            targetRotation = self.maxRotation * rotationSize / self.slowRadius

        # The final target rotation combines speed (already in the variable) and direction.
        targetRotation *= rotation / rotationSize

        # Acceleration tries to get to the target rotation.
        result.angular = targetRotation - self.character.rotation
        result.angular /= self.timeToTarget

        # Check if the acceleration is too great.
        angularAcceleration = abs(result.angular)
        if angularAcceleration > self.maxAngularAcceleration:
            result.angular /= angularAcceleration
            result.angular *= self.maxAngularAcceleration

        result.linear = Vector(0, 0)
        return result