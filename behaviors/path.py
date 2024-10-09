from vector import Vector

class Path:
    """
    Una clase para representar un camino compuesto por múltiples puntos.
    Atributos
    ---------
    points : lista de Vector
        Una lista de puntos que definen el camino.
    Métodos
    -------
    getParam(position: Vector, lastParam: float) -> float
        Encuentra el segmento más cercano en el camino a la posición dada y devuelve el parámetro correspondiente.
    _distanceToSegment(point: Vector, segment_start: Vector, segment_end: Vector) -> float
        Calcula la distancia desde un punto a un segmento de línea.
    getPosition(param: float) -> Vector
        Devuelve la posición en el camino para el parámetro dado.
    """
    def __init__(self, points):
        self.points = points

    def getParam(self, position: Vector, lastParam: float) -> float:
        # Encuentra el segmento más cercano en la ruta al personaje
        closestParam = lastParam
        closestDistance = float('inf')
        num_points = len(self.points)
        # Buscar en los segmentos cercanos al último parámetro
        for i in range(num_points):
            # Calcular la distancia al segmento
            segment_start = self.points[i]
            # El siguiente punto en el camino
            segment_end = self.points[(i + 1) % num_points]
            # Calcular la distancia al segmento y el parámetro más cercano
            distance = self._distanceToSegment(position, segment_start, segment_end)
            # Si la distancia es la más cercana, guardar el parámetro
            if distance < closestDistance:
                # Asignar la distancia más cercana y el parámetro correspondiente
                closestDistance = distance
                closestParam = i + (distance / (segment_end - segment_start).length())
        return closestParam

    def _distanceToSegment(self, point: Vector, segment_start: Vector, segment_end: Vector) -> float:
        # Calcula la distancia desde un punto a un segmento de línea
        segment_vector = segment_end - segment_start
        segment_length = segment_vector.length()
        # Verificar si la longitud del segmento es cero
        if segment_length == 0:
            # Devolver la distancia al punto de inicio del segmento
            return (point - segment_start).length()
        # Si la longitud del segmento no es cero, calcular la distancia al segmento
        point_vector = point - segment_start
        # Calcular la proyección del punto en el segmento
        segment_unit_vector = segment_vector / segment_length
        # Calcular el punto más cercano en el segmento
        projection_length = point_vector.dot(segment_unit_vector)
        # Verificar si el punto proyectado está fuera del segmento
        if projection_length < 0:
            # Si la longitud de la proyección es negativa, el punto proyectado está antes del inicio del segmento.
            # Por lo tanto, el punto más cercano en el segmento es el inicio del segmento.
            closest_point = segment_start
        elif projection_length > segment_length:
            # Si la longitud de la proyección es mayor que la longitud del segmento, el punto proyectado está después del final del segmento.
            # Por lo tanto, el punto más cercano en el segmento es el final del segmento.
            closest_point = segment_end
        else:
            # Si la longitud de la proyección está dentro del segmento, calcular el punto más cercano en el segmento.
            closest_point = segment_start + segment_unit_vector * projection_length
        # Devolver la distancia entre el punto original y el punto más cercano en el segmento.
        return (point - closest_point).length()

    def getPosition(self, param: float) -> Vector:
        # Devuelve la posición en la ruta para el parámetro dado
        num_points = len(self.points)
        # Calcular el punto entero y el siguiente punto en el camino
        int_param = int(param) % num_points
        next_param = (int_param + 1) % num_points
        # Calcular el segmento y el parámetro interpolado
        segment_start = self.points[int_param]
        segment_end = self.points[next_param]
        t = param - int_param
        # Devolver el punto interpolado en el segmento dado
        return segment_start + (segment_end - segment_start) * t