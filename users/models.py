from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES,default='student')
    profile_image=models.ImageField(upload_to='profile_images/',blank=True,null=True,default='profile_images/avater.png')
    bio = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return self.username 

