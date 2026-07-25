from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Categoria
from loja.forms.CategoriaForm import CategoriaForm

def categoria_view(request, id=None):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=get_object_or_404(Categoria, id=request.POST.get('id')) if request.POST.get('id') else None)
        if form.is_valid(): form.save(); return redirect('categoria')
    form = CategoriaForm(instance=get_object_or_404(Categoria, id=id) if id else None)
    return render(request, 'categoria/categoria.html', {'categorias': Categoria.objects.all(), 'form': form, 'editando': id})

def delete_categoria_view(request, id):
    if request.method == 'POST': get_object_or_404(Categoria, id=id).delete()
    return redirect('categoria')
