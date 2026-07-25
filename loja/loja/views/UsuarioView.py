from django.shortcuts import render, get_object_or_404
from loja.models import Usuario
from loja.forms.UserUsuarioForm import UserUsuarioForm, UserForm

def list_usuario_view(request):
    return render(request, 'usuario/usuario.html', {'usuarios': Usuario.objects.filter(perfil=2)})

def edit_usuario_view(request):
    usuario, _ = Usuario.objects.get_or_create(user=request.user)
    uf = UserForm(request.POST or None, instance=request.user)
    pf = UserUsuarioForm(request.POST or None, instance=usuario)
    message = None
    if request.method == 'POST' and uf.is_valid() and pf.is_valid():
        uf.save(); pf.save(); message={'type':'success','text':'Dados atualizados com sucesso'}
    elif request.method == 'POST': message={'type':'danger','text':'Dados inválidos'}
    return render(request, 'usuario/usuario-edit.html', {'userForm':uf,'usuarioForm':pf,'message':message})
