from django.contrib import admin

from users.models import User, Subscription


class UserAdmin(admin.ModelAdmin):
    """
    Административная модель для пользователей.
    """
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = ("username", "email",)
    list_filter = ("first_name", "last_name",)
    ordering = ("username", )
    empty_value_display = "-пусто-"


class SubscriptionAdmin(admin.ModelAdmin):
    """
    Административная модель для подписок пользователей
    на авторов рецептов.
    """
    list_display = (
        "id",
        "user",
        "author",
    )
    list_editable = ("user", "author",)
    ordering = ("user",)
    empty_value_display = "-пусто-"


admin.site.register(User, UserAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
