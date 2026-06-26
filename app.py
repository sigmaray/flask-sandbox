import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")


def parse_car_form(form):
    make = form.get("make", "").strip()
    model = form.get("model", "").strip()
    year_raw = form.get("year", "").strip()
    color = form.get("color", "").strip() or None
    price_raw = form.get("price", "").strip()

    errors = []
    if not make:
        errors.append("Марка обязательна.")
    if not model:
        errors.append("Модель обязательна.")

    year = None
    if not year_raw:
        errors.append("Год выпуска обязателен.")
    else:
        try:
            year = int(year_raw)
            if year < 1886 or year > 2100:
                errors.append("Год должен быть от 1886 до 2100.")
        except ValueError:
            errors.append("Год должен быть числом.")

    price = None
    if price_raw:
        try:
            price = float(price_raw.replace(",", "."))
            if price < 0:
                errors.append("Цена не может быть отрицательной.")
        except ValueError:
            errors.append("Цена должна быть числом.")

    return {
        "make": make,
        "model": model,
        "year": year,
        "color": color,
        "price": price,
        "errors": errors,
    }


@app.route("/")
def index():
    cars = db.fetch_cars()
    return render_template("index.html", cars=cars)


@app.route("/cars/new", methods=["GET", "POST"])
def create_car():
    if request.method == "GET":
        return render_template("form.html", car=None, action="create")

    data = parse_car_form(request.form)
    if data["errors"]:
        for error in data["errors"]:
            flash(error, "error")
        return render_template("form.html", car=data, action="create"), 400

    db.create_car(data["make"], data["model"], data["year"], data["color"], data["price"])
    flash("Автомобиль добавлен.", "success")
    return redirect(url_for("index"))


@app.route("/cars/<int:car_id>/edit", methods=["GET", "POST"])
def edit_car(car_id):
    car = db.fetch_car(car_id)
    if not car:
        flash("Автомобиль не найден.", "error")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("form.html", car=car, action="edit")

    data = parse_car_form(request.form)
    if data["errors"]:
        for error in data["errors"]:
            flash(error, "error")
        data["id"] = car_id
        return render_template("form.html", car=data, action="edit"), 400

    updated = db.update_car(
        car_id, data["make"], data["model"], data["year"], data["color"], data["price"]
    )
    if not updated:
        flash("Автомобиль не найден.", "error")
        return redirect(url_for("index"))

    flash("Автомобиль обновлён.", "success")
    return redirect(url_for("index"))


@app.route("/cars/<int:car_id>/delete", methods=["POST"])
def delete_car(car_id):
    if db.delete_car(car_id):
        flash("Автомобиль удалён.", "success")
    else:
        flash("Автомобиль не найден.", "error")
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.init_db()
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=5000)
