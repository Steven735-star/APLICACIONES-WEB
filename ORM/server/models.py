from datetime import date
from decimal import Decimal

from sqlalchemy import (
    String,
    Integer,
    Date,
    ForeignKey,
    Numeric
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from .database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100)
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True
    )

    orders: Mapped[list["Order"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    order_date: Mapped[date] = mapped_column(
        Date,
        default=date.today
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="pending"
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id")
    )

    customer: Mapped["Customer"] = relationship(
        back_populates="orders"
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(120)
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    order_items: Mapped[list["OrderItem"]] = relationship(
        back_populates="product"
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    quantity: Mapped[int] = mapped_column(
        Integer
    )

    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id")
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id")
    )

    order: Mapped["Order"] = relationship(
        back_populates="items"
    )

    product: Mapped["Product"] = relationship(
        back_populates="order_items"
    )
