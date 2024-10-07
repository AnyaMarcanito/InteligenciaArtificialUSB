from vector import Vector
from steering_output import SteeringOutput
from kinematics.kinematic import Kinematic
import math

class CollisionAvoidance:
    def __init__(self, character, targets, maxAcceleration, radius):
        self.character = character
        self.targets = targets
        self.maxAcceleration = maxAcceleration
        self.radius = radius

    def getSteering(self):
        # 1. Find the target that’s closest to collision
        shortestTime = float('inf')

        # Store the target that collides then, and other data that we will need and can avoid recalculating.
        firstTarget = None
        firstMinSeparation = None
        firstDistance = None
        firstRelativePos = None
        firstRelativeVel = None

        # Loop through each target.
        for target in self.targets:
            # Calculate the time to collision.
            relativePos = target.position - self.character.position
            relativeVel = target.velocity - self.character.velocity
            relativeSpeed = relativeVel.length()
            timeToCollision = relativePos.dot(relativeVel) / (relativeSpeed * relativeSpeed)

            # Check if it is going to be a collision at all.
            distance = relativePos.length()
            minSeparation = distance - relativeSpeed * timeToCollision
            if minSeparation > 2 * self.radius:
                continue

            # Check if it is the shortest.
            if 0 < timeToCollision < shortestTime:
                # Store the time, target and other data.
                shortestTime = timeToCollision
                firstTarget = target
                firstMinSeparation = minSeparation
                firstDistance = distance
                firstRelativePos = relativePos
                firstRelativeVel = relativeVel

        # 2. Calculate the steering
        # If we have no target, then exit.
        if not firstTarget:
            return None

        # If we’re going to hit exactly, or if we’re already colliding, then do the steering based on current position.
        if firstMinSeparation <= 0 or firstDistance < 2 * self.radius:
            relativePos = firstTarget.position - self.character.position
        # Otherwise calculate the future relative position.
        else:
            relativePos = firstRelativePos + firstRelativeVel * shortestTime

        # Avoid the target.
        relativePos = relativePos.normalize()

        result = SteeringOutput()
        result.linear = relativePos * self.maxAcceleration
        result.angular = 0
        return result