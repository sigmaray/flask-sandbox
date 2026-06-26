from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db


class Car(db.Model):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(db.String(100), nullable=False)
    model: Mapped[str] = mapped_column(db.String(100), nullable=False)
    year: Mapped[int] = mapped_column(nullable=False)
    color: Mapped[str | None] = mapped_column(db.String(50))
    price: Mapped[float | None] = mapped_column(db.Numeric(12, 2))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __str__(self) -> str:
        return f"{self.make} {self.model} ({self.year})"
