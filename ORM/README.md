# Workshop 4 — ORM with FastAPI, SQLAlchemy, and MySQL

This project implements a small order-management REST API using **FastAPI**, **SQLAlchemy ORM**, and **MySQL**.

The main objective is to demonstrate how a Python application can interact with a relational database through an Object-Relational Mapping layer instead of manually writing SQL statements for every operation.

The project includes CRUD operations, ORM relationships, nested inserts and queries, cascade deletion, inventory management, transactions, rollback, and an independent Python client.

---

## Architecture

```text
Python Client / curl
        |
        | HTTP / JSON
        v
     FastAPI
        |
        | SQLAlchemy ORM
        v
      MySQL
```

The application is divided into three main layers:

- **Client layer:** `curl` commands and an independent Python client send HTTP requests.
- **API layer:** FastAPI receives requests, validates data, and exposes REST endpoints.
- **Persistence layer:** SQLAlchemy ORM manages objects, relationships, transactions, and communication with MySQL.

---

## Technologies

- Python 3
- FastAPI
- SQLAlchemy
- MySQL 8
- PyMySQL
- Pydantic
- Uvicorn
- Requests

---

## Project Structure

```text
fastapi-orm-workshop/
│
├── server/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── client/
│   ├── client.py
│   └── data/
│       └── order.json
│
├── sql/
│   └── create_database.sql
│
├── requirements.txt
└── README.md
```

### Main files

- `server/database.py` — Configures the SQLAlchemy engine, session, and connection to MySQL.
- `server/models.py` — Defines the SQLAlchemy ORM models and their relationships.
- `server/schemas.py` — Defines the Pydantic schemas used for request validation and response serialization.
- `server/main.py` — Contains the FastAPI application and all REST endpoints.
- `client/client.py` — Independent Python client that communicates with the API using HTTP and JSON.
- `client/data/order.json` — Example JSON file used to create an Order from the external client.
- `sql/create_database.sql` — Creates the MySQL database and the workshop database user.

---

## Database Model

The application uses four entities:

```text
Customer
   |
   +----< Order
             |
             +----< OrderItem >---- Product
```

### Customer

Represents a customer registered in the system.

Main attributes:

```text
id
name
email
```

Relationship:

```text
Customer 1 ---- N Order
```

### Order

Represents a purchase made by a Customer.

Main attributes:

```text
id
order_date
status
customer_id
```

Relationships:

```text
Order N ---- 1 Customer
Order 1 ---- N OrderItem
```

### Product

Represents a product available for purchase.

Main attributes:

```text
id
name
price
stock
```

Relationship:

```text
Product 1 ---- N OrderItem
```

### OrderItem

Represents one product included in an Order.

Main attributes:

```text
id
quantity
unit_price
order_id
product_id
```

Relationships:

```text
OrderItem N ---- 1 Order
OrderItem N ---- 1 Product
```

---

## ORM Relationships

SQLAlchemy relationships are implemented using:

```python
relationship()
ForeignKey()
back_populates
```

For example:

```python
orders = relationship(
    back_populates="customer",
    cascade="all, delete-orphan"
)
```

The project uses cascade behavior in:

```text
Customer -> Orders
Order -> OrderItems
```

This means that dependent objects can be automatically removed when their parent is deleted.

Products are not deleted when an Order is removed because Products are independent entities that may be referenced by different Orders.

---

## Main Features

- Customer CRUD operations
- Product CRUD operations
- Order creation
- Nested OrderItem creation
- Nested ORM queries
- Customer-to-Order relationships
- Product-to-OrderItem relationships
- Order status updates
- Cascade deletion
- Inventory management
- Database transactions
- Transaction rollback
- Independent Python client
- JSON-file input
- Product purchase history by Customer

---

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Enter the project directory:

```bash
cd fastapi-orm-workshop
```

Create the virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## MySQL Database Setup

The project includes:

```text
sql/create_database.sql
```

It can be executed with:

```bash
sudo mysql < sql/create_database.sql
```

The database configuration used by the project is:

```text
Database: orm_workshop
User: ormuser
Password: ormpass123
```

The SQLAlchemy connection is defined in:

```text
server/database.py
```

---

## Running the API

Start FastAPI from the project root:

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Test the root endpoint:

```bash
curl http://127.0.0.1:8000/
```

Expected response:

```json
{
    "message": "ORM Workshop API"
}
```

