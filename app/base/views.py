from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.forms import modelformset_factory
from .forms import MyUserCreationForm, OfferForm, ImageForm
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

# @login_required(login_url='/login')
# def create_offer(request):
#   form = OfferForm(request.POST, request.FILES)
#   if request.method == 'POST':
#     Post.objects.create(
#       owner = request.user,
#       title = request.POST.get('title'),
#       description = request.POST.get('description'),
#       image = request.FILES.get('image')
#     )
#     return redirect('my_offers_page')

#   context = {'form': form}
#   return render(request, 'offer_form.html', context)

@login_required(login_url='/login')
def create_offer(request):
  if request.method == 'POST':
    form = OfferForm(request.POST, request.FILES)
    
    if form.is_valid():
      post = form.save(commit=False)
      post.owner = request.user
      post.save()
      
      return redirect('my_offers_page')
  
  else:
    form = OfferForm()

  context = {'form': form}
  return render(request, 'offer_form.html', context)

@login_required(login_url='/login')
def update_offer(request, pk):
  post = get_object_or_404(Post, id=pk)
  images = Image.objects.filter(post=post)

  form = OfferForm(request.POST or None, instance=post)
  ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)

  if request.method == 'POST':
    formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())

    if form.is_valid() and formset.is_valid():
      form.save()

      for form in formset.cleaned_data:
        if form:
          image = form['image']
          new_image = Image(post=post, image=image)
          new_image.save()

      images = Image.objects.filter(post=post) 
      context = {
        'form': form,
        'formset': formset,
        'post': post,
        'images': images,
      }

      return render(request, 'offer_form.html', context)

  else:
    formset = ImageFormSet(queryset=Image.objects.none())

  context = {
    'form': form,
    'formset': formset,
    'post': post,
    'images': images,
  }

  return render(request, 'offer_form.html', context)

@login_required(login_url='/login')
def delete_offer(request, pk):
  post = Post.objects.get(id=pk)
  if request.method == 'POST':
    post.delete()
    return redirect('my_offers_page')
  
  return render(request, 'delete.html', {'obj': post})