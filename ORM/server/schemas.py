from datetime import date
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr
)


# CUSTOMER

class CustomerCreate(BaseModel):
    name: str
    email: EmailStr


class CustomerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


# PRODUCT

class ProductCreate(BaseModel):
    name: str
    price: Decimal
    stock: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    stock: int | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: Decimal
    stock: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ORDER ITEM

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    quantity: int
    unit_price: Decimal
    product: ProductResponse

    model_config = ConfigDict(
        from_attributes=True
    )


# ORDER

class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    id: int
    order_date: date
    status: str
    customer: CustomerResponse
    items: list[OrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class OrderStatusUpdate(BaseModel):
    status: str


# CUSTOMER WITH ORDERS

class CustomerOrderResponse(BaseModel):
    id: int
    order_date: date
    status: str
    items: list[OrderItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )


class CustomerWithOrdersResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    orders: list[CustomerOrderResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
