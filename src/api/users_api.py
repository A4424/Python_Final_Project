#Cliente mínimo para validar el token con /users/me - Archivo: src/api/users_api.py
import requests
from typing import Dict, Any


class UsersAPI:
    def __init__(self, base_url: str, me_endpoint: str = "/users/me"):
        self.base_url = base_url.rstrip("/")
        self.me_endpoint = me_endpoint

    def get_me(self, token: str) -> Dict[str, Any]:
        url = f"{self.base_url}{self.me_endpoint}"
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        try:
            resp = requests.get(url, headers=headers)
            resp.raise_for_status()
            data = resp.json()
            data["status_code"] = resp.status_code
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}
