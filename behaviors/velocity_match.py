from steering_output import SteeringOutput

class VelocityMatch:
    """
    Una clase utilizada para representar el comportamiento de coincidencia de velocidad en IA.
    Atributos
    ---------
    character : Kinematic
        El personaje que intenta igualar la velocidad.
    target : Kinematic
        El objetivo cuya velocidad el personaje intenta igualar.
    maxAcceleration : float
        La aceleración máxima que el personaje puede alcanzar.
    timeToTarget : float, opcional
        El tiempo durante el cual se debe alcanzar la velocidad objetivo (por defecto es 0.1).
    Métodos
    -------
    getSteering():
        Calcula y devuelve la salida de dirección para igualar la velocidad del objetivo.
    """
    def __init__(self, character, target, maxAcceleration, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAcceleration = maxAcceleration
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()
        # Calcular la aceleración lineal para igualar la velocidad del objetivo.
        result.linear = self.character.velocity - self.target.velocity
        # Ajustar la aceleración en función del tiempo objetivo
        result.linear /= self.timeToTarget
        # Verificar si la aceleración es demasiado rápida y si lo es ajustarla.
        if result.linear.length() > self.maxAcceleration:
            # Normalizar la aceleración lineal y ajustarla a la aceleración máxima.
            result.linear.normalize()
            result.linear *= self.maxAcceleration
        # Asegurarse de que la aceleración angular sea 0.
        result.angular = 0
        return result