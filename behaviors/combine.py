from vector import Vector
from steering_output import SteeringOutput

class CombinedBehavior:
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def getSteering(self):
        combined_steering = SteeringOutput(Vector(0, 0), 0)
        for behavior in self.behaviors:
            steering = behavior.getSteering()
            if steering:
                combined_steering.linear += steering.linear
                combined_steering.angular += steering.angular
        return combined_steering