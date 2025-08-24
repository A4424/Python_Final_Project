

## Autor
Adriana L. Loretán

#  Python API Automation - Pruebas de Registro

## Descripción
Este proyecto de pruebas automatizadas, desarrollado con **Pytest** y la librería **Requests**, valida el comportamiento del *endpoint* de registro de usuarios (`/auth/signup`) de una API de aerolíneas. El objetivo es asegurar que la API funcione correctamente tanto con datos válidos como con errores esperados.

## Requisitos
Asegúrate de tener instalado **Python 3.8 o superior**. Para gestionar las dependencias del proyecto, se recomienda usar un entorno virtual.

##  Configuración y Ejecución de los Tests
Para empezar a trabajar con el proyecto, sigue estos pasos:

1.  **Clona el repositorio**:
    Navega a la carpeta de tu proyecto y clona el repositorio desde tu terminal:
    ```bash
    git clone [https://docs.github.com/es/get-started/using-git/getting-changes-from-a-remote-repository](https://docs.github.com/es/get-started/using-git/getting-changes-from-a-remote-repository)
    cd Python_Final_Project
    ```
    *(Nota: Reemplaza `https://docs.github.com/es/get-started/using-git/getting-changes-from-a-remote-repository` con la URL real de tu proyecto).*

2.  **Configura el entorno virtual en PyCharm**:
    -   Abre el proyecto en PyCharm.
    -   Ve a `File` -> `Settings` -> `Project: [Tu Proyecto]` -> `Python Interpreter`.
    -   Haz clic en el ícono de `Engranaje` -> `Add...`.
    -   Selecciona `Virtualenv Environment` y asegúrate de que la opción `New environment` esté seleccionada. PyCharm creará automáticamente un entorno virtual y lo configurará.

3.  **Instala las dependencias**:
    Abre la terminal de PyCharm (abajo en la ventana, en la pestaña `Terminal`) y ejecuta el siguiente comando para instalar las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecuta los tests**:
    Para ejecutar la suite de pruebas completa, abre la terminal de PyCharm y usa el siguiente comando. PyCharm reconocerá automáticamente el comando de Pytest.
    ```bash
    pytest tests/auth/test_signup.py
    ```

## Casos de Prueba
El archivo `tests/auth/test_signup.py` incluye tres casos clave que se ejecutan:

-   **Caso Positivo: Registro Exitoso** ✅
    Verifica que se pueda registrar un nuevo usuario con datos válidos, esperando una respuesta `201 Created`.

-   **Caso Negativo: Usuario Existente** ❌
    Prueba el manejo de errores al intentar registrar un usuario con un email que ya existe, esperando una respuesta `400 Bad Request`.

-   **Caso Negativo: Email Inválido** ❌
    Verifica que la API rechace una solicitud con un formato de email incorrecto, esperando una respuesta `422 Unprocessable Entity`.

## Estructura del Proyecto
.
├── config/
│   └── config.py          # Constantes y URLs
├── src/
│   └── api/
│       └── signup_api.py  # Lógica de la API para las peticiones
├── tests/
│   └── auth/
│       └── test_signup.py # Casos de prueba
├── venv/                  # Entorno virtual de Python
├── pytest.ini             # Configuración de Pytest
├── README.md              # Este documento
└── requirements.txt       # Dependencias del proyecto