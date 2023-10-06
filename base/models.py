from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
class Nota(models.Model):
    value=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    
    def __str__(self):
        return self.value
    
class CustomUser(AbstractUser):
    # Add your desired fields here
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    id_tipousuario = models.IntegerField(default=1)
    # Add any other fields you need (e.g., profile picture, date of birth, etc.)
    
    # Customize other properties if necessary (e.g., ordering, verbose names)
    
    def __str__(self):
        return self.username  # Customize how user objects are displayedpython manage.py makemigrations accounts