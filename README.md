## Autor
Adriana L. Loretán

## Sistema de Pruebas Automatizadas de API CRUD para un Catálogo de Aeronaves
Este proyecto consiste en un sistema automatizado de pruebas para validar la funcionalidad de una API que gestiona un catálogo de aeronaves. Su objetivo es asegurar que las operaciones de creación, lectura, actualización y eliminación (CRUD) de datos de aeronaves se realicen correctamente, cumpliendo con el contrato definido por la API y garantizando la integridad de los datos.
El sistema permite ejecutar pruebas de forma automática, generar reportes en HTML y mantener la calidad del software mediante integración continua con GitHub Actions, de modo que cualquier cambio en el código sea verificado inmediatamente sin depender de pruebas manuales.
Objetivo General
Validar de forma automática la funcionalidad y la integridad de las operaciones de creación, lectura, actualización y eliminación de datos de aeronaves a través de la API, asegurando que el sistema se comporte según el contrato y que los datos se gestionen de manera correcta y segura.

## Objetivos Específicos

- Elaborar un conjunto de pruebas automatizadas que valide cada uno de los endpoints de la API, asegurando que su comportamiento y las respuestas HTTP se ajusten al contrato de la especificación técnica.


- Implementar la verificación del esquema de datos en las respuestas de la API para garantizar que la estructura, los tipos de datos y los campos obligatorios cumplan con el contrato definido.


- Crear fixtures de pruebas para simular diferentes estados del sistema, lo que permitirá confirmar que el flujo de autenticación y las operaciones CRUD mantengan la coherencia con el contrato de la API, incluso en escenarios de borde.


- Integrar el sistema de pruebas en un proceso de integración continua (CI) para que se ejecuten automáticamente y se notifiquen las fallas, garantizando que cualquier cambio en la base de código no rompa el contrato de la API.


## Ejecución Rápida del Proyecto: Clonar y Revisar sin Instalación Local
- Revisión compartida: clonar, ejecutar y revisar el proyecto.
El ejemplar de revisión está alojado en un repositorio de GitHub.
Enlace al repositorio y la rama específica: 

Repositorio: https://github.com/A4424/Python_Final_Project
Rama: airline-api-test-v7

- Cómo clonar la rama

 git clone -b airline-api-test-v7 https://github.com/A4424/Python_Final_Project.git

- Ejecutar el flujo de integración continua

El workflow de GitHub Actions (.github/workflows/ci.yml) se ejecuta automáticamente con cada push o pull request a la rama.
Genera reportes HTML y logs que también estarán disponibles como artefactos descargables desde la sección “Actions” del repositorio.

- Variables de entorno

Para seguridad, las credenciales de la API no se incluyen directamente en el código.
Se cargan mediante .env local o mediante Secrets de GitHub.
Esto permite  ejecutar las pruebas sin exponer información sensible.


## Instrucciones de Instalación Local del Repositorio

- Estructura del Proyecto
├── .github/
│   └── workflows/
│       └── ci.yml              # Workflow de GitHub Actions (CI/CD)
│
├── src/
│   └── api/
│       └── aircrafts_api.py    # Cliente para interactuar con la API de aeronaves
│
├── tests/
│   ├── aircrafts/
│   │   └── test_aircrafts.py   # Pruebas CRUD de aeronaves
│   ├── data/
│   │   └── aircrafts.csv       # Datos parametrizados para pruebas
│   ├── reports/
│   │   └── report.html         # Reporte HTML generado automáticamente
│   ├── logs/
│   │   └── test.log            # Log de ejecución
│   ├── test_login.py           # Pruebas de login (errores)
│   └── test_login_flow.py      # Flujo de login completo con token
│
├── .env.example                # Ejemplo de configuración local de credenciales
├── pytest.ini                  # Configuración de pytest (marcadores, opciones)
├── requirements.txt            # Dependencias del proyecto
└── README.md                   # Documentación del proyecto


