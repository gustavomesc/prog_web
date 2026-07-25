from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#acima são bibliotecas padrões necessárias do Django, e abaixonossos models
from .fabricantes import Fabricante
from .categoria import Categoria
from .produto import Produto
PERFIL = ((1, 'Admin'), (2, 'Usuario'))
from .usuario import Usuario
