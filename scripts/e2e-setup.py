"""Prepare database state for Playwright e2e tests."""

from flask_migrate import upgrade
from sqlalchemy import text

from app import app
from extensions import db
from models import User


def main() -> None:
    with app.app_context():
        upgrade()
        db.session.execute(text("TRUNCATE TABLE cars, users RESTART IDENTITY"))
        db.session.commit()

        user = User(username="e2e")
        user.set_password("e2e-pass")
        db.session.add(user)
        db.session.commit()
        print("E2E user ready: e2e / e2e-pass")


if __name__ == "__main__":
    main()
