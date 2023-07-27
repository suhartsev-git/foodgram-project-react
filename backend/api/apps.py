from django.apps import AppConfig


class ApiConfig(AppConfig):
    """
    Конфигурация приложения 'api'.
    Класс 'ApiConfig' используется для настройки приложения 'api' в Django.
    Он определяет параметры конфигурации для данного приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
