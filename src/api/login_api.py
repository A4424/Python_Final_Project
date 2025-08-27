#Cliente de API de Login - Archivo: src / api / login_api.py
import requests
from typing import Dict, Any, Optional


class LoginAPI:
    def __init__(self, base_url: str, endpoint: str = "/auth/login", as_form: bool = True):
        self.base_url = base_url.rstrip("/")
        self.endpoint = endpoint
        self.as_form = as_form
        # headers "base"; se ajustan dinámicamente según content-type
        self.headers_json = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.headers_form = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def login_user(self, identifier: str, password: str) -> Dict[str, Any]:
        """
        Retorna:
            - En éxito: dict con el JSON de la API (p.ej., {"access_token": "...", "token_type": "bearer", ...})
            - En error : {"error": str, "status_code": <int opcional>}
        """
        url = f"{self.base_url}{self.endpoint}"

        try:
            if self.as_form:
                # Típico de FastAPI con OAuth2PasswordRequestForm: username + password
                payload = {"username": identifier, "password": password}
                response = requests.post(url, headers=self.headers_form, data=payload)
            else:
                # Contratos que esperan JSON con email + password
                payload = {"email": identifier, "password": password}
                response = requests.post(url, headers=self.headers_json, json=payload)

            response.raise_for_status()
            data = response.json()
            # Normalizo status_code para facilitar asserts en tests
            data["status_code"] = response.status_code
            return data

        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}

    @staticmethod
    def auth_header(access_token: str) -> Dict[str, str]:
        return {"Authorization": f"Bearer {access_token}", "accept": "application/json"}

