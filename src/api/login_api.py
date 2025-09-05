# Ruta src/api/login_api.py
import requests
import json
from ..schemas.login_schemas import login_schema
from jsonschema import validate, ValidationError
from config.config import config

class LoginAPI:
    def __init__(self):
        self.base_url = config.BASE_URL
        self.login_endpoint = config.LOGIN_ENDPOINT
        self.login_as_form = config.LOGIN_AS_FORM
        self.access_token = None

    def login_user(self, username, password):
        """
        Realiza una solicitud de login a la API.

        :param username: Nombre de usuario para el login.
        :param password: Clave de acceso del usuario.
        :return: Tupla con el token de acceso y el código de estado HTTP.
                 (access_token, status_code)
        """
        url = f"{self.base_url}{self.login_endpoint}"

        if self.login_as_form:
            payload = {
                "username": username,
                "password": password
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        else:
            payload = {
                "email": username,
                "password": password
            }
            headers = {
                "Content-Type": "application/json"
            }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()

            response_json = response.json()

            # Se obtiene el token de acceso
            raw_token = response_json.get("access_token")

            # Se verifica si el token existe y se le agrega el prefijo "Bearer "
            if raw_token:
                self.access_token = f"Bearer {raw_token}"
            else:
                self.access_token = None

            print(f"Token obtenido y almacenado: {self.access_token}")

            return self.access_token, response.status_code

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            return None, e.response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None, None
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta JSON: {e}")
            return None, response.status_code if 'response' in locals() else None

    def get_token(self):
        return self.access_token

# TEST DE HUMO
# Prueba de conexión manual confirma que el módulo login_api es capaz de realizar una solicitud
# de login exitosa a la API utilizando las credenciales de administrador configuradas en las
# variables de entorno.
# if __name__ == "__main__":
#     from config.config import config
#
#     api = LoginAPI()
#     print("Intentando login...")
#     token, status = api.login_user(config.ADMIN_USER, config.ADMIN_PASSWORD)
#     if token:
#         print(f"Login exitoso! Token: {token[:10]}...")
#         print(f"Código de estado: {status}")
#     else:
#         print(f"Login fallido. Código de estado: {status}")


# ##PRUEBA CON form-urlencoded ####
# import requests
#
# url = "https://cf-automation-airline-api.onrender.com/auth/login"
#
# payload = {
#     "username": "admin@demo.com",
#     "password": "admin123",
# }
#
# headers = {
#     "Content-Type": "application/x-www-form-urlencoded"
# }
#
# response = requests.post(url, data=payload, headers=headers)
#
# print(response.status_code)
# print(response.text)