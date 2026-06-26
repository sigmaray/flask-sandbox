from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

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


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __str__(self) -> str:
        return self.username
