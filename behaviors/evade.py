from behaviors.flee import Flee
from steering_output import SteeringOutput
from kinematic import Kinematic

class Evade(Flee):
    def __init__(self, character, target, maxAcceleration, maxPrediction, fleeRadius):
        super().__init__(character, target, maxAcceleration, fleeRadius)
        self.maxPrediction = maxPrediction

    def getSteering(self):
        # 1. Calculate the target to delegate to flee
        direction = self.character.position - self.target.position
        distance = direction.length()

        # Work out our current speed.
        speed = self.character.velocity.length()

        # Check if speed gives a reasonable prediction time.
        if speed <= distance / self.maxPrediction:
            prediction = self.maxPrediction
        else:
            prediction = distance / speed

        # Put the target together.
        explicitTarget = self.target.position + self.target.velocity * prediction

        # Create a temporary target for Flee to use.
        temp_target = Kinematic(explicitTarget, 0, self.target.velocity, 0)
        self.target = temp_target

        # 2. Delegate to flee.
        return super().getSteering()