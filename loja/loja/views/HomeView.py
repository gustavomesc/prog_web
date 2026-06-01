from loja.models import Produto
from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
def home_view(request):
    produto = request.GET.get("produto")
    produtos = Produto.objects.all()
    if produto is not None:
        produtos = produtos.filter(Produto__contains=produto)
    context = {
            'produtos': produtos
        }
    return render(request, template_name='home/home.html', status=200,context=context)
