from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

Users = get_user_model()


@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ('username',
                    'email',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_active',
                    'access_to_the_bot'
                    )
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username',
                           'password')
                }
         ),
        ('Персональная информация', {'fields': ('first_name',
                                                'last_name',
                                                'email',
                                                )
                                     }
         ),
        ('Доступы', {'fields': ('is_active',
                                'is_staff',
                                'is_superuser',
                                'access_to_the_bot'
                                )
                     }
         ),
        ('Даты входа и регистрации', {'fields': ('last_login',
                                                 'date_joined')
                                      }
         ),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
