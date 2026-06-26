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
