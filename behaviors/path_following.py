from behaviors.seek import Seek
from kinematic import Kinematic
from vector import Vector

class FollowPath(Seek):
    """
    Comportamiento FollowPath para que un personaje siga un camino dado con un desplazamiento.
    Hereda del comportamiento Seek para utilizar su mecanismo de dirección.
    Atributos:
        character: Kinematic
            El personaje que seguirá el camino.
        path: Path
            El camino que seguirá el personaje.
        pathOffset: float 
            El desplazamiento desde el camino a seguir.
        maxAcceleration: float
            La aceleración máxima del personaje.
        currentParam: float
            El parámetro actual en el camino.
    Métodos:
        getSteering():
            Calcula la salida de dirección para que el personaje siga el camino.
    """
    def __init__(self, character, path, pathOffset, maxAcceleration):
        super().__init__(character, None, maxAcceleration)
        self.path = path
        self.pathOffset = pathOffset
        self.currentParam = 0

    def getSteering(self):
        # Calcular el objetivo
        self.currentParam = self.path.getParam(self.character.position, self.currentParam)
        targetParam = self.currentParam + self.pathOffset
        # Conseguir la posición del objetivo
        targetPosition = self.path.getPosition(targetParam)
        # Crear un objetivo temporal
        temp_target = Kinematic(targetPosition, 0, Vector(0, 0), 0)
        self.target = temp_target
        # Delegar a Seek el cálculo de la salida de dirección
        return super().getSteering()