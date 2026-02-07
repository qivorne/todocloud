"""
Маршруты аутентификации.

Содержит обработчики:
- вход (login)
- регистрация (register)
- выход (logout)
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User
from . import auth_bp


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Вход пользователя в систему.

    При успешном входе сохраняет данные пользователя в сессии.
    Если пользователь был перенаправлен на логин со страницы,
    требующей авторизацию, выполняется возврат по параметру ?next=...
    """
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash("Неверный логин или пароль", "error")
            return redirect(url_for("auth.login"))

        # Сохраняем идентификатор и имя пользователя в сессии
        session["user_id"] = user.id
        session["user_name"] = user.name

        flash("Вы успешно вошли в аккаунт", "success")

        # Возвращаем пользователя на исходную страницу (если она передана)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("tasks.index"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Регистрация нового пользователя.

    Проверяет корректность заполнения формы и уникальность логина,
    сохраняет пользователя в базе данных.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        password2 = request.form.get("password2", "")

        if not all([name, username, password, password2]):
            flash("Заполните все поля", "error")
            return redirect(url_for("auth.register"))

        if password != password2:
            flash("Пароли не совпадают", "error")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Пользователь с таким логином уже существует", "error")
            return redirect(url_for("auth.register"))

        # Пароль хранится в виде хеша
        user = User(
            name=name,
            username=username,
            password_hash=generate_password_hash(password),
        )

        db.session.add(user)
        db.session.commit()

        flash("Регистрация прошла успешно. Теперь вы можете войти.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.get("/logout")
def logout():
    """
    Выход пользователя из системы.
    """
    session.clear()
    flash("Вы вышли из аккаунта", "info")
    return redirect(url_for("home"))

