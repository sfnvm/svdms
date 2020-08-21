from django.db import models
from django.contrib.auth.models import AbstractUser

from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()


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
    email = models.EmailField(unique=True, blank=True, null=False)


class Profile(models.Model):
    class Meta:
        db_table = 'profiles'

    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)

    avatar = models.FileField(
        upload_to='images/', storage=gd_storage, blank=True)
    address = models.CharField(max_length=256, blank=True)
    phone_number = models.CharField(max_length=16, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.BooleanField(default=True)

    def __str__(self):
        return self.code
