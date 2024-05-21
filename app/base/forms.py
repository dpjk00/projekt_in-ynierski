from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import User

class MyUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['name', 'email', 'password1', 'password2']

class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ['name', 'email']
