=-0=-0-# Ecommerce

Flask project with JWT authentication, postgreSQL and Redis.

## Prerequisites

You need to have installed on your computer:

- Python 3.x
- PostgreSQL 
- Redis 
- OpenSSL
 

## Instalation and Setup

### 1. Clone the repository

First clone the repository and navigate to the project folder:

```bash
git clone <repo-url>
cd Ecommerce
```

### 2. Install dependencies

Install all necessary libraries from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Create keys folder

Create a folder named `keys` inside the `auth` folder. If tne `auth`
folder already exists, just create `keys` inside it. If either
exists, create both.

The structure should look like this:

```
Ecommercer/
  auth/
    keys/
```

### 4. Generate RSA keys for JWT

Now you need to generate two keys (one private and one public) to handle JWT tokens.

```bash
openssl rsa -pubout -in auth/keys/private.pem -out auth/keys/public.pem
```

Ths will create two files: `private.pem` and `public.pem` inside
`auth/keys/`.

### 5. Configure environment variables

The project includes an example file called `.env.example` that shows wich variables you need to configure.

Copy that file and rename it to `.env`:

Now opne the `.env` file and edit the existing variables with your configuration.


### 6. Create database

Make sure PostgreSQL is running and create the necessary databases:

- One databse for the project
- One database for testing

You can create them from the PostgreSQL line or using a graphical tool like pdAdmin.

### 7. Run the application

Once everything is configured, run the `main.py` file:

```bash
python main.py
```

if everything went well, the application will be running at `http://localhost:5000`


## Running tests 
To run the project tests. execute:

```bash
python run_tests.py
```

This file is at the root of the project and runs all tests automatically.


## Documentación de APIs

Para ver la documentación completa de las rutas y ejemplos de uso, revisa [API_DOCS.md](routes/docs_apis.md)

## Main dependencies

- **Flask 3.1.1** - Web framework
- **SQLAlchemy 2.0.41** - Database ORM
- **psycopg2-binary 2.9.10** - PostgreSQL adapter
- **redis 6.4.0** - Redis client
- **PyJWT 2.10.1** - JWT token handling
- **python-dotenv 1.1.1** - Environment variables loader
- **bcrypt 4.3.0** - Password encryption
- **pytest 8.4.1** - Testing framework































Instalación y configuración
1. Clonar el repositorio
Primero clona el repositorio y entra a la carpeta del proyecto:
git clone <url-del-repo>
cd Ecommerce
2. Instalar dependencias
Instala todas las librerías necesarias que están en el archivo requirements.txt:
pip install -r requirements.txt
3. Crear carpeta para las llaves
Crea una carpeta llamada keys dentro de la carpeta auth. Si ya existe la carpeta auth, solo crea keys adentro. Si no existe ninguna, crea ambas.
La estructura debería verse así:
Ecommerce/
  auth/
    keys/

4. Generar llaves RSA para JWT
Ahora necesitas generar dos llaves (una privada y una pública) para manejar los tokens JWT.
Genera la llave privada:
openssl genpkey -algorithm RSA -out auth/keys/private.pem -pkeyopt rsa_keygen_bits:2048
Genera la llave pública:
openssl rsa -pubout -in auth/keys/private.pem -out auth/keys/public.pem
Esto va a crear dos archivos: private.pem y public.pem dentro de auth/keys/.

5. Configurar variables de entorno
El proyecto incluye un archivo de ejemplo llamado env.example que muestra qué variables necesitas configurar.
Copia ese archivo y renómbralo a .env:
cp env.example .env
Ahora abre el archivo .env y edita las siguientes variables con tu configuración:
Configuración de PostgreSQL:
DATABASE_URL=postgresql+psycopg2://tu_usuario:tu_contraseña@localhost:5432/nombre_bd
Configuración de Redis:
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=tu_contraseña_redis
Base de datos para testing:
DATABASE_URL_TEST=postgresql+psycopg2://tu_usuario:tu_contraseña@localhost:5432/nombre_bd_test
Cambia tu_usuario, tu_contraseña, nombre_bd, etc. por tus valores reales.

6. Crear base de datos
Asegúrate de que PostgreSQL esté corriendo y crea las bases de datos necesarias:

Una base de datos para el proyecto
Una base de datos para los tests

Puedes crearlas desde la línea de comandos de PostgreSQL o usando alguna herramienta gráfica como pgAdmin.
7. Correr la aplicación
Una vez todo configurado, ejecuta el archivo main.py:
python main.py
Si todo salió bien, la aplicación estará corriendo en http://localhost:5000
Ejecutar los tests
Para correr las pruebas del proyecto, ejecuta:
python run_tests.py
Este archivo está en la raíz del proyecto y corre todos los tests automáticamente.
Dependencias principales

Flask 3.1.1 - Framework web
SQLAlchemy 2.0.41 - ORM para base de datos
psycopg2-binary 2.9.10 - Adaptador PostgreSQL
redis 6.4.0 - Cliente Redis
PyJWT 2.10.1 - Manejo de tokens JWT
python-dotenv 1.1.1 - Carga de variables de entorno
bcrypt 4.3.0 - Encriptación de contraseñas
pytest 8.4.1 - Framework de testing