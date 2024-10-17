from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
  path('register/', views.register_page, name="register_page"),
  path('login/', views.login_page, name="login_page"),
  path('logout/', views.logout_page, name="logout_page"),
  path('', views.home, name="home"),
  path('offer/', views.create_offer, name='create_offer_page'),
  path('account/', views.account_page, name="account_page"),
  path('myoffers/', views.my_offers, name="my_offers_page"),
  path('create-offer', views.create_offer, name='create_offer'),
  path('update-offer/<str:pk>/', views.update_offer, name="update_offer"),
  path('delete-offer/<str:pk>/', views.delete_offer, name="delete_offer"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)