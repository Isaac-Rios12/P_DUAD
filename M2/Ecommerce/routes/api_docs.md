# User API Documentation

Base URL: `http://localhost:5000`

## Authentication

Most endpoints require a JWT token. Add it to your request headers:
```
Authorization: Bearer YOUR_TOKEN_HERE
```

---

## 1. Register User

**POST** `/user/register`

Creates a new user account and returns a JWT token.

**Request Body:**
```json
{
  "fullname": "John Doe",
  "nickname": "johndoe",
  "email": "john@example.com",
  "password": "mypassword123"
}
```

**Notes:** 
- All fields are required
- The user role is automatically set to "user"
- You get a token right away, so no need to login after registering

---

## 2. Login

**POST** `/user/login`

Login with your credentials to get a JWT token.

**Request Body:**
```json
{
  "nickname": "johndoe",
  "password": "mypassword123"
}
```

**Notes:**
- Use this token in the Authorization header for protected routes
- Token doesn't expire (at least not configured in this version)

---

## 3. Get Current User Info

**GET** `/user/me`

Get info about the currently logged in user.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Notes:**
- Requires authentication
- Simple endpoint to check if your token is valid

---

## 4. Update User

**PATCH** `/user/update`

Update your email and password.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "password": "newpassword123"
}
```

**Notes:**
- You can only update your own account
- Both email and password are required
- Your old token will still work after updating

---

## 5. Get User by ID (Admin Only)

**GET** `/user/<user_id>`

Get any user's information by their ID.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Example:** `GET /user/5`



**Notes:**
- Admin only - regular users can't access this
- Replace `<user_id>` with the actual user ID

---

## 6. Get All Users (Admin Only)

**GET** `/user/all-users`

Get a list of all registered users.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Notes:**
- Admin only endpoint
- Returns all users in the database

---



# Role API Documentation

Base URL: `http://localhost:5000`

All role endpoints require admin authentication.

---

## 1. Create Role

**POST** `/role/add`

Create a new role in the system.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request Body:**
```json
{
  "name": "moderator"
}
```

**Notes:**
- Admin only
- Role names should be unique

---

## 2. Get All Roles

**GET** `/role/all-roles`

Get a list of all available roles.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Notes:**
- Admin only
- Returns all roles in the system

---

## 3. Get Role by Name

**GET** `/role/<name>`

Get role details by its name.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Example:** `GET /role/admin`

**Notes:**
- Admin only
- Replace `<name>` with the actual role name (like "user", "admin", etc)

---

## 4. Update Role

**PUT** `/role/<role_id>`

Update an existing role's name.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request Body:**
```json
{
  "new_name": "super_moderator"
}
```

**Example:** `PUT /role/3`

**Notes:**
- Admin only
- Replace `<role_id>` with the actual role ID
- Only the name can be updated

---

## 5. Delete Role

**DELETE** `/role/<role_id>`

Delete a role from the system.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Example:** `DELETE /role/3`

**Notes:**
- Admin only
- Be careful, this might affect users assigned to this role
- Replace `<role_id>` with the actual role ID




# Product API Documentation

Base URL: `http://localhost:5000`

---

## 1. Get All Products

**GET** `/product/all-products`

Get a list of all products in the store.

**Notes:**
- No authentication required
- Results are cached for 5 minutes

---

## 2. Get Product by ID

**GET** `/product/<product_id>`

Get details of a specific product.

**Example:** `GET /product/5`

**Notes:**
- No authentication required
- Replace `<product_id>` with the actual product ID
- Results are cached for 5 minutes

---

## 3. Search Products by Name

**GET** `/product/?name=<product_name>`

Search for products by name.

**Example:** `GET /product/?name=laptop`

**Notes:**
- No authentication required
- Results are cached for 2 minutes
- Returns products that match the search term

---

## 4. Register Product

**POST** `/product/register`

