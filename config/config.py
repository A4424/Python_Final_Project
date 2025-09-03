# Ruta: config/config.py

#Gestionar la configuración par un entorno específico (desarrollo, pruebas, producción).

# Librería os: interactuar con el S.O.Acceder a las variables de entorno.
import os
#Librería python-dotenv, leer las claves-valor de un archivo .env
from dotenv import load_dotenv

# Se carga el archivo .env: Se llama a la función para que se ejecute la carga de las variables.
load_dotenv()

#Se agrupan diferentes tipos de datos, como URLs base, endpoints, credenciales y opciones de formato de datos (payload).
class Config:
    # URL base del proyecto
    BASE_URL = "https://cf-automation-airline-api.onrender.com"

    # Endpoints principales de autenticación
    SIGNUP_ENDPOINT = "/auth/signup"
    LOGIN_ENDPOINT = "/auth/login"

    # Endpoints de aeronaves
    AIRCRAFTS_ENDPOINT = "/aircrafts"

    # Credenciales admin obtenidas desde el entorno (.env)
    ADMIN_USER = os.getenv('ADMIN_USER')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

    # Cómo envía el payload de login:
    # True  -> application/x-www-form-urlencoded con campos: username, password
    # False -> application/json con campos: username, password
    LOGIN_AS_FORM = True #Se evidenció en esta versión - 01-09-25, no se pudo adaptar al formato del contrato que indicaba Json.

# Se crea una instancia de la clase (config = Config()) para que todas las configuraciones
# sean fácilmente accesibles desde cualquier otra parte del código de las pruebas.
config = Config()

