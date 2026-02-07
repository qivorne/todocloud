"""
Blueprint модуля аутентификации.

Отвечает за:
- вход пользователя
- регистрацию
- выход из системы
"""

from flask import Blueprint

# Blueprint для маршрутов аутентификации
auth_bp = Blueprint(
    "auth",
    __name__,
    template_folder="../templates/auth",
)

# Импорт маршрутов (после создания Blueprint)
from . import routes  # noqa: E402