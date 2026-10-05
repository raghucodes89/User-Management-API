# Secure User Management API

A backend API for managing users, authentication, and role-based access control using FastAPI and MongoDB.

## Tech Stack

- Python
- FastAPI
- MongoDB
- PyMongo
- JWT
- Passlib / Bcrypt
- Pydantic
- Uvicorn

## Main Features

- User registration
- User login
- Password hashing
- JWT authentication
- Role-based authorization
- Admin, Manager, and Employee roles
- Get all users
- Get user by ID
- Update user
- Delete user
- Duplicate email protection
- Invalid user ID handling
- Role-change protection

## Project Structure

```text
User-Management-API/
│
├── Backend/
│   ├── main.py
│   ├── requirement.txt
│   ├── .env
│   ├── .gitignore
│   │
│   ├── database/
│   │   └── database.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── routers/
│   │   └── user.py
│   ├── services/
│   │   └── user_service.py
│   └── utils/
│       └── security.py
│
└── README.md

How to Run
Clone the repository:
git clone https://github.com/raghucodes89/User-Management-API.git

Go to the Backend folder:
cd User-Management-API/Backend

Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate

Install dependencies:
pip install -r requirement.txt

Create a .env file:
MONGO_URL=mongodb://localhost:27017/User-Management
SECRET_KEY=your-long-random-secret-key

Run the application:
python -m uvicorn main:app --reload

API Documentation
After starting the server, open:
http://127.0.0.1:8000/docs

FastAPI Swagger UI can be used to test all API endpoints.


Basic Security
- Passwords are stored using hashing.
- JWT is used for authentication.
- Role-based authorization protects restricted endpoints.
- JWT secret is stored in .env.
- Duplicate email registration is prevented.
- Only Admin can delete users.
- Only Admin can change user roles.
- Passwords are not returned in user responses.


Project Status
Completed and tested.

Implemented:
- User CRUD
- MongoDB integration
- JWT authentication
- Password hashing
- Role-based authorization
- Error handling
- Security controls
- API testing