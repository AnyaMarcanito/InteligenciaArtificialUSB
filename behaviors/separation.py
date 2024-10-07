from vector import Vector
from steering_output import SteeringOutput
from kinematics.kinematic import Kinematic

class Separation:
    def __init__(self, character, targets, maxAcceleration, threshold, decayCoefficient):
        self.character = character
        self.targets = targets
        self.maxAcceleration = maxAcceleration
        self.threshold = threshold
        self.decayCoefficient = decayCoefficient

    def getSteering(self):
        result = SteeringOutput()

        # Loop through each target.
        for target in self.targets:
            # Check if the target is close.
            direction = target.position - self.character.position
            distance = direction.length()

            if distance < self.threshold:
                # Calculate the strength of repulsion (using the inverse square law).
                strength = min(self.decayCoefficient / (distance * distance), self.maxAcceleration)

                # Add the acceleration.
                direction = direction.normalize()
                result.linear += strength * direction

        # Ensure the result does not exceed maxAcceleration.
        if result.linear.length() > self.maxAcceleration:
            result.linear = result.linear.normalize() * self.maxAcceleration

        result.angular = 0
        return result