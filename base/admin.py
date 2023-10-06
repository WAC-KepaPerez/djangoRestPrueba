from django.contrib import admin

# Register your models here.
from .models import Item,Nota,CustomUser
from django.contrib.auth.admin import UserAdmin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'name')  # Customize the displayed columns

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Item)
admin.site.register(Nota)