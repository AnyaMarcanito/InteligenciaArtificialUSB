import random
import math
from vector import Vector
from behaviors.face import Face
from steering_output import SteeringOutput
from kinematic import Kinematic
from behaviors.seek import Seek

class Wander(Face):
    def __init__(self, character, wanderOffset, wanderRadius, wanderRate, maxAcceleration):
        super().__init__(character, None, maxAngularAcceleration=0, maxRotation=0, targetRadius=0, slowRadius=0)
        self.wanderOffset = wanderOffset
        self.wanderRadius = wanderRadius
        self.wanderRate = wanderRate
        self.wanderOrientation = 0
        self.maxAcceleration = maxAcceleration
        self.target = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0)  # Inicializar target como Kinematic
        self.seek = Seek(character, self.target, maxAcceleration)

    def randomBinomial(self):
        return random.random() - random.random()

    def getSteering(self):
        # 1. Calculate the target to delegate to face
        # Update the wander orientation.
        self.wanderOrientation += self.randomBinomial() * self.wanderRate

        # Calculate the combined target orientation.
        targetOrientation = self.wanderOrientation + self.character.orientation

        # Calculate the center of the wander circle.
        wanderCircleCenter = self.character.position + Vector(math.cos(self.character.orientation), math.sin(self.character.orientation)) * self.wanderOffset

        # Calculate the target location.
        target = wanderCircleCenter + Vector(math.cos(targetOrientation), math.sin(targetOrientation)) * self.wanderRadius

        # Update the target's position.
        self.target.position = target

        # 2. Delegate to face.
        result = super().getSteering()

        # 3. Now set the linear acceleration to be at full acceleration in the direction of the orientation.
        seekSteering = self.seek.getSteering()
        result.linear = seekSteering.linear

        return result