from vector import Vector

class SteeringOutput:
    def __init__(self, linear=None, angular=0):
        self.linear = linear if linear is not None else Vector(0, 0)
        self.angular = angular