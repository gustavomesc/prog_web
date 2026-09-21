from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from loja.models import Produto, Carrinho, CarrinhoItem


def carrinho_aberto(request):
    return Carrinho.objects.filter(
        pk=request.session.get('carrinho_id'), situacao=0,
        criado_em__date=timezone.localdate(),
    ).first()


@require_POST
def create_carrinhoitem_view(request, produto_id):
    produto = get_object_or_404(Produto, pk=produto_id)
    carrinho = carrinho_aberto(request)
    if carrinho is None:
        carrinho = Carrinho.objects.create()
        request.session['carrinho_id'] = carrinho.pk
    item, criado = CarrinhoItem.objects.get_or_create(
        carrinho=carrinho, produto=produto,
        defaults={'quantidade': 1, 'preco': produto.preco},
    )
    if not criado:
        CarrinhoItem.objects.filter(pk=item.pk).update(quantidade=F('quantidade') + 1)
    return redirect('list_carrinho')


def list_carrinho_view(request):
    carrinho = carrinho_aberto(request)
    return render(request, 'carrinho/carrinho-listar.html', {
        'carrinho': carrinho,
        'itens': carrinho.itens.select_related('produto') if carrinho else [],
    })


@login_required
def confirmar_carrinho_view(request):
    if request.method == 'POST':
        carrinho = carrinho_aberto(request)
        if carrinho is None or not carrinho.itens.exists():
            return redirect('list_carrinho')
        carrinho.user = request.user
        carrinho.situacao = 1
        carrinho.confirmado_em = timezone.now()
        carrinho.save(update_fields=['user', 'situacao', 'confirmado_em'])
        request.session['ultimo_pedido_id'] = carrinho.pk
        request.session.pop('carrinho_id', None)
        return redirect('confirmar_carrinho')
    carrinho = Carrinho.objects.filter(
        pk=request.session.get('ultimo_pedido_id'), user=request.user, situacao=1,
    ).first()
    if carrinho is None:
        return redirect('list_carrinho')
    return render(request, 'carrinho/carrinho-confirmado.html', {
        'carrinho': carrinho, 'itens': carrinho.itens.select_related('produto'),
    })


def item_da_sessao(request, item_id):
    carrinho = carrinho_aberto(request)
    return get_object_or_404(
        CarrinhoItem, pk=item_id, carrinho_id=carrinho.pk if carrinho else -1,
    )


@require_POST
def alterar_quantidade_view(request, item_id, acao):
    item = item_da_sessao(request, item_id)
    itens = CarrinhoItem.objects.filter(pk=item.pk)
    if acao == 'adicionar':
        itens.update(quantidade=F('quantidade') + 1)
    elif acao == 'diminuir':
        itens.filter(quantidade__gt=1).update(quantidade=F('quantidade') - 1)
    return redirect('list_carrinho')


@require_POST
def remover_item_view(request, item_id):
    item_da_sessao(request, item_id).delete()
    return redirect('list_carrinho')
