from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from loja.models import Produto


@login_required
def list_favoritos_view(request):
    produtos = request.user.produtos_favoritos.all()
    return render(request, 'home/home.html', {
        'produtos': produtos,
        'favoritos_ids': set(produtos.values_list('id', flat=True)),
        'somente_favoritos': True,
    })


@login_required
@require_http_methods(["GET", "POST"])
def favorito_view(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    if request.method == "POST":
        if request.POST.get('acao') == 'remover':
            produto.favoritos.remove(request.user)
        else:
            produto.favoritos.add(request.user)
        return redirect('list_favoritos' if request.POST.get('origem') == 'favoritos' else 'home')
    # Retorno do login: a alteração é confirmada por POST com proteção CSRF.
    return render(request, 'home/favorito.html', {'produto': produto})
