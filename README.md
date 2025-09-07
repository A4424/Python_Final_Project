## Autor
Adriana L. Loretán

# Python Final Project - QA Testing# Proyecto QA - Automatización de Tests de Aeronaves y Login API

## Descripción
Este proyecto automatiza pruebas de la API de aeronaves y login, verificando:

- Creación, actualización y eliminación de aeronaves.
- Paginación y validación de datos desde CSV.
- Contratos y respuesta de la API ante credenciales correctas e incorrectas.
- Manejo de casos intermitentes y hallazgos en los logs.

## Tecnologías utilizadas
- Python 3.12
- Pytest
- Requests
- JSON Schema
- HTML Reporting (pytest-html)

## Requisitos
1. Clonar el repositorio.
2. Crear entorno virtual:

python -m venv .venv

## Activar entorno virtual:

- Windows: .venv\Scripts\activate

- Linux/Mac: source .venv/bin/activate

## Instalar dependencias:
pip install -r requirements.txt

## Configuración

Copiar .env.example a .env o configurar config/config.py.

## Definir:
BASE_URL → URL base de la API
LOGIN_ENDPOINT → endpoint de login
AIRCRAFTS_ENDPOINT → endpoint de aeronaves

## Ejecución de tests
- Ejecutar todos los tests: pytest

## Generar reporte HTML: pytest --html=report.html --self-contained-html


## Ejecutar tests específicos:

- pytest tests/test_aircrafts.py
- pytest tests/test_login_contract.py

## Observaciones importantes

- Algunos tests pueden ser intermitentes (flaky) por capacidad baja (<5) o errores del backend.

- test_create_aircraft_from_csv valida cada fila del CSV y puede ser saltado con pytest.skip si no cumple condiciones.

- Se recomienda revisar los logs (log_finding) para hallazgos detallados.

- Las respuestas de la API pueden diferir del contrato; estos casos se documentan como hallazgos.

## Estructura del proyecto
project_root/
│
├─ src/
│  ├─ api/              # Clases y funciones para interactuar con la API
│  ├─ schemas/          # Esquemas JSON para validar respuestas
│  └─ helpers/          # Funciones auxiliares, utils y logging
│
├─ tests/
│  ├─ test_aircrafts.py
│  └─ test_login_contract.py
│
├─ data/
│  └─ aircrafts.csv
├─ requirements.txt
├─ README.md
└─ pytest.ini

## CSV de pruebas de aeronaves
El CSV se encuentra en data/aircrafts.csv con la siguiente estructura:

tail_number	model	capacity
ABC123	Boeing 737	180
XYZ789	Airbus A320	150
N5555	Cessna 172	4
SHORT	Invalid Model	100
LONGTAILNUMBEREXCEEDS	Another Model	200

Nota: La API puede saltar o fallar en filas con capacidad <5 o tail_number demasiado largo (>10).

## Resultados y Hallazgos
Cada vez que se ejecutan los tests, se recomienda generar un reporte HTML:

bash 
pytest --html=report.html --self-contained-html

## Hallazgos comunes

Test	                            Tipo de error	Descripción
test_update_aircraft_success	    Contrato	    Devuelve 200 en vez de 201 al actualizar aeronave.
test_get_aircrafts_pagination	    Backend	        Devuelve 500 Internal Server Error al paginar aeronaves.
test_create_aircraft_from_csv[row2]	Backend	        Capacidad <5 → fila saltada o falla con 500.
test_create_aircraft_from_csv[row4]	Validación	tail_number > 10 caracteres → falla con 422.
test_login_incorrect_credentials	Contrato	    Devuelve 401 en vez de 422 para credenciales incorrectas.

## Resumen de Ejecuciones de Tests

Se realizaron múltiples ejecuciones de los tests automatizados con `pytest`.  
Algunos tests presentan resultados intermitentes (flaky), especialmente los relacionados con datos de aeronaves de capacidad muy baja o `tail_number` inválidos.

Test                                     Resultado típico                   Observaciones
| `test_update_aircraft_success`         | Fallido (200 != 201)             | Devuelve `200` al actualizar, contrato espera `201`. |
| `test_get_aircrafts_pagination`        | Fallido (500 != 200)             | Internal Server Error al paginar, ocurre en varias ejecuciones. |
| `test_create_aircraft_from_csv[row0]`  | Fallido (500 != 201)             | Boeing 737, capacidad 180 → backend falla intermitente. |
| `test_create_aircraft_from_csv[row2]`  | Fallido (500 != 201) o Saltado   | Cessna 172, capacidad 4 → pytest.skip o falla según corrida. |
| `test_create_aircraft_from_csv[row4]`  | Fallido (422 != 201)             | Tail_number >10 caracteres → fallo por validación. |
| `test_login_incorrect_credentials`     | Fallido (401 != 422)             | API devuelve `401` en vez de `422` como indica contrato. |
| Otros tests                            | Pasados                          | Cumplen contrato y validación de datos. |

### Resumen de métricas (aproximadas)

- Total tests: 16  
- Pasados: 10  
- Fallidos: 6  
- Saltados: 1 (fila con capacidad <5)  

### Recomendaciones

1. Revisar backend para errores `500` y resultados inconsistentes en `create_aircraft`.  
2. Ajustar contrato de login si 401 es la respuesta correcta para credenciales incorrectas.  
3. Para filas CSV con `capacity <5` o `tail_number` inválidos, considerar **pytest.skip** y documentar como caso de prueba especial.  
4. Generar reporte HTML después de cada ejecución para registrar hallazgos visualmente:

pytest --html=report.html --self-contained-html
