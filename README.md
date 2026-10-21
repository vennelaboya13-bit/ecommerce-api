# E-commerce REST API

A beginner-friendly E-commerce REST API built using Python, FastAPI, and MySQL.

## Technologies Used
- Python
- FastAPI
- MySQL
- SQLAlchemy
- Pydantic
- Swagger UI

## Features
- User Registration and Login
- Product Create, Read, Update, and Delete
- Shopping Cart Management
- Order Placement
- Automatic Product Stock Update
- MySQL Database Integration

## Setup
1. Install Python and MySQL.
2. Install dependencies:

   `pip install -r requirements.txt`

3. Create a MySQL database named `ecommerce_db`.
4. Create a `.env` file with your local database settings.
5. Run the application:

   `python -m uvicorn app.main:app --reload`

6. Open Swagger UI at `http://127.0.0.1:8000/docs`.

## Note
Do not upload your `.env` file or database passwords to GitHub.
