import requests

class AircraftsAPI:
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Cambiar según tu API
        self.endpoint = "/aircrafts"
        self.headers = {}

    def set_token(self, token):
        self.headers = {"Authorization": f"Bearer {token}"}

    def create_aircraft(self, payload):
        return requests.post(f"{self.base_url}{self.endpoint}", json=payload, headers=self.headers)

    def get_aircraft(self, aircraft_id):
        return requests.get(f"{self.base_url}{self.endpoint}/{aircraft_id}", headers=self.headers)

    def update_aircraft(self, aircraft_id, payload):
        return requests.put(f"{self.base_url}{self.endpoint}/{aircraft_id}", json=payload, headers=self.headers)

    def delete_aircraft(self, aircraft_id):
        return requests.delete(f"{self.base_url}{self.endpoint}/{aircraft_id}", headers=self.headers)
