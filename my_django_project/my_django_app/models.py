from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class users_info(models.Model):
    user_name = models.CharField(max_length=100)
    user_age = models.IntegerField()
    user_city = models.CharField(max_length=100)
    user_hobby = models.TextField()

    def __str__(self):
        return f"{self.user_name} {self.user_age} {self.user_city} {self.user_hobby}"


class users_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=100)
    user_age = models.IntegerField()
    user_city = models.CharField(max_length=100)
    user_hobby = models.TextField()
    user_image = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user_name} {self.user_age} {self.user_city} {self.user_hobby} {self.user_image}"





"""
from django.db import models

# Create your models here.

class users_info(models.Model):
    user_name = models.CharField(max_length=100)
    user_age = models.PositiveIntegerField()
    user_city = models.CharField(max_length=100)
    user_hobby = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user_name} {self.user_city} {self.user_age} {self.user_hobby}"
        """
