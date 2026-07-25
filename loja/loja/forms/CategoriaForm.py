from django import forms
from loja.models import Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {'Categoria': forms.TextInput(attrs={'class': 'form-control'})}
