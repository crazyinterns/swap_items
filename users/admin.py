from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = [
        'username',
        'first_name',
        'last_name',
        'email',
    ]
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
