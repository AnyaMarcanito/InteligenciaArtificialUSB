from behaviors.seek import Seek
from kinematic import Kinematic

class Pursue(Seek):
    """
    Comportamiento de persecución para que un personaje siga a un objetivo en movimiento.
    Hereda del comportamiento Seek y añade predicción para tener en cuenta el movimiento del objetivo.

    Atributos:
        character: Kinematic
            El personaje que persigue al objetivo.
        target: Kinematic
            El objetivo que el personaje está persiguiendo.
        maxAcceleration: float
            La aceleración máxima del personaje.
        maxPrediction: float
            El tiempo máximo de predicción para anticipar la futura posición del objetivo.

    Métodos:
        getSteering():
            Calcula la salida de dirección para perseguir al objetivo, teniendo en cuenta la futura posición del objetivo.
    """
    def __init__(self, character, target, maxAcceleration, maxPrediction):
        super().__init__(character, target, maxAcceleration)
        self.maxPrediction = maxPrediction

    def getSteering(self):
        # Calcular la dirección y la distancia al objetivo.
        direction = self.target.position - self.character.position
        distance = direction.length()
        # Conseguir la velocidad actual del personaje.
        speed = self.character.velocity.length()
        # Verificar si la velocidad del personaje es menor o igual a la distancia 
        # al objetivo dividida por el tiempo máximo de predicción.
        if speed <= distance / self.maxPrediction:
            # Si es así, usar el tiempo máximo de predicción.
            prediction = self.maxPrediction
        else:
            # De lo contrario, usar la distancia al objetivo dividida por la velocidad del personaje.
            prediction = distance / speed
        # Calcular la posición futura del objetivo.
        explicitTarget = self.target.position + self.target.velocity * prediction
        # Crear un objetivo temporal para Seek.
        temp_target = Kinematic(explicitTarget, 0, self.target.velocity, 0)
        # Guardar el objetivo original.
        original_target = self.target
        # Asignar el objetivo temporal.
        self.target = temp_target
        # Delegar a Seek
        steering = super().getSteering()
        # Restaurar el objetivo original
        self.target = original_target
        return steering