Task Management REST API
📌 Overview

The Task Management REST API is a backend application built using Flask that allows users to securely manage tasks.
It provides JWT-based authentication and supports creating, updating, deleting, and retrieving tasks with filtering, sorting, and pagination.

🌐 Base URL
http://localhost:5000/api

🔐 Authentication

This API uses JWT (JSON Web Tokens) for authentication.

All protected endpoints require the following HTTP header:

Authorization: Bearer <ACCESS_TOKEN>


The access token is obtained after successful login.

🔑 Endpoints
🔹 Authentication

POST /auth/register – Register a new user

POST /auth/login – Login and receive JWT token

🔹 Tasks

GET /tasks – Get all tasks (supports pagination, filtering, sorting)

POST /tasks – Create a new task

GET /tasks/{id} – Get a task by ID

PUT /tasks/{id} – Update a task

DELETE /tasks/{id} – Delete a task

🔹 Users

GET /users/me – Get the current logged-in user profile

🚨 Error Handling

The API returns standard HTTP status codes:

400 – Validation error

401 – Unauthorized or invalid token

404 – Resource not found

500 – Internal server error

All error responses are returned in JSON format.

🔒 Security Features

JWT authentication

Password hashing

Protected API routes

Input validation

Proper HTTP status codes

🧪 Testing

Unit tests written using pytest

Authentication, task, and user endpoints tested

In-memory database used for testing

🏁 Conclusion

This Task Management REST API follows REST principles and demonstrates secure backend development using Flask.
It is scalable, well-documented, and suitable for real-world applications and portfolio submissions.