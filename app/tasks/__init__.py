"""
Blueprint модуля задач.

Отвечает за:
- отображение списка задач
- добавление, редактирование и удаление задач
- изменение статуса задачи
"""

from flask import Blueprint

# Blueprint для маршрутов, связанных с задачами
tasks_bp = Blueprint(
    "tasks",
    __name__,
    template_folder="../templates/tasks",
)

# Импорт маршрутов (после создания Blueprint)
from . import routes  # noqa: E402