Create a new product (Admin only).

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request Body:**
```json
{
  "name": "Gaming Laptop",
  "description": "High performance laptop for gaming",
  "price": 1299.99,
  "stock": 15
}
```

**Notes:**
- Admin only
- All fields are required
- Price and stock must be positive numbers
- Clears product cache after creation

---

## 5. Update Product Price

**PUT** `/product/update-price/<product_id>`

Update the price of an existing product.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Request Body:**
```json
{
  "new_price": 1199.99
}
```

**Example:** `PUT /product/update-price/5`

**Notes:**
- Admin only
- Price must be a positive number
- Clears product cache after update

---

## 6. Delete Product

**DELETE** `/product/delete/<product_id>`

Delete a product from the store.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Example:** `DELETE /product/delete/5`

**Notes:**
- Admin only
- Replace `<product_id>` with the actual product ID
- Clears product cache after deletion



# Cart API Documentation

Base URL: `http://localhost:5000`

All cart endpoints require user authentication.

---

## 1. Get Cart

**GET** `/cart/`

Get your shopping cart with all items.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Notes:**
- If you don't have a cart, it creates one automatically
- Shows all products in your cart with quantities

---

## 2. Add Items to Cart

**POST** `/cart/add-items`

Add one or more products to your cart.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request Body:**
```json
{
  "items": [
    {
      "product_id": 5,
      "quantity": 2
    },
    {
      "product_id": 8,
      "quantity": 1
    }
  ]
}
```

**Notes:**
- Can add multiple products at once
- Checks if enough stock is available
- If product already exists in cart, it adds to existing quantity

---

## 3. Update Item Quantity

**PATCH** `/cart/update-quantity/<product_id>`

Change the quantity of a product in your cart.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request Body:**
```json
{
  "new_quantity": 5
}
```

**Example:** `PATCH /cart/update-quantity/5`

**Notes:**
- Replace `<product_id>` with the actual product ID
- Checks stock availability before updating
- New quantity must be positive

---

## 4. Delete Item from Cart

**DELETE** `/cart/delete-item/<product_id>`

Remove a specific product from your cart.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Example:** `DELETE /cart/delete-item/5`

**Notes:**
- Replace `<product_id>` with the actual product ID
- Removes the product completely regardless of quantity

---

## 5. Delete Entire Cart

**DELETE** `/cart/delete`

Delete your entire cart and all items in it.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Notes:**
- Removes all products from your cart
- The cart itself is deleted
- A new cart will be created on your next add operation


# Sale API Documentation

Base URL: `http://localhost:5000`

---

## User Endpoints

## 1. Create Sale

**POST** `/sale/new-sale`

Create a new sale from your current cart.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Request Body:**
```json
{
  "billing_address": "123 Main St, City, Country"
}
```

**Notes:**
- Uses all items from your current cart
- Cart is cleared after sale is created
- Billing address is required
- Stock is automatically updated

---

## 2. Get My Sales

**GET** `/sale/my-sales`

Get all your purchase history.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Notes:**
- Shows all your past purchases
- Includes details of products and quantities

---

## 3. Get Specific Sale

**GET** `/sale/my-sales/<sale_id>`

Get details of a specific purchase.

**Headers:**
```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Example:** `GET /sale/my-sales/15`

**Notes:**
- You can only view your own sales
- Replace `<sale_id>` with the actual sale ID

---

## Admin Endpoints

## 4. Get Sale by ID (Admin)

**GET** `/sale/admin/<sale_id>`

Get details of any sale (Admin only).

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Example:** `GET /sale/admin/15`

**Notes:**
- Admin only
- Can view any user's sale
- Results are cached for 5 minutes

---

## 5. Get All Sales (Admin)

**GET** `/sale/admin/all-sales`

Get a list of all sales in the system.

**Headers:**
```
Authorization: Bearer ADMIN_TOKEN_HERE
```

**Notes:**
- Admin only
- Shows all sales from all users
- Results are cached for 1 minute