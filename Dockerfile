# Utiliza la imagen oficial de Python 3.9 como base
FROM python:3.9

# Establece el directorio de trabajo en /usr/src/app
WORKDIR /usr/src/app

# Copia los archivos de la aplicación al contenedor
COPY ./app ./app

# Copia el archivo Requirements.txt y luego instala las dependencias del proyecto
RUN pip install --no-cache-dir -r ./app/Requirements.txt

# Copia el archivo prestart.sh al contenedor
COPY ./start_server.sh .
COPY ./init_db.sh .
ENV PYTHONPATH=/app
# Expone el puerto 3000 para que pueda ser accedido externamente
EXPOSE 3000

# Define el comando predeterminado para ejecutar la aplicación
CMD ["bash", "./start_server.sh"]