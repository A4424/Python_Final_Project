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

    def login_user(self, username, password):
        """
        Realiza una solicitud de login a la API.

        :param username: Nombre de usuario para el login.
        :param password: Clave de acceso del usuario.
        :return: Tupla con el token de acceso y el código de estado HTTP.
                 (access_token, status_code)
        """
        url = f"{self.base_url}{self.login_endpoint}"

        # Se prepara el payload según la configuración
        if self.login_as_form:
            # Los datos se envían como form-urlencoded
            payload = {
                "username": username,
                "password": password
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        else:
            # Los datos se enviarían como JSON (no se usará en este caso)
            payload = {
                "email": username,
                "password": password
            }
            headers = {
                "Content-Type": "application/json"
            }

        try:
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()  # Se eleva una excepción para códigos de error HTTP

            # Se valida el esquema de la respuesta
            response_json = response.json()
            # La validación se omite por ahora, ya que no se tiene el esquema de la respuesta

            # Se obtiene el token
            access_token = response_json.get("access_token")
            return access_token, response.status_code

        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e}")
            return None, e.response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
            return None, None
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error al procesar la respuesta JSON: {e}")
            return None, response.status_code if 'response' in locals() else None


# Para fines de prueba
if __name__ == "__main__":
    from config.config import config

    api = LoginAPI()
    print("Intentando login...")
    token, status = api.login_user(config.ADMIN_USER, config.ADMIN_PASSWORD)
    if token:
        print(f"Login exitoso! Token: {token[:10]}...")
        print(f"Código de estado: {status}")
    else:
        print(f"Login fallido. Código de estado: {status}")