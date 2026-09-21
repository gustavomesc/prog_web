from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from loja.models import Produto, Carrinho, CarrinhoItem


class FluxoLojaTests(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(Produto='Produto de teste', preco=Decimal('12.50'))
        self.usuario = User.objects.create_user(username='cliente', password='senha-teste')

    def comprar(self):
        return self.client.post(reverse('create_carrinhoitem', args=[self.produto.pk]))

    def test_home_e_carrinho_vazio(self):
        self.assertContains(self.client.get(reverse('home')), 'Comprar')
        self.assertContains(self.client.get(reverse('list_carrinho')), 'Seu carrinho está vazio.')

    def test_compra_quantidade_e_exclusao(self):
        self.comprar()
        self.comprar()
        item = CarrinhoItem.objects.get()
        self.assertEqual(item.quantidade, 2)
        self.client.post(reverse('alterar_quantidade', args=[item.pk, 'adicionar']))
        item.refresh_from_db()
        self.assertEqual(item.total, Decimal('37.50'))
        for _ in range(3):
            self.client.post(reverse('alterar_quantidade', args=[item.pk, 'diminuir']))
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)
        self.assertContains(self.client.get(reverse('list_carrinho')), '12,50')
        self.client.post(reverse('remover_carrinhoitem', args=[item.pk]))
        self.assertFalse(CarrinhoItem.objects.exists())

    def test_sessao_invalida_cria_novo_carrinho(self):
        sessao = self.client.session
        sessao['carrinho_id'] = 9999
        sessao.save()
        self.assertEqual(self.client.get(reverse('list_carrinho')).status_code, 200)
        self.comprar()
        self.assertEqual(Carrinho.objects.count(), 1)

    def test_nao_altera_carrinho_de_outra_sessao(self):
        self.comprar()
        item = CarrinhoItem.objects.get()
        outro = Client()
        self.assertEqual(outro.post(reverse('alterar_quantidade', args=[item.pk, 'adicionar'])).status_code, 404)
        self.assertEqual(outro.post(reverse('remover_carrinhoitem', args=[item.pk])).status_code, 404)
        self.assertEqual(self.client.get(reverse('remover_carrinhoitem', args=[item.pk])).status_code, 405)

    def test_confirmacao_com_itens_e_pedido_preservado(self):
        self.comprar()
        item = CarrinhoItem.objects.get()
        self.client.force_login(self.usuario)
        resposta = self.client.post(reverse('confirmar_carrinho'), follow=True)
        self.assertContains(resposta, 'Compra Confirmada')
        self.assertContains(resposta, self.produto.Produto)
        self.assertContains(resposta, '12,50')
        pedido = Carrinho.objects.get()
        self.assertEqual(pedido.user_id, self.usuario.pk)
        self.assertEqual(pedido.situacao, 1)
        self.assertIsNotNone(pedido.confirmado_em)
        self.assertNotIn('carrinho_id', self.client.session)
        self.assertEqual(self.client.post(reverse('alterar_quantidade', args=[item.pk, 'adicionar'])).status_code, 404)
        self.comprar()
        self.assertEqual(Carrinho.objects.count(), 2)
        item.refresh_from_db()
        self.assertEqual(item.quantidade, 1)

    def test_finalizacao_exige_login_e_nao_confirma_por_get(self):
        self.comprar()
        resposta = self.client.post(reverse('confirmar_carrinho'))
        self.assertEqual(resposta.status_code, 302)
        self.assertIn('/login?next=', resposta.url)
        self.client.force_login(self.usuario)
        self.client.get(reverse('confirmar_carrinho'))
        self.assertEqual(Carrinho.objects.get().situacao, 0)

    def test_favoritos_exigem_login_e_sao_por_usuario(self):
        url = reverse('favorito', args=[self.produto.pk])
        resposta = self.client.post(url)
        self.assertIn('/login?next=', resposta.url)
        self.client.force_login(self.usuario)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.usuario.produtos_favoritos.count(), 0)
        self.client.post(url, {'acao': 'adicionar'})
        self.client.post(url, {'acao': 'adicionar'})
        self.assertEqual(self.usuario.produtos_favoritos.count(), 1)
        self.assertContains(self.client.get(reverse('list_favoritos')), self.produto.Produto)
        outro = User.objects.create_user(username='outro')
        self.client.force_login(outro)
        self.assertNotContains(self.client.get(reverse('list_favoritos')), self.produto.Produto)
        self.client.post(url, {'acao': 'remover'})
        self.assertEqual(self.usuario.produtos_favoritos.count(), 1)
        self.client.force_login(self.usuario)
        self.client.post(url, {'acao': 'remover'})
        self.assertEqual(self.usuario.produtos_favoritos.count(), 0)

    def test_csrf_obrigatorio_para_comprar(self):
        cliente = Client(enforce_csrf_checks=True)
        self.assertEqual(cliente.post(reverse('create_carrinhoitem', args=[self.produto.pk])).status_code, 403)
