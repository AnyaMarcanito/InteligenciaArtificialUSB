from steering_output import SteeringOutput

class Arrive:
    def __init__(self, character, target, maxAcceleration, maxSpeed, targetRadius, slowRadius, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.maxSpeed = maxSpeed
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()

        # Get the direction to the target.
        direction = self.target.position - self.character.position
        distance = direction.length()

        # Check if we are there, return no steering.
        if distance < self.targetRadius:
            return None

        # If we are outside the slowRadius, then move at max speed.
        if distance > self.slowRadius:
            targetSpeed = self.maxSpeed
        # Otherwise calculate a scaled speed.
        else:
            targetSpeed = self.maxSpeed * distance / self.slowRadius

        # The target velocity combines speed and direction.
        targetVelocity = direction
        targetVelocity.normalize()
        targetVelocity *= targetSpeed

        # Acceleration tries to get to the target velocity.
        result.linear = targetVelocity - self.character.velocity
        result.linear /= self.timeToTarget

        # Check if the acceleration is too fast.
        if result.linear.length() > self.maxAcceleration:
            result.linear.normalize()
            result.linear *= self.maxAcceleration

        result.angular = 0
        return result