from django.apps import AppConfig


class RecipesConfig(AppConfig):
    """
    Конфигурация приложения 'recipes'.
    Класс 'RecipesConfig' используется для настройки приложения 'recipes' в Django.
    Он определяет параметры конфигурации для данного приложения.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
