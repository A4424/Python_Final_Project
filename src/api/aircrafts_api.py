#Ruta: src/api/aircrafts_api.py
# Archivo: src/api/aircrafts_api.py
import requests

class AircraftsAPI:
    def __init__(self, token, base_url="https://cf-automation-airline-api.onrender.com"):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    def create_aircraft(self, aircraft_data):
        url = f"{self.base_url}/aircrafts"
        response = requests.post(url, json=aircraft_data, headers=self.headers)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, {}

    def get_aircraft_by_id(self, aircraft_id):
        url = f"{self.base_url}/aircrafts/{aircraft_id}"
        response = requests.get(url, headers=self.headers)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, {}

    def get_all_aircrafts(self, params=None):
        url = f"{self.base_url}/aircrafts"
        response = requests.get(url, headers=self.headers, params=params)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, []

    def update_aircraft(self, aircraft_id, aircraft_data):
        url = f"{self.base_url}/aircrafts/{aircraft_id}"
        response = requests.put(url, json=aircraft_data, headers=self.headers)
        try:
            return response.status_code, response.json()
        except ValueError:
            return response.status_code, {}

    def delete_aircraft(self, aircraft_id):
        url = f"{self.base_url}/aircrafts/{aircraft_id}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code
