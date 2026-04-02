from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class ReservationModel(Base):
    __tablename__ = "reservations"
    id: Mapped[int] = mapped_column(primary_key=True)
    is_confirmed = mapped_column(Boolean, nullable=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    