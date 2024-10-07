from vector import Vector

class Collision:
    def __init__(self, position, normal):
        self.position = position
        self.normal = normal

class CollisionDetector:
    def __init__(self, obstacles):
        self.obstacles = obstacles  # Lista de segmentos de línea que representan los obstáculos

    def getCollision(self, position, moveAmount):
        closestCollision = None
        closestDistance = float('inf')

        for obstacle in self.obstacles:
            collision = self._checkRaySegmentCollision(position, moveAmount, obstacle[0], obstacle[1])
            if collision:
                distance = (collision.position - position).length()
                if distance < closestDistance:
                    closestDistance = distance
                    closestCollision = collision

        return closestCollision

    def _checkRaySegmentCollision(self, rayOrigin, rayDirection, segmentStart, segmentEnd):
        # Implementar la lógica para detectar colisiones entre un rayo y un segmento de línea
        v1 = rayOrigin - segmentStart
        v2 = segmentEnd - segmentStart
        v3 = Vector(-rayDirection.y, rayDirection.x)

        dot = v2.dot(v3)
        if abs(dot) < 1e-6:
            return None  # No hay colisión, el rayo es paralelo al segmento

        t1 = v2.cross(v1) / dot
        t2 = v1.dot(v3) / dot

        if t1 >= 0 and 0 <= t2 <= 1:
            collisionPoint = rayOrigin + rayDirection * t1
            normal = Vector(segmentEnd.y - segmentStart.y, segmentStart.x - segmentEnd.x).normalize()
            return Collision(collisionPoint, normal)

        return None