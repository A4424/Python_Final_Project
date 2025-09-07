import random
import string

def generate_tail_number(length=6):
    """Genera un tail_number aleatorio tipo 'ABC123'."""
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    digits = ''.join(random.choices(string.digits, k=3))
    return letters + digits

def extract_id_from_response(response_json):
    """Extrae el ID de la respuesta JSON."""
    return response_json.get("id")
