from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class OurUserAdmin(UserAdmin):
    model = User
    list_display = (
        "username",
    )
    date_hierarchy = "date_joined"
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                )
            },
        ),
        (
            _("Telegram"),
            {
                "fields": (
                    "telegram_id",
                    "telegram_username",
                    "phone_number",
                    "referral",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "telegram_id",
                    "telegram_username",
                ),
            },
        ),
    )
    search_fields = ("username", "telegram_username")


admin.site.register(User, OurUserAdmin)
