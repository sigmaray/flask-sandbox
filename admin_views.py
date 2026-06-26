from flask import flash, redirect, request, url_for
from flask_admin import expose
from flask_login import current_user
from wtforms import PasswordField, validators

from auth import SecureBaseView, SecureModelView


class CarAdmin(SecureModelView):
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


class UserAdmin(SecureModelView):
    column_list = ["id", "username"]
    column_searchable_list = ["username"]
    column_sortable_list = ["id", "username"]
    column_default_sort = ("id", False)
    column_exclude_list = ["password_hash"]
    form_excluded_columns = ["password_hash"]

    column_labels = {
        "id": "ID",
        "username": "Логин",
    }

    form_columns = ["username", "password", "password_confirm"]
    form_args = {
        "username": {"label": "Логин"},
    }

    form_extra_fields = {
        "password": PasswordField("Пароль"),
        "password_confirm": PasswordField("Подтверждение пароля"),
    }

    can_view_details = True
    page_size = 25

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.password.validators = [
            validators.DataRequired(message="Пароль обязателен."),
        ]
        form.password_confirm.validators = [
            validators.DataRequired(),
            validators.EqualTo("password", message="Пароли не совпадают."),
        ]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.password.validators = [validators.Optional()]
        form.password_confirm.validators = [
            validators.Optional(),
            validators.EqualTo("password", message="Пароли не совпадают."),
        ]
        return form

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

    def delete_model(self, model):
        if model.id == current_user.id:
            flash("Нельзя удалить текущего пользователя.", "error")
            return False
        return super().delete_model(model)


class ToolsAdmin(SecureBaseView):
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
