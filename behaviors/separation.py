from typing import List
from kinematic import Kinematic
from steering_output import SteeringOutput
from vector import Vector

class Separation:
    def __init__(self, character: Kinematic, targets: List[Kinematic], player: Kinematic, maxAcceleration: float, threshold: float, decayCoefficient: float, timeToTarget: float = 0.1):
        self.character: Kinematic = character
        self.targets: List[Kinematic] = targets
        self.player: Kinematic = player
        self.maxAcceleration: float = maxAcceleration
        self.threshold: float = threshold
        self.decayCoefficient: float = decayCoefficient
        self.timeToTarget: float = timeToTarget

    def getSteering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()
        # Use Velocity Match behavior to match the player velocity
        steering.linear = self.player.velocity
        steering.linear /= self.timeToTarget

        if steering.linear.length() > self.maxAcceleration:
            steering.linear = steering.linear.normalize() * self.maxAcceleration

        steering.angular = 0

        # Calculate the separation for each target
        for target in self.targets:
            # Check if the target is close
            direction: Vector = self.character.position - target.position 
            distance: float = direction.length()

            # If the target is close, calculate the separation
            if distance < self.threshold:
                # Calculate the strength of the separation with the decay coefficient
                strength: float = min(self.decayCoefficient / (distance ** 2) if distance != 0 else 0, self.maxAcceleration)
                # Calculate the direction of the separation
                direction = direction.normalize()
                # Add the separation to the steering
                steering.linear += direction * strength

        return steering