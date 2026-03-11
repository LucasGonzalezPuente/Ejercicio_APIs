# 1. Usamos la imagen oficial de FastAPI (basada en Python)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requerimientos (si tienes uno) o instalamos directo
# En este caso, como es básico, instalamos las librerías necesarias
RUN pip install --no-cache-dir fastapi uvicorn

# 4. Copiamos todo el contenido de tu carpeta local al contenedor
COPY . /app

# 5. Exponemos el puerto en el que correrá la app (por defecto 80)
EXPOSE 80

# El comando de inicio ya viene configurado en la imagen de tiangolo, 
# pero podemos sobrescribirlo para asegurar que use nuestro main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]