- Requisitos Previos

1. Python
   - Versión recomendada: Python 3.12.4
   - Comprobar versión instalada:   python --version
   - Instalar pip (gestor de paquetes de Python)

2. Dependencias principales
   - Las librerías necesarias para correr los tests se encuentran en requirements.txt.    

    Se incluyen:
     - pytest (8.4.1) – framework de pruebas
     - pytest-html (4.1.1) – generación de reportes HTML
     - requests (2.32.5) – para realizar llamadas HTTP a la API
     - python-dotenv (1.1.1) – para cargar variables de entorno desde .env

   - Instalar dependencias:     pip install -r requirements.txt (todas las dependencias están en requirements.txt, instalarlarlas  desde ese fichero colabora a que los tests funcionen correctamente)
     

3. Entorno virtual recomendado
   - Se sugiere crear un entorno virtual para aislar las dependencias del proyecto:

     python -m venv venv
    
     source venv/bin/activate  # Linux / macOS
     venv\Scripts\activate     # Windows
     

4. Archivo de variables de entorno
   - Crear un archivo .env en la raíz del proyecto con las credenciales necesarias para la API:

     ADMIN_USER="admin@demo.com"
     ADMIN_PASSWORD="admin123"
     

5. Contar con una cuenta en GitHub (para ejecutar el flujo CI/CD con GitHub Actions): 
     - Subir el proyecto al repositorio remoto.
     - Ejecutar el flujo de Integración Continua (CI) mediante GitHub Actions.
     - Gestionar secrets y credenciales de la API de forma segura.
     - GitHub Actions se activará automáticamente con cada push o pull request a las ramas configuradas (main y airline-api-test-v7), ejecutando los tests y generando reportes HTML.
   - Repositorio: https://github.com/A4424/Python_Final_Project
     
      Rama: airline-api-test-v7
      Clonar rama: git clone -b airline-api-test-v7 https://github.com/A4424/Python_Final_Project.git



- Instalación y Configuración Local / Clonar el repositorio

  git clone https://github.com/A4424/Python_Final_Project.git
  cd Python_Final_Project
  Rama a clonar: airline-api-test-v7

  Ejemplo: git clone -b airline-api-test-v7 https://github.com/A4424/Python_Final_Project.git
cd Python_Final_Project

- Crear y activar entorno virtual (opcional pero recomendado)

 python -m venv
 source venv/bin/activate   # Linux/Mac
 venv\Scripts\activate      # Windows

- Instalar dependencias
 pip install --upgrade pip
 pip install -r requirements.txt

-Configurar variables de entorno
 Copiar el archivo  .env.

- Editar el archivo con las credenciales correspondientes:
             ADMIN_USER="admin@demo.com"
             ADMIN_PASSWORD="admin123"
IMPORTANTE: Los secrets configurados en GitHub reemplazan las credenciales locales del .env durante la ejecución del workflow.
## Ejecución de las Pruebas
- Ejecutar todas las pruebas
  pytest -v
- Generar reporte HTML
  pytest -v --html=tests/reports/report.html --self-contained-html
- Ejecutar pruebas por marcador
  pytest -m create    # Solo pruebas de creación
  pytest -m error     # Solo pruebas de error

## Integración Continua (CI/CD con GitHub Actions)
El workflow definido en .github/workflows/ci.yml se ejecuta automáticamente en cada push o pull request hacia las ramas main o airline-api-test-v7.

El pipeline realiza las siguientes tareas:
 - Instala dependencias.
 - Ejecuta las pruebas con Pytest.
 - Genera reportes en HTML y logs.
 - Publica los reportes como artefactos descargables desde GitHub Actions.

- Para configurar las credenciales necesarias en GitHub:
  Ir a Settings > Secrets and variables > Actions.

- Crear los secrets:
     ADMIN_USER
     ADMIN_PASSWORD



