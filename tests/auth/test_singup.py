# Archivo: tests/test_signup.py
import pytest
from src.api.signup_api import SignupAPI
# tests/auth/test_login.py
from config.config import config as project_config

import uuid


@pytest.fixture
def signup_client():
    return SignupAPI(project_config.BASE_URL)

def test_signup_successful(signup_client):
    unique_email = f"test_user_{uuid.uuid4()}@example.com"
    user_data = {
        "email": unique_email,
        "password": "secure_password_123",
        "full_name": "Test User"
    }

    response = signup_client.signup_user(user_data)

    assert "id" in response
    assert response.get("email") == unique_email
    assert response.get("full_name") == "Test User"

def test_signup_existing_user(signup_client):
    existing_user_data = {
        "email": "existing_user@example.com",
        "password": "some_password",
        "full_name": "Existing User"
    }

    signup_client.signup_user(existing_user_data)
    response = signup_client.signup_user(existing_user_data)

    assert "error" in response
    assert response.get("status_code") == 400
    # Se valida que el mensaje contenga el código de error en lugar de un mensaje específico.
    assert "400 Client Error" in response.get("error", "")

def test_signup_with_invalid_email(signup_client):
    invalid_user_data = {
        "email": "invalid-email",
        "password": "test_password",
        "full_name": "Invalid User"
    }

    response = signup_client.signup_user(invalid_user_data)

    assert "error" in response
    assert response.get("status_code") == 422
    # Se valida que el mensaje contenga el código de error en lugar de un mensaje específico.
    assert "422 Client Error" in response.get("error", "")