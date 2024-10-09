from steering_output import SteeringOutput

class CollisionAvoidance:
    """
    Una clase para representar el comportamiento de evitación de colisiones para un personaje.
    Atributos:
    ----------
    character : Kinematic
        El personaje que está evitando colisiones.
    targets : list
        Una lista de personajes objetivo que el personaje principal necesita evitar.
    maxAcceleration : float
        La aceleración máxima que el personaje puede alcanzar.
    radius : float
        El radio dentro del cual el personaje considera una colisión.
    Métodos:
    --------
    getSteering():
        Calcula y devuelve la salida de dirección para evitar colisiones.
    """
    def __init__(self, character, targets, maxAcceleration, radius):
        self.character = character
        self.targets = targets
        self.maxAcceleration= maxAcceleration
        self.radius = radius

    def getSteering(self):
        shortest_time = float('inf')
        first_target = None
        first_min_separation = 0
        first_distance = 0
        first_relative_position = None
        first_relative_velocity = None
        # Iterar sobre los objetivos y calcular el tiempo de colisión más corto.
        for target in self.targets:
            # Calcular la posición y velocidad relativa.
            relative_position = target.position - self.character.position
            relative_velocity = target.velocity - self.character.velocity
            relative_speed = relative_velocity.length()
            # Calcular el tiempo de colisión.
            time_to_collision = relative_position.dot(relative_velocity) / (relative_speed ** 2) if relative_speed != 0 else float('inf')
            distance = relative_position.length()
            # Calcular la separación mínima.
            min_separation = distance - relative_speed * time_to_collision
            # Si la separación mínima es mayor que el doble del radio, no hay colisión.
            if min_separation > 2 * self.radius:
                continue
            # Si el tiempo de colisión es negativo, no hay colisión.
            if time_to_collision > 0 and time_to_collision < shortest_time:
                shortest_time = time_to_collision
                # Guardar los datos del objetivo más cercano.
                first_target = target
                first_min_separation = min_separation
                first_distance = distance
                first_relative_position = relative_position
                first_relative_velocity = relative_velocity
        # Si no hay colisión, no es necesario hacer nada
        if first_target is None:
            return SteeringOutput()
        # Si hay colisión, calcular la dirección de evitación.
        if first_min_separation <= 0 or first_distance < 2 * self.radius:
            relative_position = first_target.position - self.character.position
        else:
            relative_position = first_relative_position + first_relative_velocity * shortest_time
        # Normalizar la dirección de evitación.
        relative_position = relative_position.normalize()
        # Devolver la dirección de evitación.
        steering: SteeringOutput = SteeringOutput(linear=relative_position * -self.maxAcceleration, angular=0)
        return steering