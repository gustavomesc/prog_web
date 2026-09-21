from django.urls import path
from loja.views.HomeView import home_view
from loja.views.FavoritoView import list_favoritos_view, favorito_view

urlpatterns = [
    path("", home_view, name='home'),
    path("favoritos/", list_favoritos_view, name='list_favoritos'),
    path("favoritos/<int:produto_id>/", favorito_view, name='favorito'),
]
