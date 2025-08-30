## Autor
Adriana L. Loretán

# Python Final Project - QA Testing
![Python](https://img.shields.io/badge/python-3.12-blue)
![Pytest](https://img.shields.io/badge/pytest-8.4.1-orange)
![Status](https://img.shields.io/badge/build-passing-brightgreen)

## Descripción
Proyecto de pruebas automatizadas en Python con Pytest para la validación de la API de aerolíneas: `https://cf-automation-airline-api.onrender.com`. El framework se enfoca en validar las operaciones CRUD (Create, Read, Update, Delete) del endpoint `/aircrafts`, incluyendo la autenticación. Se utiliza la parametrización de datos con archivos CSV para cubrir tanto el happy path como los escenarios de error, asegurando un framework modular y de fácil mantenimiento.

---
## Tecnologías
- Python 3.12
- Pytest 8.4.1
- Virtual environment (`venv`)
- `requests`
- `pandas`
- `pytest-html`
- `allure-pytest`

---
## Estructura del proyecto
- `config/`: Contiene el archivo de configuración con URLs y credenciales.
- `data/`: Almacena los archivos CSV con los datos de prueba.
- `src/`: Contiene el código fuente de los clientes de la API.
- `tests/`: Contiene los tests, organizados por funcionalidad.
- `conftest.py`: Archivo para definir fixtures y compartir la lógica de autenticación.
- `pytest.ini`: Archivo de configuración para Pytest y marcadores.
- `requirements.txt`: Archivo con todas las dependencias del proyecto.

---
## Configuración e Instalación
1. Clonar el repositorio.
2. Navegar a la carpeta del proyecto.
3. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   
## Instalar las dependencias, desde la terminal:
pip install -r requirements.txt

## Ejecución de tests
- Para correr todos los tests: pytest

- Para ejecutar tests con marcadores específicos, utiliza la opción -m:

- Ejecutar solo los tests de validación básica: pytest -m smoke

-Ejecutar solo los tests del happy path: pytest -m happy_path

-Ejecutar solo los tests de error: pytest -m error

- Para ejecutar y generar un informe HTML: pytest --html=report.html

- Para ejecutar y generar un reporte con Allure: pytest --alluredir=./allure-results
allure serve ./allure-results

## Resultado Esperado
Al ejecutar los tests, se debería obtener un resultado similar al siguiente, mostrando que las pruebas de autenticación y CRUD han pasado exitosamente:

collected X items

tests/auth/test_login.py::test_login_success_and_validate_me PASSED
tests/auth/test_login.py::test_login_with_wrong_password PASSED
tests/auth/test_login.py::test_login_non_existing_user PASSED
tests/auth/test_login.py::test_login_invalid_payload PASSED
tests/auth/test_singup.py::test_signup_successful PASSED
tests/auth/test_singup.py::test_signup_existing_user PASSED
tests/auth/test_singup.py::test_signup_with_invalid_email PASSED

tests/aircrafts/test_aircrafts.py::test_create_aircraft_happy_path PASSED
tests/aircrafts/test_aircrafts.py::test_create_aircraft_error_cases PASSED
tests/aircrafts/test_aircrafts.py::test_get_aircrafts PASSED
tests/aircrafts/test_aircrafts.py::test_get_aircraft_by_id PASSED
tests/aircrafts/test_aircrafts.py::test_update_aircraft PASSED
tests/aircrafts/test_aircrafts.py::test_delete_aircraft PASSED

X passed in XX.XXs