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

Para ver la documentación completa de las rutas y ejemplos de uso, revisa [API_DOCS.md](routes/api_docs.md)

## Main dependencies

- **Flask 3.1.1** - Web framework
- **SQLAlchemy 2.0.41** - Database ORM
- **psycopg2-binary 2.9.10** - PostgreSQL adapter
- **redis 6.4.0** - Redis client
- **PyJWT 2.10.1** - JWT token handling
- **python-dotenv 1.1.1** - Environment variables loader
- **bcrypt 4.3.0** - Password encryption
- **pytest 8.4.1** - Testing framework