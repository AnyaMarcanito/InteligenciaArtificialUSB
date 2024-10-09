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
        steering.linear = Vector(0, 0)

        for target in self.targets:
            direction: Vector = self.character.position - target.position
            distance: float = direction.length()  # Usamos el método length() definido

            # Evitamos la división por cero
            if distance > 0.0001:  # Un valor muy pequeño para evitar divisiones por cero
                strength: float = min(self.decayCoefficient / (distance ** 2), self.maxAcceleration)
                direction = direction.normalize()
                steering.linear += direction.__mul__(strength)

        # Limitamos la aceleración
        if steering.linear.length() > self.maxAcceleration:
            steering.linear = steering.linear.normalize() * self.maxAcceleration

        steering.angular = 0
        return steering