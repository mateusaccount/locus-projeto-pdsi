# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm

# View para a página inicial que lista as ideias aprovadas
def lista_ideias(request):
    ideias_aprovadas = Ideia.objects.filter(status='aprovada').order_by('-data_criacao')
    contexto = {
        'ideias': ideias_aprovadas
    }
    return render(request, 'app/lista_ideias.html', contexto)

# View para a página de detalhes de uma ideia específica
def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    comentarios = ideia.comentarios.all().order_by('data_criacao')
    contexto = {
        'ideia': ideia,
        'comentarios': comentarios,
    }
    return render(request, 'app/detalhe_ideia.html', contexto)

# View para a página de submissão de uma nova ideia (requer login)
@login_required
def submeter_ideia(request):
    if request.method == 'POST':
        form = IdeiaForm(request.POST)
        if form.is_valid():
            nova_ideia = form.save(commit=False)
            nova_ideia.autor = request.user
            nova_ideia.save()
            return redirect('app:detalhe_ideia', ideia_id=nova_ideia.id)
    else:
        form = IdeiaForm()
    contexto = {
        'form': form
    }
    return render(request, 'app/submeter_ideia.html', contexto)

# View para processar um voto em uma ideia (requer login)
@login_required
def votar_ideia(request, ideia_id, tipo_voto):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    usuario = request.user
    voto_existente, criado = Votacao.objects.get_or_create(
        ideia=ideia,
        usuario=usuario,
        defaults={'tipo': tipo_voto}
    )
    if not criado:
        if voto_existente.tipo == tipo_voto:
            voto_existente.delete()
        else:
            voto_existente.tipo = tipo_voto
            voto_existente.save()
    return redirect('app:detalhe_ideia', ideia_id=ideia.id)