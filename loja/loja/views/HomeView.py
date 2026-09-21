from django.shortcuts import render
from loja.models import Produto


def home_view(request):
    produtos = Produto.objects.all()
    busca = request.GET.get("produto", "")
    if busca:
        produtos = produtos.filter(Produto__icontains=busca)
    favoritos_ids = set()
    if request.user.is_authenticated:
        favoritos_ids = set(request.user.produtos_favoritos.values_list("id", flat=True))
    return render(request, 'home/home.html', {
        'produtos': produtos, 'favoritos_ids': favoritos_ids, 'busca': busca,
    })
