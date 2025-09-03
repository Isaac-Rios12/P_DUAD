from sqlalchemy import Integer, String, DateTime, func, ForeignKey
from .base import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fullname: Mapped[str] = mapped_column(String(150), nullable=False)
    nickname: Mapped[str] = mapped_column(String(75), nullable=False, unique=True)
    email:Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    #the user has several carts
    carts: Mapped[list["Cart"]] = relationship(back_populates="user")
    #the user has a role
    role: Mapped["Role"] = relationship(back_populates="users")
    #lista de compras del usuario
    sales: Mapped[list["Sale"]] = relationship(back_populates="user")