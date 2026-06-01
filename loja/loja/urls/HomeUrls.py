from django.urls import path
from loja.views.HomeView import *
urlpatterns = [
path("", home_view,name= 'home'),
]