from steering_output import SteeringOutput

class VelocityMatch:
    def __init__(self, character, target, maxAcceleration, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()

        # Acceleration tries to get to the target velocity.
        result.linear = self.target.velocity - self.character.velocity
        result.linear /= self.timeToTarget

        # Check if the acceleration is too fast.
        if result.linear.length() > self.maxAcceleration:
            result.linear.normalize()
            result.linear *= self.maxAcceleration

        result.angular = 0
        return result