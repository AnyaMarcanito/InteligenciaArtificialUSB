from vector import Vector
from steering_output import SteeringOutput
from behaviors.seek import Seek
from behaviors.collision_detector import CollisionDetector, Collision

class ObstacleAvoidance(Seek):
    def __init__(self, character, maxAcceleration, lookahead, avoidDistance, collisionDetector):
        super().__init__(character, None, maxAcceleration)
        self.lookahead = lookahead
        self.avoidDistance = avoidDistance
        self.collisionDetector = collisionDetector

    def getSteering(self):
        # 1. Calculate the target to delegate to seek
        # Calculate the collision ray vector.
        ray = self.character.velocity.normalize() * self.lookahead

        # Find the collision.
        collision = self.collisionDetector.getCollision(self.character.position, ray)

        # If have no collision, do nothing.
        if not collision:
            return None

        # 2. Otherwise create a target and delegate to seek.
        targetPosition = collision.position + collision.normal * self.avoidDistance

        # Create a temporary target for Seek to use
        temp_target = self.character
        temp_target.position = targetPosition

        # Delegate to seek
        self.target = temp_target
        return super().getSteering()