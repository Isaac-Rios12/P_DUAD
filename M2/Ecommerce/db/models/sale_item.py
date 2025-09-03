from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Numeric
from .base import Base
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime



class SaleItem(Base):
    __tablename__ = "sale_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relaciones
    sale: Mapped["Sale"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship()