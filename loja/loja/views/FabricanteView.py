from django.shortcuts import render, redirect, get_object_or_404
from loja.models import Fabricante
from loja.forms.FabricanteForm import FabricanteForm

def fabricante_view(request, id=None):
    obj = get_object_or_404(Fabricante, id=id) if id else None
    form = FabricanteForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid(): form.save(); return redirect('fabricante')
    return render(request, 'fabricante/fabricante.html', {'fabricantes': Fabricante.objects.all(), 'form': form, 'editando': id})

def delete_fabricante_view(request, id):
    if request.method == 'POST': get_object_or_404(Fabricante, id=id).delete()
    return redirect('fabricante')
