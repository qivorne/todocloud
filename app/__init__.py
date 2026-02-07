"""
Инициализация Flask-приложения.

Файл содержит фабрику приложения create_app(),
в которой:
- создаётся экземпляр Flask
- загружается конфигурация
- инициализируется база данных
- регистрируются blueprints
"""

from flask import Flask, render_template

from app.config import Config
from app.models import db


def create_app() -> Flask:
    """
    Фабрика приложения.

    Используется для создания и настройки экземпляра Flask.
    Такой подход удобен для разработки, тестирования
    и развёртывания приложения.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация базы данных
    db.init_app(app)

    # Регистрация blueprint'ов
    from app.auth import auth_bp
    from app.tasks import tasks_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    # Главная страница
    @app.get("/")
    def home():
        """
        Отображение главной страницы приложения.
        """
        return render_template("home.html")

    return app