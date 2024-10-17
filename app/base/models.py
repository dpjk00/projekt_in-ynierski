from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from regex import regex

class User(AbstractUser):
  name = models.CharField(max_length=200, null=True)
  email = models.EmailField(unique=True, null=True)
  username = None
  phone_regex = RegexValidator(regex=r'^\+?1?[\d\s]{9,15}$', message="Phone number must match requirements.")
  phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True)
  avatar = models.ImageField(null=True, default="avatar.svg")

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

class Post(models.Model):
  title = models.CharField(max_length=200, null=True)
  description = models.CharField(max_length=2000, null=True)
  image = models.ImageField(upload_to="images/", null=True, blank=True)
  owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Image(models.Model):
  image = models.ImageField(upload_to='images/')
  post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
