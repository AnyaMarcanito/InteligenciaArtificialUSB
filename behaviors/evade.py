from behaviors.flee import Flee
from steering_output import SteeringOutput
from kinematic import Kinematic
from vector import Vector

class Evade(Flee):
    """
    Comportamiento de evasión para que un personaje evite un objetivo en movimiento.
    Hereda de:
        Flee: La clase base para el comportamiento de huida.
    Atributos:
        character: Kinematic
            El personaje que está evadiendo.
        target: Kinematic
            El objetivo del que el personaje está evadiendo.
        maxAcceleration: float 
            La aceleración máxima del personaje.
        maxPrediction: float
            El tiempo máximo de predicción para estimar la posición futura del objetivo.
        fleeRadius: float
            El radio dentro del cual el personaje comenzará a evadir.
    Métodos:
        getSteering():
            Calcula la salida de dirección para el comportamiento de evasión.
            Devuelve un objeto SteeringOutput con las aceleraciones lineales y angulares calculadas.
    """
    def __init__(self, character, target, maxAcceleration, maxPrediction, fleeRadius):
        super().__init__(character, target, maxAcceleration, fleeRadius)
        self.maxPrediction = maxPrediction

    def getSteering(self):
        # Calcular la distancia al objetivo
        direction = self.target.position - self.character.position
        distance = direction.length()
        # Si el objetivo está fuera del radio de huida, devolver SteeringOutput con aceleraciones en cero
        if distance > self.fleeRadius:
            steering = SteeringOutput()
            steering.linear = Vector(0, 0)
            steering.angular = 0
            self.character.velocity = Vector(0, 0)
            return steering
        # Calcular la velocidad actual del objetivo
        speed = self.character.velocity.length()
        # Calcular la predicción
        if speed <= distance / self.maxPrediction:
            prediction = self.maxPrediction
        else:
            prediction = distance / speed
        # Calcular el objetivo futuro
        future_position = self.target.position + self.target.velocity * prediction
        # Crear un objetivo temporal para Flee
        temp_target = Kinematic(future_position, 0, self.target.velocity, 0)
        # Guardar el objetivo original
        original_target = self.target
        # Asignar el objetivo temporal
        self.target = temp_target
        # Delegar a Flee
        steering = super().getSteering()
        # Restaurar el objetivo original
        self.target = original_target
        return steering