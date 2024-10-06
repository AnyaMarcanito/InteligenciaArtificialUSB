import math

def mapToRange(rotation):
    rotation = rotation % (2 * math.pi)
    if rotation > math.pi:
        rotation -= 2 * math.pi
    return rotation