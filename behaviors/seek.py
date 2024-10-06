from steering_output import SteeringOutput
from vector import Vector

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