# URL base  del proyecto
# BASE_URL = "https://cf-automation-airline-api.onrender.com"


# Endpoints principales de autenticación
#SIGNUP_ENDPOINT = "/auth/signup"
#LOGIN_ENDPOINT = "/auth/login"

#Endpoints de aeropuertos
#POST_AIRCRAFTS= "/airports"

# Credenciales de usuario admin (para login y operaciones restringidas)
#ADMIN_USER = "admin"
#ADMIN_PASSWORD = "admin123"

# ---------------------------------------------------------------------------------------------
# NUEVA CONFIGURACIÓN 26-08-25  ---------------------------------------------------------------

class Config:
    # URL base del proyecto
    BASE_URL = "https://cf-automation-airline-api.onrender.com"

    # Endpoints principales de autenticación
    SIGNUP_ENDPOINT = "/auth/signup"
    LOGIN_ENDPOINT = "/auth/login"

    # Endpoints de usuarios
    USERS_ME_ENDPOINT = "/users/me"

    # Endpoints de aeropuertos (lo que ya tenías)
    POST_AIRCRAFTS = "/airports"

    # Credenciales admin
    ADMIN_USER = "admin"
    ADMIN_PASSWORD = "admin123"

    # Cómo envía el payload de login:
    # True  -> application/x-www-form-urlencoded con campos: username, password
    # False -> application/json con campos: email, password
    LOGIN_AS_FORM = True

# Para mantener compatibilidad con tu import actual:
config = Config()
