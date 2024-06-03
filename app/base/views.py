from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from .forms import MyUserCreationForm
from .models import User
# Create your views here.

def register_page(request):
  form = MyUserCreationForm()

  if request.method == 'GET':
    form = MyUserCreationForm()
    return render(request, 'register.html', {'form': form})   

  if request.method == 'POST':
    form = MyUserCreationForm(request.POST)
    if form.is_valid():
      user = form.save(commit=False)
      user.email = user.email.lower()
      user.save()
      login(request, user)
      return redirect('home')
    else:
        messages.error(request, 'An error occurred during registration')

  return render(request, 'register.html', {'form': form})

def login_page(request):
  page = 'login'
  if request.user.is_authenticated:
    return redirect('home')

  if request.method == 'POST':
    email = request.POST.get('email').lower()
    password = request.POST.get('password')

    try:
      user = User.objects.get(email=email)
    except:
      messages.error(request, 'User does not exist')

    user = authenticate(request, email=email, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username and passowrd does not match')

  context = {'page': page}
  return render(request, 'login.html', context)

def logout_page(request):
  logout(request)
  return redirect('home')

def home(request):
  accounts = User.objects.all()
  context = {'accounts': accounts}
  return render(request, 'home.html', context)

def create_offer(request):
  context = {}
  return render(request, 'base/offer.html', context)


def account_page(request):
  return render(request)