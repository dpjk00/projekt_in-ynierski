from django.urls import path
from . import views

urlpatterns = [
  path('register/', views.register_page, name="register_page"),
  path('login/', views.login_page, name="login_page"),
  path('logout/', views.logout_page, name="logout_page"),
  path('', views.home, name="home"),
  path('offer/', views.create_offer, name='create_offer_page'),
  path('account/', views.account_page, name="account_page"),
]