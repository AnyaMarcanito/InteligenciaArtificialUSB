from steering_output import SteeringOutput

class Seek:
    """
    Una clase de comportamiento que representa el comportamiento de búsqueda para un personaje.
    Atributos:
        character: Kinematic
            El personaje que está buscando el objetivo.
        target: Kinematic
            El objetivo que el personaje está buscando.
        maxAcceleration: float
            La aceleración máxima que el personaje puede alcanzar.
    Métodos:
        getSteering():
            Calcula y devuelve la salida de dirección para el comportamiento de búsqueda.
    """
    def __init__(self, character, target, maxAcceleration):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration

    def getSteering(self):
        result = SteeringOutput()
        # Conseguir la dirección al objetivo.
        result.linear = self.target.position - self.character.position
        # Asegurarse de que la dirección sea normalizada.
        result.linear.normalize()
        # Ajustar la dirección a la aceleración máxima.
        result.linear *= self.maxAcceleration
        result.angular = 0
        return result