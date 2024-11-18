# E-commerce API

## Introduction
Django-powered API provides a backend for an e-commerce platform, enabling users to manage products, orders, and user accounts.

## Key Features

* **User Management:** Handles user registration, authentication, and profile management.
* **Product Management:** Enables the creation, editing, and deletion of products.
* **Order Management:** Processes orders, tracks their status, and handles payments.
* **Authentication and Authorization:** Implements secure authentication

## User Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| POST | `/register/` | Registers a new user | None |
| GET | `/userinfo/` | Retrieves user information | None |
| PUT | `/userinfo/edit/` | Edits user information | Required |
| POST | `/forgot_password/` | Initiates password reset | Required |
| POST | `/reset_password/<str:token>` | Resets password using token | Required |

### Product Endpoints

| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/products/` | Retrieves a list of all products | None |
| GET | `/products/<str:pk>` | Retrieves a specific product | None |
| POST | `/products/add/` | Adds a new product | Required |
| PUT | `/products/edit/<str:pk>` | Edits an existing product | Required |
| DELETE | `/products/delete/<str:pk>` | Deletes a product | Required |

## Order Endpoints
| Method | Endpoint | Description | Authentication |
|---|---|---|---|
| GET | `/orders/` | Retrieves a list of all orders | Required |
| POST | `/orders/new/` | Creates a new order | Required |
| GET | `/orders/<str:pk>/` | Retrieves a specific order | Required |
| DELETE | `/orders/delete/<str:pk>/` | Deletes an order | Required |
| PUT | `/orders/edit/<str:pk>/` | Edits the status of an order | Required |

## Authentication:

* **JWT-based Authentication:** Implement JWT-based authentication to protect sensitive endpoints.
* **User Roles:** Define different user roles (e.g., admin, customer) and assign appropriate permissions.

## Security Considerations:

* **Input Validation:** Validate user input to prevent malicious attacks like SQL injection.
* **Data Encryption:** Encrypt sensitive data like passwords.
