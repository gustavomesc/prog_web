from decimal import Decimal

from django.test import SimpleTestCase

from loja.forms.FabricanteForm import FabricanteForm
from loja.models import CarrinhoItem, Produto


class FirstLojaTests(SimpleTestCase):
    def test_f_fast_calcula_subtotal_em_memoria(self):
        item = CarrinhoItem(quantidade=3, preco=Decimal("12.50"))

        self.assertEqual(item.total, Decimal("37.50"))

    def test_i_isolated_alterar_um_item_nao_afeta_o_outro(self):
        produto = Produto(Produto="Caderno", preco=Decimal("8.00"))
        primeiro = CarrinhoItem(produto=produto, quantidade=1, preco=produto.preco)
        segundo = CarrinhoItem(produto=produto, quantidade=2, preco=produto.preco)

        primeiro.quantidade = 4

        self.assertEqual(segundo.total, Decimal("16.00"))

    def test_r_repeatable_retorna_o_mesmo_nome_com_a_mesma_entrada(self):
        nomes = [
            str(Produto(Produto="Caderno", preco=Decimal("8.00")))
            for _ in range(2)
        ]

        self.assertEqual(nomes, ["Caderno", "Caderno"])

    def test_s_self_verifying_rejeita_fabricante_sem_nome(self):
        formulario = FabricanteForm(data={"Fabricante": ""})

        self.assertFalse(formulario.is_valid())
        self.assertTrue(formulario.has_error("Fabricante", code="required"))

    def test_t_timely_cobre_quantidade_zero_antes_de_mudar_o_calculo(self):
        # Registra o resultado esperado antes de futuras mudancas no subtotal.
        item = CarrinhoItem(quantidade=0, preco=Decimal("12.50"))

        self.assertEqual(item.total, Decimal("0.00"))
