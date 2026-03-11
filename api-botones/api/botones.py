from fastapi import APIRouter, HTTPException
from typing import List
from model.boton import Boton
from schemas.boton_schema import BotonBase, BotonResponse, BotonUpdate

router = APIRouter(prefix="/botones", tags=["Botones"])

# Almacenamiento temporal
db_botones: List[Boton] = []
id_counter = 1

@router.post("/", response_model=BotonResponse)
async def crear_boton(data: BotonBase):
    """
    Create a new button.
    Args:
    - data (BotonBase): name and color for the new button.
    Returns:
    - BotonResponse: the created button data.
    """
    global id_counter
    if any(b.nombre == data.nombre for b in db_botones):
        raise HTTPException(status_code=400, detail="El nombre ya existe")
    
    nuevo = Boton(id=id_counter, nombre=data.nombre, color=data.color)
    db_botones.append(nuevo)
    id_counter += 1
    return nuevo

@router.get("/{nombre}", response_model=BotonResponse)
async def leer_boton(nombre: str):
    """
    Read a button by name.
    Args:
    - nombre (str): name of the button to retrieve.
    Returns:
    - BotonResponse: the data of the button.
    """
    for b in db_botones:
        if b.nombre == nombre:
            return b
    raise HTTPException(status_code=404, detail="Botón no encontrado")

@router.put("/{nombre}")
async def editar_boton(nombre: str, update: dict):
    """
    Update a button.
    Args:
    - nombre (str): name of the button to set the value.
    - update (dict): par key/value to set.
    Returns:
    - dict: {"status": "success"}.
    """
    for b in db_botones:
        if b.nombre == nombre:
            if "nombre" in update: b.nombre = update["nombre"]
            if "color" in update: b.color = update["color"]
            if "estado" in update: b.estado = update["estado"]
            return {"status": "success", "data": b}
    raise HTTPException(status_code=404, detail="Botón no encontrado")

@router.delete("/{nombre}")
async def borrar_boton(nombre: str):
    """
    Delete a button by name.
    Args:
    - nombre (str): name of the button to delete.
    Returns:
    - dict: {"status": "success"}.
    """
    global db_botones
    original_size = len(db_botones)
    db_botones = [b for b in db_botones if b.nombre != nombre]
    if len(db_botones) < original_size:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Botón no encontrado")