import os

from dotenv import load_dotenv
from flask import Flask, redirect, url_for
from flask_admin import Admin

from admin_views import CarAdmin
from extensions import db
from models import Car

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/flask-cars"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

admin = Admin(app, name="Flask Cars", url="/admin")
admin.add_view(CarAdmin(Car, db, name="Автомобили", endpoint="cars"))


@app.route("/")
def index():
    return redirect(url_for("cars.index_view"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=os.environ.get("FLASK_DEBUG", "0") == "1", host="0.0.0.0", port=5000)
