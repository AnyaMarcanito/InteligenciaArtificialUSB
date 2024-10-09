from vector import Vector
from steering_output import SteeringOutput
from utils.utils import mapToRange

class Align:
    """
        Comportamiento: Alinea la orientación de un personaje con la orientación de un objetivo.
        Atributos:
            character: Kinematic.
                El personaje que está siendo controlado.
            target: Kinematic.
                El objetivo con el que el personaje intenta alinearse.
            maxAngularAcceleration: float.
                La aceleración angular máxima que el personaje puede alcanzar.
            maxRotation: float.
                La velocidad de rotación máxima que el personaje puede alcanzar.
            targetRadius: float.
                El radio dentro del cual se considera que el personaje está alineado con el objetivo.
            slowRadius: float.
                El radio dentro del cual el personaje comienza a desacelerar para alinearse con el objetivo.
            timeToTarget: float.
                El tiempo durante el cual se debe alcanzar la rotación objetivo (por defecto es 0.1).
        Métodos:
            getSteering():
                Calcula la salida de dirección para alinear la orientación del personaje con la orientación del objetivo.
                Devuelve un objeto SteeringOutput con las aceleraciones lineales y angulares calculadas.
    """
    def __init__(self, character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget=0.1):
        self.character = character
        self.target = target
        self.maxAngularAcceleration = maxAngularAcceleration
        self.maxRotation = maxRotation
        self.targetRadius = targetRadius
        self.slowRadius = slowRadius
        self.timeToTarget = timeToTarget

    def getSteering(self):
        result = SteeringOutput()
        rotation = self.target.orientation - self.character.orientation
        rotation = mapToRange(rotation)
        rotationSize = abs(rotation)
        # Si el personaje ya está alineado con el objetivo, no es necesario hacer nada.
        if rotationSize < self.targetRadius:
            return result
        # Si el personaje está fuera del radio de desaceleración, la rotación es máxima.
        if rotationSize > self.slowRadius:
            targetRotation = self.maxRotation
        # Si el personaje está dentro del radio de desaceleración, la rotación se ajusta para desacelerar.
        else:
            targetRotation = self.maxRotation * rotationSize / self.slowRadius
        # Ajustar la dirección de rotación.
        targetRotation *= rotation / rotationSize
        # Calcular la aceleración angular.
        result.angular = targetRotation - self.character.rotation
        # Ajustar la aceleración angular en función del tiempo objetivo
        result.angular /= self.timeToTarget
        # Verificar si la aceleración angular es demasiado rápida y si lo es ajustarla
        angularAcceleration = abs(result.angular)
        if angularAcceleration > self.maxAngularAcceleration:
            result.angular /= angularAcceleration
            result.angular *= self.maxAngularAcceleration
        # Ajustar la aceleración lineal.
        result.linear = Vector(0, 0)
        return result