"""
Модели базы данных приложения.

Содержит описание сущностей:
- User — пользователь системы
- Task — задача пользователя
"""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# Экземпляр SQLAlchemy создаётся здесь
# и инициализируется в create_app()
db = SQLAlchemy()


class User(db.Model):
    """
    Модель пользователя.

    Хранит данные для аутентификации и
    связан с задачами пользователя.
    """

    id = db.Column(db.Integer, primary_key=True)

    # Имя пользователя (отображается в интерфейсе)
    name = db.Column(db.String(100), nullable=False)

    # Логин (уникален)
    username = db.Column(db.String(80), unique=True, nullable=False)

    # Хеш пароля
    password_hash = db.Column(db.String(255), nullable=False)

    # Дата регистрации
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связь с задачами
    tasks = db.relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Task(db.Model):
    """
    Модель задачи пользователя.
    """

    id = db.Column(db.Integer, primary_key=True)

    # Внешний ключ на пользователя
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
    )

    # Заголовок задачи
    title = db.Column(db.String(200), nullable=False)

    # Описание задачи
    description = db.Column(db.Text, default="")

    # Статус задачи: active / done
    status = db.Column(db.String(10), nullable=False, default="active")

    # Дата создания и последнего обновления
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )