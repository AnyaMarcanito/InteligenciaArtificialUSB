from behaviors.align import Align
from steering_output import SteeringOutput
from vector import Vector
import math

class LookWhereYoureGoing(Align):
    def __init__(self, character, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget=0.1):
        # No need for an overridden target member, we have no explicit target to set.
        super().__init__(character, None, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def getSteering(self):
        # 1. Calculate the target to delegate to align
        # Check for a zero direction, and make no change if so.
        velocity = self.character.velocity
        if velocity.length() == 0:
            return None

        # Otherwise set the target based on the velocity.
        explicitTarget = self.character
        explicitTarget.orientation = math.atan2(velocity.y, velocity.x)

        # 2. Delegate to align.
        self.target = explicitTarget
        return super().getSteering()