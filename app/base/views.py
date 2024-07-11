from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import MyUserCreationForm, OfferForm
from .models import User, Post, Image
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

def account_page(request):
  return render(request, 'account.html')

@login_required(login_url='/login')
def my_offers(request):
  form = OfferForm()
  if request.method == 'POST':
    form = OfferForm(request.POST)
    if form.is_valid():
      form.save()

  users = User.objects.all()
  posts = Post.objects.all()
  context = {'form': form, 'posts': posts, 'users': users}
  return render(request, 'myoffers.html', context)

@login_required(login_url='/login')
def create_offer(request):
  form = OfferForm()
  if request.method == 'POST':
    Post.objects.create(
      owner = request.user,
      title = request.POST.get('title'),
      description = request.POST.get('description')
    )
    return redirect('my_offers_page')

  context = {'form': form}
  return render(request, 'offer_form.html', context)

@login_required(login_url='/login')
def update_offer(request, pk):
  post = Post.objects.get(id = pk)
  form = OfferForm(instance=post)

  if request.method == 'POST':
    form = OfferForm(request.POST, instance=post)
    if form.is_valid():
      form.save()
      return redirect('my_offers_page')

  context = {'form': form}
  return render(request, 'offer_form.html', context)

@login_required(login_url='/login')
def delete_offer(request, pk):
  post = Post.objects.get(id=pk)
  if request.method == 'POST':
    post.delete()
    return redirect('my_offers_page')
  
  return render(request, 'delete.html', {'obj': post})