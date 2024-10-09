from steering_output import SteeringOutput

class Separation:
    """
    Comportamiento de separación para un personaje para evitar el hacinamiento manteniendo una distancia de otros objetivos.
    Atributos:
        character: Kinematic
            El personaje que está realizando la separación.
        targets: List[Kinematic]
            La lista de objetivos a evitar.
        player: Kinematic
            El jugador cuya velocidad se debe igualar.
        maxAcceleration: float
            La aceleración máxima que el personaje puede alcanzar.
        threshold: float
            La distancia dentro de la cual se activa el comportamiento de separación.
        decayCoefficient: float
            El coeficiente utilizado para calcular la fuerza de separación.
        timeToTarget: float
            El tiempo durante el cual el personaje iguala la velocidad del jugador.
    Métodos:
        getSteering() -> SteeringOutput:
            Calcula y devuelve la salida de dirección para el comportamiento de separación.
    """
    def __init__(self, character, targets, player, maxAcceleration, threshold, decayCoefficient, timeToTarget = 0.1):
        self.character= character
        self.targets = targets
        self.player= player
        self.maxAcceleration = maxAcceleration
        self.threshold= threshold
        self.decayCoefficient = decayCoefficient
        self.timeToTarget= timeToTarget

    def getSteering(self) -> SteeringOutput:
        steering: SteeringOutput = SteeringOutput()
        # Igualar la velocidad del personaje con la del jugador.
        steering.linear = self.player.velocity
        # Ajustar la aceleración en función del tiempo objetivo
        steering.linear /= self.timeToTarget
        # Verificar si la aceleración es demasiado rápida y si lo es ajustarla.
        if steering.linear.length() > self.maxAcceleration:
            steering.linear = steering.linear.normalize() * self.maxAcceleration
        # Asegurarse de que la aceleración angular sea 0.
        steering.angular = 0
        # Iterar sobre los objetivos y calcular la separación.
        for target in self.targets:
            # Calcular la dirección y la distancia al objetivo.
            direction = self.character.position - target.position 
            distance = direction.length()
            # Si el objetivo está dentro del radio de separación, calcular la fuerza de separación
            if distance < self.threshold:
                # Calcular la fuerza de separación
                strength = min(self.decayCoefficient / (distance ** 2) if distance != 0 else 0, self.maxAcceleration)
                # Calcular la dirección de la fuerza de separación y normalizarla
                direction = direction.normalize()
                # Añadir la fuerza de separación a la aceleración lineal
                steering.linear += direction * strength
        return steering