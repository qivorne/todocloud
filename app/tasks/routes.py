"""
Маршруты для работы с задачами пользователя.

Содержит обработчики:
- просмотр списка задач
- добавление задачи
- смена статуса (active/done)
- редактирование
- удаление
"""

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)

from app.models import db, Task
from app.utils import login_required
from . import tasks_bp


@tasks_bp.get("/tasks")
@login_required
def index():
    """
    Страница со списком задач текущего пользователя.

    Задачи разделяются на:
    - активные (status="active")
    - выполненные (status="done")
    """
    user_id = session["user_id"]

    active_tasks = (
        Task.query.filter_by(user_id=user_id, status="active")
        .order_by(Task.created_at.desc())
        .all()
    )
    done_tasks = (
        Task.query.filter_by(user_id=user_id, status="done")
        .order_by(Task.created_at.desc())
        .all()
    )

    return render_template(
        "tasks/index.html",
        active_tasks=active_tasks,
        done_tasks=done_tasks,
    )


@tasks_bp.post("/tasks/add")
@login_required
def add():
    """
    Добавление новой задачи.
    """
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title:
        flash("Введите название задачи", "error")
        return redirect(url_for("tasks.index"))

    task = Task(
        user_id=session["user_id"],
        title=title,
        description=description,
        status="active",
    )

    db.session.add(task)
    db.session.commit()

    flash("Задача добавлена", "success")
    return redirect(url_for("tasks.index"))


@tasks_bp.post("/tasks/<int:task_id>/toggle")
@login_required
def toggle(task_id: int):
    """
    Переключение статуса задачи (active <-> done).
    """
    user_id = session["user_id"]

    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
    task.status = "done" if task.status == "active" else "active"

    db.session.commit()

    flash("Статус задачи изменён", "info")
    return redirect(url_for("tasks.index"))


@tasks_bp.route("/tasks/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit(task_id: int):
    """
    Редактирование задачи.
    """
    user_id = session["user_id"]
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()

        if not title:
            flash("Название задачи не может быть пустым", "error")
            return redirect(url_for("tasks.edit", task_id=task_id))

        task.title = title
        task.description = description
        db.session.commit()

        flash("Задача обновлена", "success")
        return redirect(url_for("tasks.index"))

    return render_template("tasks/edit.html", task=task)


@tasks_bp.post("/tasks/<int:task_id>/delete")
@login_required
def delete(task_id: int):
    """
    Удаление задачи.
    """
    user_id = session["user_id"]
    task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

    db.session.delete(task)
    db.session.commit()

    flash("Задача удалена", "info")
    return redirect(url_for("tasks.index"))