from vector import Vector

class Path:
    def __init__(self, points):
        self.points = points

    def getParam(self, position: Vector, lastParam: float) -> float:
        # Encuentra el segmento más cercano en la ruta al personaje
        closestParam = lastParam
        closestDistance = float('inf')
        num_points = len(self.points)

        # Buscar en los segmentos cercanos al último parámetro
        for i in range(num_points):
            segment_start = self.points[i]
            segment_end = self.points[(i + 1) % num_points]
            distance = self._distanceToSegment(position, segment_start, segment_end)
            if distance < closestDistance:
                closestDistance = distance
                closestParam = i + (distance / (segment_end - segment_start).length())

        return closestParam

    def _distanceToSegment(self, point: Vector, segment_start: Vector, segment_end: Vector) -> float:
        # Calcula la distancia desde un punto a un segmento de línea
        segment_vector = segment_end - segment_start
        segment_length = segment_vector.length()
        
        # Verificar si la longitud del segmento es cero
        if segment_length == 0:
            return (point - segment_start).length()

        point_vector = point - segment_start
        segment_unit_vector = segment_vector / segment_length
        projection_length = point_vector.dot(segment_unit_vector)
        if projection_length < 0:
            closest_point = segment_start
        elif projection_length > segment_length:
            closest_point = segment_end
        else:
            closest_point = segment_start + segment_unit_vector * projection_length
        return (point - closest_point).length()

    def getPosition(self, param: float) -> Vector:
        # Devuelve la posición en la ruta para el parámetro dado
        num_points = len(self.points)
        int_param = int(param) % num_points  # Asegurarse de que el índice esté dentro del rango
        next_param = (int_param + 1) % num_points
        segment_start = self.points[int_param]
        segment_end = self.points[next_param]
        t = param - int_param
        return segment_start + (segment_end - segment_start) * t