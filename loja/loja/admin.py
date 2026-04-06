from django.contrib import admin
from .models import * #imporata nossos models
admin.site.register(Fabricante)
admin.site.register(Categoria)
admin.site.register(Produto)

# Register your models here.
