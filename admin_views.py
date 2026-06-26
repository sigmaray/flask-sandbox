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
        "make": "Make",
        "model": "Model",
        "year": "Year",
        "color": "Color",
        "price": "Price",
        "created_at": "Created",
        "updated_at": "Updated",
    }

    form_columns = ["make", "model", "year", "color", "price"]
    form_args = {
        "make": {"label": "Make"},
        "model": {"label": "Model"},
        "year": {"label": "Year"},
        "color": {"label": "Color"},
        "price": {"label": "Price"},
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
        "username": "Username",
    }

    form_columns = ["username", "password", "password_confirm"]
    form_args = {
        "username": {"label": "Username"},
    }

    form_extra_fields = {
        "password": PasswordField("Password"),
        "password_confirm": PasswordField("Confirm password"),
    }

    can_view_details = True
    page_size = 25

    def create_form(self, obj=None):
        form = super().create_form(obj)
        form.password.validators = [
            validators.DataRequired(message="Password is required."),
        ]
        form.password_confirm.validators = [
            validators.DataRequired(),
            validators.EqualTo("password", message="Passwords do not match."),
        ]
        return form

    def edit_form(self, obj=None):
        form = super().edit_form(obj)
        form.password.validators = [validators.Optional()]
        form.password_confirm.validators = [
            validators.Optional(),
            validators.EqualTo("password", message="Passwords do not match."),
        ]
        return form

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

    def delete_model(self, model):
        if model.id == current_user.id:
            flash("Cannot delete the current user.", "error")
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

    @expose("/clear/", methods=["POST"])
    def clear(self):
        from car_service import clear_cars_table

        category, message = clear_cars_table()
        flash(message, category)
        return redirect(url_for(".index"))
