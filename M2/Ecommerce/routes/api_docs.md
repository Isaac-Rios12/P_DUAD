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
