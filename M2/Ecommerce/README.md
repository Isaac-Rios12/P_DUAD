Ecommerce
Proyecto de Flask con autenticación JWT, PostgreSQL y Redis.
Requisitos previos
Necesitas tener instalado en tu computadora:

Python 3.x
PostgreSQL (corriendo localmente)
Redis (corriendo localmente)
OpenSSL

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