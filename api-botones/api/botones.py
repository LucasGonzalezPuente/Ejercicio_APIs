from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from model.boton import Boton
from schemas.boton_schema import BotonBase, BotonResponse, BotonUpdate
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

router = APIRouter(prefix="/botones", tags=["Botones"])

# Conexión a MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URL)
db = client["sialitech_db"]
coleccion = db["botones"]

# Documentos mongo pasados a disct para que sea compatible con Pydantic
def m_doc(doc):
    if not doc: return None
    doc["id"] = str(doc["_id"]) # ObjectId de Mongo a string
    return doc

@router.post("/", response_model=BotonResponse)
async def crear_boton(data: BotonBase):
    if coleccion.find_one({"nombre": data.nombre}):
        raise HTTPException(status_code=400, detail="El nombre ya existe")
    
    nuevo_doc = {
        "nombre": data.nombre,
        "color": data.color,
        "estado": False,
        "fecha_creacion": datetime.now()  # <--- CAMBIA ESTO
    }
    resultado = coleccion.insert_one(nuevo_doc)
    return m_doc(coleccion.find_one({"_id": resultado.inserted_id}))



@router.get("/", response_model=List[BotonResponse])
async def listar_botones():
    """Devuelve todos los botones guardados en la DB"""
    botones = list(coleccion.find())
    return [m_doc(b) for b in botones]

@router.get("/buscar", response_model=BotonResponse)
async def leer_boton(id: Optional[str] = None, nombre: Optional[str] = None):
    """Busca por ID (ObjectId de Mongo) o por nombre"""
    filtro = {}
    if id:
        try:
            filtro = {"_id": ObjectId(id)}
        except:
            raise HTTPException(status_code=400, detail="ID no válido")
    elif nombre:
        filtro = {"nombre": nombre}
    else:
        raise HTTPException(status_code=400, detail="Debes proporcionar id o nombre")

    resultado = coleccion.find_one(filtro)
    if not resultado:
        raise HTTPException(status_code=404, detail="Botón no encontrado")
    return m_doc(resultado)

@router.put("/{nombre}")
async def editar_boton(nombre: str, update: dict):
    resultado = coleccion.find_one_and_update(
        {"nombre": nombre},
        {"$set": update},
        return_document=True
    )
    if not resultado:
        raise HTTPException(status_code=404, detail="Botón no encontrado")
    return {"status": "success", "data": m_doc(resultado)}

@router.delete("/{nombre}")
async def borrar_boton(nombre: str):
    resultado = coleccion.delete_one({"nombre": nombre})
    if resultado.deleted_count > 0:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Botón no encontrado")