# Usa una imagen base
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios
COPY . .

# Instala las dependencias
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expone el puerto (por ejemplo 8000 para Django)
EXPOSE 8000

# Comando para arrancar
CMD ["gunicorn", "apiboatgraphql.wsgi:application", "--bind", "0.0.0.0:8000"]
