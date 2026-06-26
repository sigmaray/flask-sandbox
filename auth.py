from flask import flash, redirect, render_template, request, url_for
from flask_admin import AdminIndexView, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, logout_user

from extensions import db
from models import User

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Войдите, чтобы получить доступ."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


class SecureModelView(ModelView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


class SecureBaseView(BaseView):
    def is_accessible(self) -> bool:
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


def init_auth(app) -> None:
    login_manager.init_app(app)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("cars.index_view"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user, remember=True)
                next_page = request.args.get("next")
                if next_page and next_page.startswith("/"):
                    return redirect(next_page)
                return redirect(url_for("cars.index_view"))

            flash("Неверный логин или пароль.", "danger")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))
