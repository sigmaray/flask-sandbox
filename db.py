import os

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask-cars"
)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS cars (
                    id SERIAL PRIMARY KEY,
                    make VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    year INTEGER NOT NULL CHECK (year >= 1886 AND year <= 2100),
                    color VARCHAR(50),
                    price NUMERIC(12, 2) CHECK (price >= 0),
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        conn.commit()


def fetch_cars():
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, make, model, year, color, price, created_at, updated_at
                FROM cars
                ORDER BY id
                """
            )
            return cur.fetchall()


def fetch_car(car_id):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, make, model, year, color, price, created_at, updated_at
                FROM cars
                WHERE id = %s
                """,
                (car_id,),
            )
            return cur.fetchone()


def create_car(make, model, year, color, price):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                INSERT INTO cars (make, model, year, color, price)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, make, model, year, color, price, created_at, updated_at
                """,
                (make, model, year, color, price),
            )
            row = cur.fetchone()
        conn.commit()
        return row


def update_car(car_id, make, model, year, color, price):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                UPDATE cars
                SET make = %s,
                    model = %s,
                    year = %s,
                    color = %s,
                    price = %s,
                    updated_at = NOW()
                WHERE id = %s
                RETURNING id, make, model, year, color, price, created_at, updated_at
                """,
                (make, model, year, color, price, car_id),
            )
            row = cur.fetchone()
        conn.commit()
        return row


def delete_car(car_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM cars WHERE id = %s RETURNING id", (car_id,))
            deleted = cur.fetchone()
        conn.commit()
        return deleted is not None
