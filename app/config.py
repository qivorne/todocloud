"""
Конфигурация приложения.

Файл содержит настройки Flask и SQLAlchemy.
Используется фабрикой приложения create_app().
"""

import os

# Абсолютный путь к директории app/
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Базовый класс конфигурации приложения.
    """

    # Секретный ключ Flask (используется для сессий и flash-сообщений)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # URI базы данных (SQLite)
    # База хранится в папке instance/, вне пакета app
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "..", "instance", "todo.db")
    )

    # Отключаем отслеживание изменений объектов (экономит ресурсы)
    SQLALCHEMY_TRACK_MODIFICATIONS = False