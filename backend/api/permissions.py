from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений для определения доступа к объектам
    на основе авторства.
    """
    def has_permission(self, request, view):
        """Определяет, имеет ли пользователь разрешение
        для доступа к представлению.
        (разрешено: безопасные методы или
        права предастовляются зарегистрированному пользователю )
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Определяет, имеет ли пользователь разрешение
        для доступа к конкретному объекту.
        (разрешено: безопасные методы или
        права предастовляются если пользователь является автором )
        """
        return obj.author == request.user


class AdminOrReadOnly(permissions.BasePermission):
    """
    Пользовательский класс разрешений для определения доступа
    к объектам на основе роли администратора.
    """
    def has_permission(self, request, obj):
        """Определяет, имеет ли пользователь разрешение
        для доступа к представлению.
        (разрешено: безопасные методы или
        права предастовляются если пользователь является администратором)
        """
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
