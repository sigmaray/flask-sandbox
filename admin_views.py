from flask import flash, redirect, request, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView


class CarAdmin(ModelView):
    column_list = ["id", "make", "model", "year", "color", "price", "updated_at"]
    column_searchable_list = ["make", "model", "color"]
    column_filters = ["make", "year", "color"]
    column_sortable_list = ["id", "make", "model", "year", "price", "updated_at"]
    column_default_sort = ("id", False)

    column_labels = {
        "id": "ID",
        "make": "Марка",
        "model": "Модель",
        "year": "Год",
        "color": "Цвет",
        "price": "Цена",
        "created_at": "Создан",
        "updated_at": "Обновлён",
    }

    form_columns = ["make", "model", "year", "color", "price"]
    form_args = {
        "make": {"label": "Марка"},
        "model": {"label": "Модель"},
        "year": {"label": "Год"},
        "color": {"label": "Цвет"},
        "price": {"label": "Цена"},
    }

    can_view_details = True
    page_size = 25


class ToolsAdmin(BaseView):
    @expose("/")
    def index(self):
        from models import Car
        from seed_data import SAMPLE_CARS

        return self.render(
            "admin/tools.html",
            cars_count=Car.query.count(),
            sample_count=len(SAMPLE_CARS),
        )

    @expose("/seed/", methods=["POST"])
    def seed(self):
        from car_service import seed_cars

        clear = request.form.get("clear") == "1"
        category, message = seed_cars(clear=clear)
        flash(message, category)
        return redirect(url_for(".index"))
