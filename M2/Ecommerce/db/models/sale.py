from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Numeric
from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from typing import List


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"), nullable=False)
    billing_address: Mapped[str] = mapped_column(String(250), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Rlaciones
    user: Mapped["User"] = relationship(back_populates="sales")
    cart: Mapped["Cart"] = relationship("Cart")  # a que cart le pertence la venta
    items: Mapped[List["SaleItem"]] = relationship(back_populates="sale", cascade="all, delete-orphan")

