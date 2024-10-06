from vector import Vector
from kinematic import Kinematic, Seek, Arrive, KinematicWander, Flee, Align

def crear_personaje(posicion, velocidad, tipo, imagen, target_personaje=None):
    # Crear instancia de Kinematic para el personaje
    kinematic = Kinematic(posicion, 0, velocidad, 0)

    # Definir el objetivo según el parámetro target_personaje
    if target_personaje:
        target_kinematic = target_personaje.kinematic
    else:
        target_kinematic = None

    # Crear el personaje según el tipo
    if tipo == 'wander':
        personaje = KinematicWander(kinematic, 90, 1.0)
    elif tipo == 'seek':
        if not target_kinematic:
            target_kinematic = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0)
        personaje = Seek(kinematic, target_kinematic, 300)
    elif tipo == 'arrive':
        if not target_kinematic:
            target_kinematic = Kinematic(Vector(500, 500), 0, Vector(0, 0), 0)
        personaje = Arrive(kinematic, target_kinematic, 100, 300, 10, 5)
    elif tipo == 'flee':
        if not target_kinematic:
            target_kinematic = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0)
        personaje = Flee(kinematic, target_kinematic, 600)
    elif tipo == 'align':
        if not target_kinematic:
            target_kinematic = Kinematic(Vector(100, 100), 0, Vector(100, 100), 0)
        personaje = Align(kinematic, target_kinematic, maxAngularAcceleration=2000, maxRotation=100, targetRadius=0.1, slowRadius=1)
    elif tipo == 'player':
        personaje = Kinematic(kinematic, 0, 0, 0)
    else:
        raise ValueError(f"Tipo de personaje desconocido: {tipo}")
    
    # Asignar la imagen al personaje
    personaje.image = imagen
    personaje.kinematic = kinematic  
    personaje.behavior = tipo
    
    return personaje