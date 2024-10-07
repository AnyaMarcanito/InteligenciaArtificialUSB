from behaviors.seek import Seek
from steering_output import SteeringOutput
from behaviors.path import Path
from kinematics.kinematic import Kinematic

class FollowPath(Seek):
    def __init__(self, character, path, pathOffset, maxAcceleration):
        super().__init__(character, None, maxAcceleration)
        self.path = path
        self.pathOffset = pathOffset
        self.currentParam = 0

    def getSteering(self):
        # 1. Calculate the target to delegate to seek
        # Find the current position on the path
        self.currentParam = self.path.getParam(self.character.position, self.currentParam)
        # Offset it
        targetParam = self.currentParam + self.pathOffset

        # Get the target position
        targetPosition = self.path.getPosition(targetParam)

        # Create a temporary target for Seek to use
        temp_target = Kinematic(targetPosition, 0, Vector(0, 0), 0)
        self.target = temp_target

        # 2. Delegate to seek
        return super().getSteering()