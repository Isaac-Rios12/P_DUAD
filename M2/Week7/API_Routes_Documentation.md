
# 📘 API Routes Documentation

Este documento describe las rutas disponibles en tu aplicación Flask, organizadas por tipo de recurso.

---

### 🧑‍💻 Rutas de usuarios (`/users`)

| Método | Endpoint               | Descripción                          |
|--------|------------------------|--------------------------------------|
| POST   | `/users/register`      | Registrar un nuevo usuario (admin)   |-------------
| POST   | `/users/login`         | Iniciar sesión y obtener token       |
| GET    | `/users/me`            | Obtener información del usuario autenticado |

Ejemplo para registrar un nuevo usuario(`/users/register`)
    {
        "username": "luquita",
        "password": "luquita123",
        "role": "user"
    }

ejemplo para hacer un login(`/users/login`)
    {
        "username": "luquita",
        "password": "luquita123"
    }
---

### 📦 Rutas de productos (`/products`)

| Método | Endpoint               | Descripción                          |
|--------|------------------------|--------------------------------------|
| GET    | `/products/`           | Obtener todos los productos          |
| POST   | `/products/register`   | Crear un nuevo producto (admin)      |
| GET    | `/products/<id>`       | Obtener un producto por ID (admin)   |
| PUT    | `/products/<id>`       | Actualizar un producto (admin)       |
| DELETE | `/products/<id>`       | Eliminar un producto (admin)         |

Ejemplo para registrar un producto(`/products/register` )
    {
        "name": "fresa",
        "price": 100,
        "quantity": 200
    }

Ejemplo para hacer actualizacion de producto(`/products/<id>`)
    {
            "name": "uva",
            "price": 500.00,
            "quantity": 100
    }


---

### 🧾 Rutas de compras (`/purchases`)

| Método | Endpoint                   | Descripción                             |
|--------|----------------------------|-----------------------------------------|
| POST   | `/purchases/`              | Realizar una compra                     |
| GET    | `/purchases/my-purchases`  | Obtener compras del usuario autenticado |
| GET    | `/purchases/user/<id>`     | Obtener compras por usuario (admin)     |


Lista ejemplo para realizar una compra(`/purchases/` )
    [
        {"product_id": 4, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ]

---

🛡️ **Nota:** Algunas rutas requieren autenticación y permisos de administrador.
