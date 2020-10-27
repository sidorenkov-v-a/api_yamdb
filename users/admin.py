from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import User

#
# class CustomUserCreationForm(UserCreationForm):
#     class Meta(UserCreationForm):
#         model = User
#         fields = ('email',)


class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'role')
    search_fields = ('username', 'email', 'role')

    ordering = ('role', 'email',)
    empty_value_display = '-пусто-'

    fieldsets = (
        (None,
         {'fields': (
             'email', 'password', 'username', 'first_name', 'last_name', 'bio'
         )}),
        ('Permissions', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role')}
         ),
    )


admin.site.register(User, UserAdmin)
