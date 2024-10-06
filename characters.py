from vector import Vector
from kinematic import Kinematic, Seek, Arrive, KinematicWander, Flee

def crear_personaje(posicion, velocidad, tipo, imagen):
    # Crear instancia de Kinematic para el personaje
    kinematic = Kinematic(posicion, 0, velocidad, 0)

    # Crear el personaje según el tipo
    if tipo == 'wander':
        personaje = KinematicWander(kinematic, 200, 1.0)
    elif tipo == 'seek':
        seek_target = Kinematic(Vector(400, 400), 0, Vector(0, 0), 0) 
        personaje = Seek(kinematic, seek_target, 300)
    elif tipo == 'arrive':
        arrive_target = Kinematic(Vector(500, 500), 0, Vector(0, 0), 0) 
        personaje = Arrive(kinematic, arrive_target, 10, 20, 5, 50) 
    elif tipo == 'flee':
        flee_target = Kinematic(Vector(100, 100), 0, Vector(0, 0), 0) 
        personaje = Flee(kinematic, flee_target, 0) 
    else:
        raise ValueError(f"Tipo de personaje desconocido: {tipo}")
    
    # Asignar la imagen al personaje
    personaje.image = imagen


    return personaje