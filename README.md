# Personal Finance Tracker API

A RESTful API built with **FastAPI**, **SQLAlchemy**, and **Pydantic** for managing personal finances. The API allows users to track transactions, set category-based budgets, and monitor spending habits.

## Features

* Create, read, update, and delete transactions
* Create, read, update, and delete budgets
* Filter transactions by type and category
* SQLAlchemy ORM integration
* Pydantic request/response validation
* Automatic interactive API documentation with Swagger UI

## Tech Stack

* FastAPI
* SQLAlchemy
* Pydantic
* SQLite (or any SQLAlchemy-supported database)

## Data Models

### Transactions

* Amount
* Category ID
* Type (Income / Expense)
* Description
* Date

### Budgets

* Category ID
* Budget Amount
* Month

### Categories

* Category Name
* Type (Income / Expense)

## API Endpoints

### Transactions

| Method | Endpoint             | Description                    |
| ------ | -------------------- | ------------------------------ |
| GET    | `/transactions`      | Get all transactions           |
| GET    | `/transactions/{id}` | Get a transaction by ID        |
| POST   | `/transactions`      | Create a transaction           |
| PUT    | `/transactions/{id}` | Replace a transaction          |
| PATCH  | `/transactions/{id}` | Partially update a transaction |
| DELETE | `/transactions/{id}` | Delete a transaction           |

### Budgets

| Method | Endpoint        | Description               |
| ------ | --------------- | ------------------------- |
| GET    | `/budgets`      | Get all budgets           |
| GET    | `/budgets/{id}` | Get a budget by ID        |
| POST   | `/budgets`      | Create a budget           |
| PUT    | `/budgets/{id}` | Replace a budget          |
| PATCH  | `/budgets/{id}` | Partially update a budget |
| DELETE | `/budgets/{id}` | Delete a budget           |

## Running the Project

```bash
pip install -r requirements.txt

uvicorn main:app --reload
```

Visit:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Future Improvements

* User authentication (JWT)
* Monthly summary endpoint
* Category management endpoints
* Dashboard analytics

