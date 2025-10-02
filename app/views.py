from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm, CustomUserCreationForm

def lista_ideias(request):
    ideias_destaque = Ideia.objects.filter(status='aprovada').annotate(
        pontuacao=Count('votos', filter=Q(votos__tipo='upvote')) - Count('votos', filter=Q(votos__tipo='downvote'))
    ).order_by('-pontuacao')[:3]

    area_selecionada = request.GET.get('area')
    ideias_aprovadas = Ideia.objects.filter(status='aprovada')
    if area_selecionada:
        ideias_aprovadas = ideias_aprovadas.filter(problema_alvo__area=area_selecionada)
    ideias_aprovadas = ideias_aprovadas.order_by('-data_criacao')
    
    areas_disponiveis = Problema.AREA_CHOICES

    contexto = {
        'ideias_destaque': ideias_destaque,
        'ideias': ideias_aprovadas,
        'areas': areas_disponiveis,
        'area_selecionada': area_selecionada,
    }
    # Correção: Removido 'app/' do caminho do template
    return render(request, 'lista_ideias.html', contexto)

def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    comentarios = ideia.comentarios.all().order_by('data_criacao')
    contexto = {
        'ideia': ideia,
        'comentarios': comentarios,
    }
    # Correção: Removido 'app/' do caminho do template
    return render(request, 'detalhe_ideia.html', contexto)

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
    # Correção: Removido 'app/' do caminho do template
    return render(request, 'submeter_ideia.html', contexto)

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

def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:lista_ideias')
    else:
        form = CustomUserCreationForm()
    
    contexto = {'form': form}
    # Correção: Removido 'app/' do caminho do template
    return render(request, 'registration/cadastro.html', contexto)