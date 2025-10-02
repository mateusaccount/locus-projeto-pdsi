# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm

def lista_ideias(request):
    # --- 1. LÓGICA PARA AS IDEIAS EM DESTAQUE ---
    
    # Explicando a consulta:
    # .annotate() é uma função poderosa que adiciona um novo "campo calculado" a cada
    # objeto do resultado da consulta.
    # Estamos criando um campo chamado 'pontuacao'.
    # O valor de 'pontuacao' será: a contagem de votos (Count) que são do tipo 'upvote'
    # MENOS a contagem de votos que são do tipo 'downvote'.
    # O objeto Q() nos ajuda a criar essa condição de contagem.
    ideias_destaque = Ideia.objects.filter(status='aprovada').annotate(
        pontuacao=Count('votos', filter=Q(votos__tipo='upvote')) - Count('votos', filter=Q(votos__tipo='downvote'))
    ).order_by('-pontuacao')[:3] # Ordenamos pela maior pontuação e pegamos os 3 primeiros.

    # --- 2. LÓGICA PRINCIPAL DA LISTA (com filtros, como já tínhamos) ---
    area_selecionada = request.GET.get('area')
    ideias_aprovadas = Ideia.objects.filter(status='aprovada')
    if area_selecionada:
        ideias_aprovadas = ideias_aprovadas.filter(problema_alvo__area=area_selecionada)
    ideias_aprovadas = ideias_aprovadas.order_by('-data_criacao')
    
    areas_disponiveis = Problema.AREA_CHOICES

    contexto = {
        'ideias_destaque': ideias_destaque, # Enviamos a nova lista para o template
        'ideias': ideias_aprovadas,
        'areas': areas_disponiveis,
        'area_selecionada': area_selecionada,
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

