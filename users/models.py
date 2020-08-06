from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    class Meta:
        db_table = 'users'
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'manager'),
        (3, 'salesman'),
        (4, 'agency'),
    )

    role = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES, default=4)
    email = models.EmailField(unique=True, blank=True)


class Profile(models.Model):
    class Meta:
        db_table = 'profiles'

    # auto fields
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    # required
    # code = models.CharField(max_length=32, unique=True, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    gender = models.BooleanField(default=True)

    def __str__(self):
        return self.code
