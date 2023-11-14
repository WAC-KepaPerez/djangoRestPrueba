from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
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
    done = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.value
    
class CustomUser(AbstractUser):
    # Add your desired fields here
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    id_tipousuario = models.IntegerField(default=1)

    def __str__(self):
        return self.username  # Customize how user objects are displayedpython manage.py makemigrations accounts
    
class Post(models.Model):
    name = models.CharField(max_length=255)
    post_id = models.IntegerField()
    image = models.ImageField(upload_to='post_images/')

class MyModel(models.Model):
    image = models.ImageField(upload_to='Images/')
    image2 = models.ImageField(upload_to='Images2/')