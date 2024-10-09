from behaviors.align import Align
from steering_output import SteeringOutput
import math
from kinematic import Kinematic

class LookWhereYoureGoing(Align):
    """
    LookWhereYoureGoing es una clase de comportamiento que hereda de Align. Alinea la orientación del personaje 
    con la dirección de su velocidad actual.
    Atributos:
        character: Kinematic
            El personaje al que se aplica este comportamiento.
        maxAngularAcceleration: float
            La aceleración angular máxima.
        maxRotation: float
            La rotación máxima.
        targetRadius: float
            El radio para llegar a la orientación objetivo.
        slowRadius: float
            El radio para reducir la velocidad de rotación.
        maxSpeed: float
            La velocidad máxima del personaje.
        timeToTarget: float
            El tiempo durante el cual se logra la orientación objetivo.
    Métodos:
        getSteering():
            Calcula y devuelve la salida de dirección para alinear la orientación del personaje con la dirección de su velocidad.
    """
    def __init__(self, character, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, maxSpeed, timeToTarget=0.1):
        super().__init__(character, None, maxAngularAcceleration, maxRotation, targetRadius, slowRadius, timeToTarget)
        self.maxSpeed = maxSpeed

    def getSteering(self):
        steering = SteeringOutput()
        #  Calcular la orientación del personaje.
        velocity = self.character.velocity
        # Si la velocidad es cero, no es necesario hacer nada.
        if velocity.length() == 0:
            return steering
        # Calcular la orientación
        self.character.orientation = math.atan2(velocity.y, velocity.x)
        # Crear un objetivo temporal con la posición y orientación actuales del personaje.
        temp_target = Kinematic(self.character.position, self.character.orientation, velocity, self.character.rotation)
        self.target = temp_target
        # Delegar a Align el cálculo de la salida de dirección.
        return super().getSteering()