from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from users.models import User

class CustomUserAdmin(UserAdmin):
    model = User 

admin.site.register(User, CustomUserAdmin)
