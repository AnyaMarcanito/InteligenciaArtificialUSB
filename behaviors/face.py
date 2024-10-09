from behaviors.align import Align
from steering_output import SteeringOutput
import math
class Face(Align):
    """
    Clase de comportamiento Face que hereda de Align.
    Esta clase es responsable de hacer que un personaje mire hacia un objetivo 
    calculando la orientación adecuada y delegando la alineación al comportamiento Align.
    Atributos:
        character: Kinematic
            El personaje que realizará el comportamiento de mirar.
        target: Kinematic
            El objetivo al que el personaje mirará.
        maxAngularAcceleration: float
            La aceleración angular máxima permitida.
        maxRotation: float
            La rotación máxima permitida.
        targetRadius: float
            El radio dentro del cual se considera que el personaje ha alcanzado la orientación objetivo.
        slowRadius: float
            El radio dentro del cual el personaje comenzará a desacelerar.
        timeToTarget: float
            El tiempo durante el cual se debe alcanzar la velocidad objetivo.
    Métodos:
        getSteering():
            Calcula la salida de dirección para hacer que el personaje mire hacia el objetivo.
    """
    def __init__(self, character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget=0.1):
        super().__init__(character, target, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)

    def getSteering(self):
        # Calcular la dirección al objetivo.
        direction = self.target.position - self.character.position
        # Revisar si el objetivo está fuera del radio de alineación.
        if direction.length() == 0:
            return SteeringOutput()
        # Calcular la orientación explícita al objetivo.
        explicitTarget = self.target
        explicitTarget.orientation = math.atan2(direction.y, direction.x)
        # Delegar a Align el cálculo de la salida de dirección.
        self.target = explicitTarget
        return super().getSteering()