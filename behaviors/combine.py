from steering_output import SteeringOutput

class CombinedBehavior:
    """
    Una clase para combinar múltiples comportamientos de dirección.
    Atributos:
    ----------
    behaviors : list
        Una lista de objetos de comportamiento que tienen un método `getSteering` y un atributo `maxAcceleration`.
    Métodos:
    --------
    getSteering():
        Calcula la salida de dirección combinada de todos los comportamientos.
    """
    def __init__(self, behaviors):
        self.behaviors = behaviors

    def getSteering(self):
        steering = SteeringOutput()
        # Iterar sobre todos los comportamientos y sumar sus salidas de dirección.
        for behavior in self.behaviors:
            # Obtener la salida de dirección del comportamiento actual.
            behavior_steering = behavior.getSteering()
            # Si la salida de dirección no es None, sumarla a la salida de dirección total.
            if behavior_steering:
                # Sumar las aceleraciones lineales y angulares.
                steering.linear += behavior_steering.linear
                steering.angular += behavior_steering.angular
        # Normalizar el vector linear si su magnitud excede el maxAcceleration
        if steering.linear.length() > self.behaviors[0].maxAcceleration:
            steering.linear = steering.linear.normalize() * self.behaviors[0].maxAcceleration
        return steering
    
    