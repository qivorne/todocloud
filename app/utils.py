"""
Вспомогательные утилиты приложения.

Содержит декораторы и функции,
используемые в разных частях проекта.
"""

from functools import wraps

from flask import session, redirect, url_for, request


def login_required(view):
    """
    Декоратор для защиты маршрутов.

    Проверяет, авторизован ли пользователь.
    Если нет — перенаправляет на страницу входа
    с сохранением исходного URL.
    """

    @wraps(view)
    def wrapped(*args, **kwargs):
        # Если пользователь не вошёл в систему —
        # перенаправляем на страницу логина
        if not session.get("user_id"):
            return redirect(
                url_for(
                    "auth.login",
                    next=request.path,
                )
            )

        return view(*args, **kwargs)

    return wrapped