FastAPI interactive documentation is available at:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Customers

| Method | Endpoint | Description |
|---|---|---|
| POST | `/customers` | Create a customer |
| GET | `/customers` | List all customers |
| GET | `/customers/{customer_id}` | Get one customer |
| PUT | `/customers/{customer_id}` | Update a customer |
| DELETE | `/customers/{customer_id}` | Delete a customer |
| GET | `/customers/{customer_id}/orders` | Get a customer with nested orders |

### Products

| Method | Endpoint | Description |
|---|---|---|
| POST | `/products` | Create a product |
| GET | `/products` | List all products |
| GET | `/products/{product_id}` | Get one product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |
| GET | `/products/{product_id}/customers` | Get customers who purchased a product |

### Orders

| Method | Endpoint | Description |
|---|---|---|
| POST | `/orders` | Create an order with nested items |
| GET | `/orders/{order_id}` | Get a complete nested order |
| PUT | `/orders/{order_id}/status` | Update order status |
| DELETE | `/orders/{order_id}` | Delete an order |

---

## Nested Order Creation

Example:

```json
{
    "customer_id": 1,
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 1},
        {"product_id": 3, "quantity": 3}
    ]
}
```

SQLAlchemy automatically manages the foreign-key relationships between Customer, Order, OrderItem, and Product.

---

## Nested Queries

The endpoint:

```text
GET /orders/{order_id}
```

returns a complete nested Order representation:

```text
Order
 ├── Customer
 └── OrderItems
      └── Product
```

Example:

```bash
curl -s http://127.0.0.1:8000/orders/1 | python -m json.tool
```

---

## Inventory Management

When an Order is created, the requested quantity is removed from the Product inventory:

```python
product.stock -= item_data.quantity
```

The stock modification and Order creation are executed inside the same database transaction.

---

## Transactions and Rollback

A successful operation finishes with:

```python
db.commit()
```

This permanently stores the Order, its OrderItems, and the inventory updates.

If one part of the operation fails, the application executes:

```python
db.rollback()
```

For example, if an Order requests more stock than available, the API returns:

```json
{
    "detail": "Insufficient stock for Webcam"
}
```

The complete transaction is rolled back, preventing partial inventory changes.

---

## Cascade Delete

The relationship between Order and OrderItem uses:

```python
cascade="all, delete-orphan"
```

Therefore, when an Order is deleted:

```text
Order       -> deleted
OrderItems  -> deleted
Products    -> preserved
```

Products remain because they are independent records and can participate in other Orders.

---

## Independent Python Client

Run the client with:

```bash
python client/client.py
```

The client communicates with FastAPI using:

```python
requests.get()
requests.post()
requests.put()
requests.delete()
```

It also supports creating Orders from the JSON file located at:

```text
client/data/order.json
```

---

## Final Exercise

The project implements:

```text
GET /products/{product_id}/customers
```

This endpoint returns all Customers who purchased a specific Product.

The SQLAlchemy query is:

```python
statement = (
    select(models.Customer)
    .join(models.Customer.orders)
    .join(models.Order.items)
    .where(
        models.OrderItem.product_id == product_id
    )
    .distinct()
)
```

The `.distinct()` operation prevents the same Customer from appearing multiple times if that Customer purchased the selected Product more than once.

Test:

```bash
curl -s http://127.0.0.1:8000/products/1/customers | python -m json.tool
```

---

## SQL Generated by SQLAlchemy

The SQLAlchemy engine is configured with:

```python
echo=True
```

This allows the SQL generated by the ORM to be displayed in the Uvicorn terminal.

For example:

```python
order.status = data.status
db.commit()
```

causes SQLAlchemy to generate the corresponding SQL `UPDATE` statement automatically.

---

## Conclusion

This workshop demonstrates how FastAPI, SQLAlchemy, and MySQL can be combined to build a structured database-driven REST API.

SQLAlchemy allows Python objects to represent relational database records while automatically generating the required SQL operations. ORM relationships make it possible to work with connected objects such as Customers, Orders, OrderItems, and Products without manually managing every foreign-key operation.

Transactions, commit, and rollback ensure that complex operations such as Order creation and inventory modification remain consistent even when an error occurs.

The independent Python client also demonstrates the separation between the API implementation and external applications consuming the service.

---

## Authors

- **Paul Rodríguez**
- **Kevin Erazo**

Web Applications  
Semester II — 2026
