from django.db import models
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
  City = models.CharField(max_length=100, blank=True, null=True)
  Phone = models.CharField(max_length=100, blank=True, null=True)
  Address = models.CharField(max_length=100, blank=True, null=True)
  
  def __str__(self):
    return self.username

