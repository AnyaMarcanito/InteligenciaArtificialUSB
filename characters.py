from vector import Vector
from kinematic import Kinematic, Seek, Arrive, KinematicWander, Flee

def crear_personajes():
    # Crear instancias de Kinematic para los personajes
    position_wander = Vector(100, 100)
    velocity_wander = Vector(5, 0)
    kinematic_wander = Kinematic(position_wander, 0, velocity_wander, 0)

    position_seek = Vector(200, 200)
    velocity_seek = Vector(10, 0)
    kinematic_seek = Kinematic(position_seek, 0, velocity_seek, 0)

    position_arrive = Vector(300, 300)
    velocity_arrive = Vector(0, 0)
    kinematic_arrive = Kinematic(position_arrive, 0, velocity_arrive, 0)

    position_flee = Vector(400, 400)
    velocity_flee = Vector(20, 0)
    kinematic_flee = Kinematic(position_flee, 0, velocity_flee, 0)

    # Crear instancias de los algoritmos de movimiento con valores aumentados
    wander = KinematicWander(kinematic_wander, 200, 1.0)  # Aumentar maxSpeed y maxRotation
    seek_target = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)  # Objetivo para Seek
    seek = Seek(kinematic_seek, seek_target, 300)  # Aumentar maxAcceleration
    arrive_target = Kinematic(Vector(500, 500), 0, Vector(0, 0), 0)  # Objetivo para Arrive
    arrive = Arrive(kinematic_arrive, arrive_target, 10, 20, 5, 50)  # Aumentar maxAcceleration y maxSpeed
    flee_target = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)  # Objetivo para Flee
    flee = Flee(kinematic_flee, flee_target, 0)  # Aumentar maxAcceleration

    return wander, seek, arrive, flee