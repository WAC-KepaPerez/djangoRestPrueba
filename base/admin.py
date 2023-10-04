from django.contrib import admin

# Register your models here.
from .models import Item,Nota

admin.site.register(Item)
admin.site.register(Nota)