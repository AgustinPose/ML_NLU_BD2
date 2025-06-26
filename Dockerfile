# Imagen base oficial de Python 3.11
FROM python:3.11-slim

# Evita preguntas interactivas en install
ENV DEBIAN_FRONTEND=noninteractive

# Setea directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt ./
COPY ML.py ./
# Si necesitas el .sql, descomenta la siguiente línea
# COPY obligatorio_bd2.sql ./

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Por defecto, ejecuta tu script (podés cambiarlo según quieras)
CMD ["python", "ML.py"]
