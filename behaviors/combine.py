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

        # Normalizar el vector linear si su magnitud excede el maxAcceleration
        if steering.linear.length() > self.behaviors[0].maxAcceleration:
            steering.linear = steering.linear.normalize() * self.behaviors[0].maxAcceleration

        return steering
    
    