from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения 'users'.
    Класс 'UsersConfig' используется
    для настройки приложения 'users' в Django.
    Он определяет параметры конфигурации для данного приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
