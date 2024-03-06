# Login Fastapi - Genérico

Una API de login genérico básico desarrollado con FastAPI.

## Instalación

### Crear Entorno Virtual

```bash
python -m venv venv
```

### Activar entorno virtual 

#### En windows (cmd.exe)
```bash
C:\> <venv>\Scripts\activate.bat
```
#### En windows (cmd.exe)
```bash
C:\> <venv>\Scripts\activate.bat
```
#### En Linux/macOS
```bash
source <venv>/bin/activate
```
### instalar dependencias 
```bash
pip install -r Requirements.txt
```

## Configuración
1. Crear un archivo .env en la raíz del proyecto.
2. Agregar la siguiente línea al archivo .env:

```env
SECRET_KEY="Palabra_super_secreta"
```


## Inicialización

Para inicializar la aplicación, sigue estos pasos:

1. Abre la terminal en la carpeta del proyecto.
2. Ejecuta el siguiente comando:
```bash 
python scripts/init_app_script.py
```
Esto ejecutará el script de inicialización de la aplicación usando uvicorn.
