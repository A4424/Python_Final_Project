# Archivo: src/api/signup_api.py

import requests
from typing import Dict, Any

class SignupAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.endpoint = "/auth/signup"

    def signup_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{self.endpoint}"
        # Se imprime la URL y los datos que se enviarán
        print(f"\nEnviando petición a: {url}")
        print(f"Datos de usuario: {user_data}")

        try:
            response = requests.post(url, headers=self.headers, json=user_data)
            # Se añade esta línea para guardar el status_code en la respuesta
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Ahora el diccionario de error incluye el status_code
            if e.response is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}