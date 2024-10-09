import random
import math
from vector import Vector
from behaviors.face import Face
from kinematic import Kinematic
from behaviors.seek import Seek

class Wander(Face):
    """
    Comportamiento de deambulación para un personaje en un espacio 2D.
    Esta clase hereda del comportamiento Face e implementa el comportamiento de deambulación
    cambiando aleatoriamente la orientación del personaje y moviéndose hacia una posición objetivo
    en un círculo alrededor del personaje.

    Atributos:
        character: Kinematic
            El personaje que deambula.
        wanderOffset: float
            Distancia desde el personaje hasta el centro del círculo de deambulación.
        wanderRadius: float
            Radio del círculo de deambulación.
        wanderRate: float
            Tasa máxima a la que puede cambiar la orientación de deambulación.
        maxAcceleration: float
            Aceleración lineal máxima del personaje.
    Métodos:
        randomBinomial():
            Genera un número aleatorio entre -1 y 1 usando una distribución binomial.
        getSteering():
            Calcula la salida de dirección para el comportamiento de deambulación, incluyendo la actualización
            de la posición objetivo y delegando en los comportamientos de face y seek.

    """
    def __init__(self, character, wanderOffset, wanderRadius, wanderRate, maxAcceleration):
        super().__init__(character, None, maxAngularAcceleration=0, maxRotation=0, targetRadius=0, slowRadius=0)
        self.wanderOffset = wanderOffset
        self.wanderRadius = wanderRadius
        self.wanderRate = wanderRate
        self.wanderOrientation = 0
        self.maxAcceleration = maxAcceleration
        self.target = Kinematic(Vector(0, 0), 0, Vector(0, 0), 0) 
        self.seek = Seek(character, self.target, maxAcceleration)

    def randomBinomial(self):
        return random.random() - random.random()

    def getSteering(self):
        # Actualizar la orientación de deambulación.
        self.wanderOrientation += self.randomBinomial() * self.wanderRate
        # Calcular la orientación objetivo.
        targetOrientation = self.wanderOrientation + self.character.orientation
        # Calcular el centro del círculo de deambulación.
        wanderCircleCenter = self.character.position + Vector(math.cos(self.character.orientation), math.sin(self.character.orientation)) * self.wanderOffset
        # Calcular la posición objetivo en el círculo de deambulación.
        target = wanderCircleCenter + Vector(math.cos(targetOrientation), math.sin(targetOrientation)) * self.wanderRadius
        # Actualizar la posición objetivo.
        self.target.position = target
        # Delegar a Face para orientar al personaje hacia la posición objetivo.
        result = super().getSteering()
        # Delegar a Seek para mover al personaje hacia la posición objetivo.
        seekSteering = self.seek.getSteering()
        # Combinar las aceleraciones lineales de Face y Seek.
        result.linear = seekSteering.linear
        return result