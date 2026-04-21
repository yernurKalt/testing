from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class OutboxEvent(Base):
    __tablename__ = "outbox_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    