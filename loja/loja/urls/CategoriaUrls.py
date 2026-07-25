from django.urls import path
from loja.views.CategoriaView import categoria_view, delete_categoria_view
urlpatterns = [path('', categoria_view, name='categoria'), path('edit/<int:id>', categoria_view, name='edit_categoria'), path('delete/<int:id>', delete_categoria_view, name='delete_categoria')]
