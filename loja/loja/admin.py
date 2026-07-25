from django.contrib import admin
from .models import * #imporata nossos models
admin.site.register(Categoria)
class FabricanteAdmin(admin.ModelAdmin):
    # Cria um filtro de hierarquia com datas
    date_hierarchy = 'criado_em'
class ProdutoAdmin(admin.ModelAdmin):
    date_hierarchy = 'criado_em'
    list_display = ('Produto', 'destaque', 'promocao', 'msgPromocao',
    'preco', 'categoria',)
    empty_value_display = 'Vazio'
    fields = ('Produto', 'destaque', 'promocao',
'msgPromocao', 'preco', 'categoria',)

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Fabricante,FabricanteAdmin)
admin.site.register(Usuario)

# Register your models here.
