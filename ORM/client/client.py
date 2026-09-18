import json
import requests


BASE_URL = "http://127.0.0.1:8000"


def show_response(response):
    print()
    print("HTTP:", response.status_code)

    try:
        print(
            json.dumps(
                response.json(),
                indent=4
            )
        )
    except Exception:
        print(response.text)


def create_customer():
    name = input("Customer name: ")
    email = input("Email: ")

    data = {
        "name": name,
        "email": email
    }

    response = requests.post(
        f"{BASE_URL}/customers",
        json=data
    )

    show_response(response)


def list_customers():
    response = requests.get(
        f"{BASE_URL}/customers"
    )

    show_response(response)


def create_product():
    name = input("Product name: ")
    price = input("Price: ")
    stock = int(input("Stock: "))

    data = {
        "name": name,
        "price": price,
        "stock": stock
    }

    response = requests.post(
        f"{BASE_URL}/products",
        json=data
    )

    show_response(response)


def list_products():
    response = requests.get(
        f"{BASE_URL}/products"
    )

    show_response(response)


def create_order_from_json():
    filename = input(
        "JSON filename [client/data/order.json]: "
    )

    if filename.strip() == "":
        filename = "client/data/order.json"

    with open(
        filename,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    response = requests.post(
        f"{BASE_URL}/orders",
        json=data
    )

    show_response(response)


def show_order():
    order_id = input("Order ID: ")

    response = requests.get(
        f"{BASE_URL}/orders/{order_id}"
    )

    show_response(response)


def show_customer_orders():
    customer_id = input("Customer ID: ")

    response = requests.get(
        f"{BASE_URL}/customers/"
        f"{customer_id}/orders"
    )

    show_response(response)


def update_order():
    order_id = input("Order ID: ")
    status = input("New status: ")

    data = {
        "status": status
    }

    response = requests.put(
        f"{BASE_URL}/orders/"
        f"{order_id}/status",
        json=data
    )

    show_response(response)


def delete_order():
    order_id = input("Order ID: ")

    response = requests.delete(
        f"{BASE_URL}/orders/{order_id}"
    )

    show_response(response)


def show_product_customers():
    product_id = input("Product ID: ")

    response = requests.get(
        f"{BASE_URL}/products/"
        f"{product_id}/customers"
    )

    show_response(response)


while True:
    print()
    print("================================")
    print("      ORM WORKSHOP CLIENT")
    print("================================")
    print("1. Create customer")
    print("2. List customers")
    print("3. Create product")
    print("4. List products")
    print("5. Create order from JSON")
    print("6. Show order")
    print("7. Show customer orders")
    print("8. Update order")
    print("9. Delete order")
    print("10. Show customers by product")
    print("0. Exit")

    option = input("Option: ")

    if option == "1":
        create_customer()
    elif option == "2":
        list_customers()
    elif option == "3":
        create_product()
    elif option == "4":
        list_products()
    elif option == "5":
        create_order_from_json()
    elif option == "6":
        show_order()
    elif option == "7":
        show_customer_orders()
    elif option == "8":
        update_order()
    elif option == "9":
        delete_order()
    elif option == "10":
        show_product_customers()
    elif option == "0":
        break
    else:
        print("Invalid option")
