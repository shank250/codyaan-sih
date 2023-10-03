from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Create your models here.
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'

class UserData(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
 
class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, unique=True)    
    full_name = models.CharField(max_length=100)
    public_id = models.CharField(max_length=20,unique=True)
    mobile_number = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    aadhar_number = models.BigIntegerField()
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name
