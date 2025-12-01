from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cart_id: Mapped[int] = mapped_column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id: Mapped[int] =  mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    #
    cart: Mapped["Cart"] = relationship(back_populates="items")
    #es un producto unico
    product: Mapped["Product"] = relationship(back_populates="cart_items")