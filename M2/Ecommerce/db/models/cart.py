from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Boolean, UniqueConstraint
from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List


class Cart(Base):
    __tablename__ = 'carts'
    __table_args__ = (
        UniqueConstraint("user_id", "is_finalized", name="uq_user_cart_active"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    is_finalized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    #carritos creados por el usuario
    user: Mapped["User"] = relationship(back_populates="carts")

    items: Mapped[List["CartItem"]] = relationship(back_populates="cart", cascade="all, delete-orphan")