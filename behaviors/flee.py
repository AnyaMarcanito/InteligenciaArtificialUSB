from steering_output import SteeringOutput
from vector import Vector

class Flee:
    def __init__(self, character, target, maxAcceleration, fleeRadius):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.fleeRadius = fleeRadius

    def getSteering(self):
        result = SteeringOutput()
        # Get the direction away from the target.
        direction = self.character.position - self.target.position
        distance = direction.length()

        # If the target is outside the flee radius, stop the character
        if distance > self.fleeRadius:
            self.character.velocity = Vector(0, 0)
            result.linear = Vector(0, 0)
            result.angular = 0
            return result

        # Give full acceleration along this direction.
        result.linear = direction.normalize() * self.maxAcceleration
        result.angular = 0
        return result