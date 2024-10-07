from vector import Vector
from steering_output import SteeringOutput

class CombinedBehavior:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def getSteering(self):
        steering = SteeringOutput()
        for behavior in self.behaviors:
            behavior_steering = behavior.getSteering()
            if behavior_steering:
                steering.linear += behavior_steering.linear
                steering.angular += behavior_steering.angular
        return steering