# Workshop 4 - Quick Setup

## 1. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

## 3. Create the MySQL database

Option A - execute the included SQL script:

```bash
sudo mysql < sql/create_database.sql
```

If your MySQL root account requires another authentication method, enter MySQL manually
and execute the contents of `sql/create_database.sql`.

Verify:

```bash
mysql -u ormuser -p orm_workshop
```

Password:

```text
ormpass123
```

## 4. Start FastAPI

From the project root:

```bash
uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload
```

Test:

```bash
curl http://127.0.0.1:8000/
```

## 5. Verify the tables

```bash
mysql -u ormuser -p orm_workshop
```

Then:

```sql
SHOW TABLES;
```

Expected:

```text
customers
order_items
orders
products
```

## 6. Create the sample customers

```bash
curl -X POST http://127.0.0.1:8000/customers     -H "Content-Type: application/json"     -d '{"name":"Alice Brown","email":"alice@example.com"}'
```

```bash
curl -X POST http://127.0.0.1:8000/customers     -H "Content-Type: application/json"     -d '{"name":"John Smith","email":"john@example.com"}'
```

```bash
curl -X POST http://127.0.0.1:8000/customers     -H "Content-Type: application/json"     -d '{"name":"Maria Lopez","email":"maria@example.com"}'
```

## 7. Create the sample products

```bash
curl -X POST http://127.0.0.1:8000/products     -H "Content-Type: application/json"     -d '{"name":"Mechanical Keyboard","price":85.50,"stock":20}'
```

```bash
curl -X POST http://127.0.0.1:8000/products     -H "Content-Type: application/json"     -d '{"name":"Wireless Mouse","price":28.50,"stock":40}'
```

```bash
curl -X POST http://127.0.0.1:8000/products     -H "Content-Type: application/json"     -d '{"name":"USB-C Hub","price":42.00,"stock":15}'
```

```bash
curl -X POST http://127.0.0.1:8000/products     -H "Content-Type: application/json"     -d '{"name":"Webcam","price":65.00,"stock":10}'
```

## 8. Run the Python client

```bash
python client/client.py
```

## 9. Final endpoint

```bash
curl -s http://127.0.0.1:8000/products/1/customers | python -m json.tool
```

The project already includes the final Workshop 4 endpoint and the client option used to test it.
