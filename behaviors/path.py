from vector import Vector

class Path:
    def __init__(self, points):
        self.points = points

    def getParam(self, position, lastParam):
        # Encuentra el segmento más cercano en la ruta al personaje
        closestParam = lastParam
        closestDistance = float('inf')
        num_points = len(self.points)

        # Buscar en los segmentos cercanos al último parámetro
        for i in range(lastParam - 1, lastParam + 2):
            segment_start = self.points[i % num_points]
            segment_end = self.points[(i + 1) % num_points]
            distance = self._distanceToSegment(position, segment_start, segment_end)
            if distance < closestDistance:
                closestDistance = distance
                closestParam = i % num_points

        return closestParam

    def _distanceToSegment(self, point, segment_start, segment_end):
        # Calcula la distancia desde un punto a un segmento de línea
        segment_vector = segment_end - segment_start
        point_vector = point - segment_start
        segment_length = segment_vector.length()
        segment_unit_vector = segment_vector / segment_length
        projection_length = point_vector.dot(segment_unit_vector)
        if projection_length < 0:
            closest_point = segment_start
        elif projection_length > segment_length:
            closest_point = segment_end
        else:
            closest_point = segment_start + segment_unit_vector * projection_length
        return (point - closest_point).length()

    def getPosition(self, param):
        # Devuelve la posición en la ruta para el parámetro dado
        num_points = len(self.points)
        if param < 0:
            param = 0
        elif param >= num_points:
            param = num_points - 1
        return self.points[param]