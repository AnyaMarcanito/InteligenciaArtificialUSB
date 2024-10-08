from behaviors.align import Align
from steering_output import SteeringOutput
import math
class Face(Align):
    def __init__(self, character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget=0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def getSteering(self):
        # 1. Calculate the target to delegate to align
        direction = self.target.position - self.character.position

        # Check for a zero direction, and make no change if so.
        if direction.length() == 0:
            return SteeringOutput()

        # Calculate the orientation to face the target.
        explicitTarget = self.target
        explicitTarget.orientation = math.atan2(direction.y, direction.x)

        # 2. Delegate to align.
        self.target = explicitTarget
        return super().getSteering()