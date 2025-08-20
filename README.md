# Python_Final_Project
Este repositorio contiene un framework de automatización de pruebas para la API de demostración "Airline Demo API". El proyecto utiliza Pytest y la librería Requests para validar las funcionalidades clave de la API, siguiendo una arquitectura modular y escalable.

## Objetivos del Proyecto
El objetivo principal es asegurar la calidad de la API mediante la verificación de sus funcionalidades de:
* **Autenticación (AUTH):** Validar el flujo de login y el uso de tokens.
* **Gestión de Aviones (AIRCRAFTS):** Confirmar que las operaciones CRUD (Crear, Leer, Actualizar, Eliminar) funcionan correctamente y respetan los permisos.

## Estructura del Proyecto
El framework se organiza en la siguiente estructura modular para facilitar la reutilización y el mantenimiento del código:
* `tests/`: Contiene todos los casos de prueba.
* `src/`: Incluye el código fuente del framework, como clases de API y esquemas de validación.
* `data/`: Almacena los datos de prueba separados del código.
* `config/`: Guarda las variables de configuración del proyecto (ej. URLs, credenciales).

## Requisitos de Instalación
Para ejecutar las pruebas, se deben instalar las dependencias de Python necesarias.
1.  Asegúrese de tener un entorno virtual activo.
2.  Ejecute el siguiente comando para instalar las librerías:
    `pip install -r requirements.txt`

## Ejecución de las Pruebas
Las pruebas se ejecutan utilizando Pytest. Se pueden ejecutar todos los tests con el siguiente comando:
`pytest`

Para ejecutar un test específico o un conjunto de tests, se pueden usar las siguientes opciones:
* Ejecutar todos los tests en un archivo:
    `pytest tests/auth/test_auth.py`
* Ejecutar los tests con una marca específica:
    `pytest -m "smoke"`

## Reporte de Pruebas
Se pueden generar reportes de pruebas en formato HTML con la librería pytest-html.
* Instalar la librería:
    `pip install pytest-html`
* Ejecutar los tests y generar el reporte:
    `pytest --html=reporte_pruebas.html`

## Autor
* Adriana L. Loretán