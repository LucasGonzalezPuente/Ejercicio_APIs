from datetime import datetime
from pydantic import BaseModel, Field

class Boton: #defino la clase fisica
    def __init__(self, id: int, nombre: str, color: str):
        self.id = id
        self.nombre = nombre
        self.estado = False
        self.color = color
        self.fecha_creacion = datetime.now()


