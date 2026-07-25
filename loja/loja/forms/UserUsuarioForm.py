from django import forms
from django.contrib.auth.models import User
from loja.models import Usuario

class UserUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['user', 'perfil', 'aniversario']
        widgets = {'user': forms.HiddenInput(), 'perfil': forms.Select(attrs={'class':'form-control'}), 'aniversario': forms.DateInput(attrs={'class':'form-control','type':'date'})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.perfil != 1:
            self.fields.pop('perfil', None)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {f: forms.TextInput(attrs={'class':'form-control'}) for f in fields}
        widgets['email'] = forms.EmailInput(attrs={'class':'form-control'})
