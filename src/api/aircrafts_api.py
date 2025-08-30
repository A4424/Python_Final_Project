import requests
from typing import Dict, Any, Optional
from config.config import config # Se importa la configuración

class AircraftsAPI:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        # Se utiliza la constante de configuración en lugar de un valor fijo
        self.endpoint = config.AIRCRAFTS_ENDPOINT

    def create_aircraft(self, token: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una nueva aeronave."""
        url = f"{self.base_url}{self.endpoint}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            data["status_code"] = response.status_code
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}

    def get_all_aircrafts(self, token: str) -> Dict[str, Any]:
        """Obtiene una lista de todas las aeronaves."""
        url = f"{self.base_url}{self.endpoint}"
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            data["status_code"] = response.status_code
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}

    def get_aircraft_by_id(self, token: str, aircraft_id: str) -> Dict[str, Any]:
        """Obtiene una aeronave específica por su ID."""
        url = f"{self.base_url}{self.endpoint}/{aircraft_id}"
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            data["status_code"] = response.status_code
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}

    def update_aircraft(self, token: str, aircraft_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Actualiza una aeronave existente."""
        url = f"{self.base_url}{self.endpoint}/{aircraft_id}"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        try:
            response = requests.put(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            data["status_code"] = response.status_code
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}

    def delete_aircraft(self, token: str, aircraft_id: str) -> Dict[str, Any]:
        """Elimina una aeronave por su ID."""
        url = f"{self.base_url}{self.endpoint}/{aircraft_id}"
        headers = {"Authorization": f"Bearer {token}", "accept": "application/json"}
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            data = {"message": "Aircraft deleted successfully", "status_code": response.status_code}
            return data
        except requests.exceptions.RequestException as e:
            if getattr(e, "response", None) is not None:
                return {"error": str(e), "status_code": e.response.status_code}
            return {"error": str(e)}