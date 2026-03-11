from fastapi import FastAPI
from api.botones import router as botones_router

app = FastAPI(title="Formación Botones Sialitech")


app.include_router(botones_router)

@app.get("/")
async def root():
    return {"message": "API de Botones Operativa"}