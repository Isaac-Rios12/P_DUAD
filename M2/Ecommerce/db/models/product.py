from sqlalchemy import Integer, String, DateTime, func, Numeric
from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional


class Product(Base):
    __tablename__ = 'products'

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)  # SKU único
    name: Mapped[str] = mapped_column(String(75), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(150))
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    #muchos carritos pueden tener este producto
    cart_items: Mapped[list["CartItem"]] = relationship(back_populates="product")
