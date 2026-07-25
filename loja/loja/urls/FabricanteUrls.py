from django.urls import path
from loja.views.FabricanteView import fabricante_view, delete_fabricante_view
urlpatterns = [path('', fabricante_view, name='fabricante'), path('edit/<int:id>', fabricante_view, name='edit_fabricante'), path('delete/<int:id>', delete_fabricante_view, name='delete_fabricante')]
