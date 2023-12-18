Sure, I'll help you structure a README based on the information you provided. Please note that I'll format it as plain text. You can then use Markdown or any other formatting tool when you copy it into your GitHub repository. Here's a basic structure:

```plaintext
# Little Lemon Restaurant API

API project for the Little Lemon restaurant, designed for client application developers to build web and mobile applications. This API enables users with different roles to browse, add and edit menu items, place orders, browse orders, assign delivery crew to orders, and deliver orders.

## Installation

```bash
cd LittleLemon
pipenv shell
pipenv install
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## API Endpoints

### User Registration and Token Generation

- **POST /api/users**
  - Role: No role required
  - Purpose: Creates a new user with name, email, and password.

- **GET /api/users/users/me/**
  - Role: Anyone with a valid user token
  - Purpose: Displays only the current user.

- **POST /token/login/**
  - Role: Anyone with a valid username and password
  - Purpose: Generates access tokens for other API calls in this project.

### Menu Items

- **GET /api/menu-items**
  - Role: Customer, delivery crew
  - Purpose: Lists all menu items.

- **POST, PUT, PATCH, DELETE /api/menu-items**
  - Role: Customer, delivery crew
  - Purpose: Denies access and returns 403 – Unauthorized HTTP status code.

- **GET /api/menu-items/{menuItem}**
  - Role: Customer, delivery crew
  - Purpose: Lists a single menu item.

- **GET /api/menu-items**
  - Role: Manager
  - Purpose: Lists all menu items.

- **POST /api/menu-items**
  - Role: Manager
  - Purpose: Creates a new menu item.

- **GET /api/menu-items/{menuItem}**
  - Role: Manager
  - Purpose: Lists a single menu item.

- **PUT, PATCH /api/menu-items/{menuItem}**
  - Role: Manager
  - Purpose: Updates a single menu item.

- **DELETE /api/menu-items/{menuItem}**
  - Role: Manager
  - Purpose: Deletes a menu item.

### User Group Management

- **GET /api/groups/manager/users**
  - Role: Manager
  - Purpose: Returns all managers.

- **POST /api/groups/manager/users**
  - Role: Manager
  - Purpose: Assigns the user in the payload to the manager group.

- **DELETE /api/groups/manager/users/{userId}**
  - Role: Manager
  - Purpose: Removes a user from the manager group.

- **GET /api/groups/delivery-crew/users**
  - Role: Manager
  - Purpose: Returns all delivery crew.

- **POST /api/groups/delivery-crew/users**
  - Role: Manager
  - Purpose: Assigns the user in the payload to the delivery crew group.

- **DELETE /api/groups/delivery-crew/users/{userId}**
  - Role: Manager
  - Purpose: Removes a user from the delivery crew group.

### Cart Management

- **GET /api/cart/menu-items**
  - Role: Customer
  - Purpose: Returns current items in the cart for the current user token.

- **POST /api/cart/menu-items**
  - Role: Customer
  - Purpose: Adds a menu item to the cart.

- **DELETE /api/cart/menu-items**
  - Role: Customer
  - Purpose: Deletes all menu items created by the current user token.

### Order Management

- **GET /api/orders**
  - Role: Customer
  - Purpose: Returns all orders with order items created by this user.

- **POST /api/orders**
  - Role: Customer
  - Purpose: Creates a new order item for the current user.

- **GET /api/orders/{orderId}**
  - Role: Customer
  - Purpose: Returns all items for this order id.

- **GET /api/orders**
  - Role: Manager
  - Purpose: Returns all orders with order items by all users.

- **PUT, PATCH /api/orders/{orderId}**
  - Role: Customer
  - Purpose: Updates the order.

- **DELETE /api/orders/{orderId}**
  - Role: Manager
  - Purpose: Deletes an order.

- **GET /api/orders**
  - Role: Delivery crew
  - Purpose: Returns all orders with order items assigned to the delivery crew.

- **PATCH /api/orders/{orderId}**
  - Role: Delivery crew
  - Purpose: Updates the order status.

### Notes

- You can use Djoser for user registration and token generation.
- Refer to the [Introduction to Djoser library for better authentication video](#) for additional endpoints.

```

Feel free to adjust the formatting, add more details, or modify it according to your needs.
