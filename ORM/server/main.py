from fastapi import (
    FastAPI,
    Depends,
    HTTPException
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import (
    engine,
    Base,
    get_db
)

from . import models
from . import schemas


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ORM Workshop API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "ORM Workshop API"
    }


# =========================================================
# CUSTOMER CRUD
# =========================================================

@app.post(
    "/customers",
    response_model=schemas.CustomerResponse
)
def create_customer(
    data: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    customer = models.Customer(
        name=data.name,
        email=data.email
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@app.get(
    "/customers",
    response_model=list[schemas.CustomerResponse]
)
def list_customers(
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(models.Customer)
    )

    return result.scalars().all()


@app.get(
    "/customers/{customer_id}",
    response_model=schemas.CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@app.put(
    "/customers/{customer_id}",
    response_model=schemas.CustomerResponse
)
def update_customer(
    customer_id: int,
    data: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if data.name is not None:
        customer.name = data.name

    if data.email is not None:
        customer.email = data.email

    db.commit()
    db.refresh(customer)

    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted",
        "id": customer_id
    }


# =========================================================
# PRODUCT CRUD
# =========================================================

@app.post(
    "/products",
    response_model=schemas.ProductResponse
)
def create_product(
    data: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    product = models.Product(
        name=data.name,
        price=data.price,
        stock=data.stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


@app.get(
    "/products",
    response_model=list[schemas.ProductResponse]
)
def list_products(
    db: Session = Depends(get_db)
):
    result = db.execute(
        select(models.Product)
    )

    return result.scalars().all()


@app.get(
    "/products/{product_id}",
    response_model=schemas.ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(
        models.Product,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.put(
    "/products/{product_id}",
    response_model=schemas.ProductResponse
)
def update_product(
    product_id: int,
    data: schemas.ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.get(
        models.Product,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if data.name is not None:
        product.name = data.name

    if data.price is not None:
        product.price = data.price

    if data.stock is not None:
        product.stock = data.stock

    db.commit()
    db.refresh(product)

    return product


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(
        models.Product,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted",
        "id": product_id
    }


# =========================================================
# ORDER - NESTED INSERT + TRANSACTION + INVENTORY
# =========================================================

@app.post(
    "/orders",
    response_model=schemas.OrderResponse
)
def create_order(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        data.customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    order = models.Order(
        customer=customer,
        status="pending"
    )

    try:
        for item_data in data.items:
            product = db.get(
                models.Product,
                item_data.product_id
            )

            if product is None:
                raise HTTPException(
                    status_code=404,
                    detail="Product not found"
                )

            if product.stock < item_data.quantity:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Insufficient stock "
                        f"for {product.name}"
                    )
                )

            product.stock -= item_data.quantity

            item = models.OrderItem(
                product=product,
                quantity=item_data.quantity,
                unit_price=product.price
            )

            order.items.append(item)

        db.add(order)
        db.commit()
        db.refresh(order)

        return order

    except Exception:
        db.rollback()
        raise


# =========================================================
# ORDER - NESTED QUERY
# =========================================================

@app.get(
    "/orders/{order_id}",
    response_model=schemas.OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.get(
        models.Order,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# =========================================================
# CUSTOMER WITH ORDERS
# =========================================================

@app.get(
    "/customers/{customer_id}/orders",
    response_model=schemas.CustomerWithOrdersResponse
)
def get_customer_orders(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.get(
        models.Customer,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


# =========================================================
# ORDER - UPDATE STATUS
# =========================================================

@app.put(
    "/orders/{order_id}/status",
    response_model=schemas.OrderResponse
)
def update_order_status(
    order_id: int,
    data: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db)
):
    order = db.get(
        models.Order,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = data.status

    db.commit()
    db.refresh(order)

    return order


# =========================================================
# ORDER - DELETE
# =========================================================

@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.get(
        models.Order,
        order_id
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted",
        "id": order_id
    }


# =========================================================
# FINAL EXERCISE
# GET /products/{product_id}/customers
# =========================================================

@app.get(
    "/products/{product_id}/customers",
    response_model=list[schemas.CustomerResponse]
)
def get_product_customers(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.get(
        models.Product,
        product_id
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    statement = (
        select(models.Customer)
        .join(models.Customer.orders)
        .join(models.Order.items)
        .where(
            models.OrderItem.product_id
            == product_id
        )
        .distinct()
    )

    result = db.execute(statement)

    return result.scalars().all()
