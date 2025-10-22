# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm, CustomUserCreationForm, ProblemaForm, ComentarioForm
from django.contrib import messages


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
    return render(request, 'lista_ideias.html', contexto)

def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    comentarios = ideia.comentarios.all().order_by('data_criacao')
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('app:login')

        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            novo_comentario = comment_form.save(commit=False)
            novo_comentario.autor = request.user
            novo_comentario.ideia = ideia
            novo_comentario.save()
            return redirect('app:detalhe_ideia', ideia_id=ideia.id)
    else:
        comment_form = ComentarioForm()

    contexto = {
        'ideia': ideia,
        'comentarios': comentarios,
        'comment_form': comment_form,
    }
    return render(request, 'detalhe_ideia.html', contexto)

@login_required
def submeter_ideia(request):
    if request.method == 'POST':
        form = IdeiaForm(request.POST)
        if form.is_valid():
            nova_ideia = form.save(commit=False)
            nova_ideia.autor = request.user
            nova_ideia.status = 'aprovada'
            nova_ideia.save()
            return redirect('app:detalhe_ideia', ideia_id=nova_ideia.id)
    else:
        problema_id_inicial = request.GET.get('problema')
        initial_data = {}
        if problema_id_inicial:
            initial_data['problema_alvo'] = problema_id_inicial
        form = IdeiaForm(initial=initial_data)
        
    contexto = {
        'form': form
    }
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
            return redirect('app:dashboard')
    else:
        form = CustomUserCreationForm()
    
    contexto = {'form': form}
    return render(request, 'registration/cadastro.html', contexto)

def lista_problemas(request):
    area_selecionada = request.GET.get('area')
    problemas_list = Problema.objects.all()
    if area_selecionada:
        problemas_list = problemas_list.filter(area=area_selecionada)
    problemas_list = problemas_list.order_by('-id')
    areas_disponiveis = Problema.AREA_CHOICES
    contexto = {
        'problemas': problemas_list,
        'areas': areas_disponiveis,
        'area_selecionada': area_selecionada,
    }
    return render(request, 'lista_problemas.html', contexto)

@login_required
def relatar_problema(request):
    if request.method == 'POST':
        form = ProblemaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:lista_problemas')
    else:
        form = ProblemaForm()
    
    contexto = {
        'form': form
    }
    return render(request, 'relatar_problema.html', contexto)

@login_required
def dashboard(request):
    ideias_destaque = Ideia.objects.filter(status='aprovada').annotate(
        pontuacao=Count('votos', filter=Q(votos__tipo='upvote')) - Count('votos', filter=Q(votos__tipo='downvote'))
    ).order_by('-pontuacao')[:3]

    problemas_carousel = Problema.objects.all().order_by('-id')[:5]

    contexto = {
        'ideias_destaque': ideias_destaque,
        'problemas_carousel': problemas_carousel,
    }
    return render(request, 'dashboard.html', contexto)

def detalhe_problema(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)
    ideias_relacionadas = problema.ideia_set.filter(status='aprovada').annotate(
        pontuacao=Count('votos', filter=Q(votos__tipo='upvote')) - Count('votos', filter=Q(votos__tipo='downvote'))
    ).order_by('-pontuacao')

    contexto = {
        'problema': problema,
        'ideias': ideias_relacionadas,
    }
    return render(request, 'detalhe_problema.html', contexto)

@login_required
def reportar_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    if request.method == 'POST':
        ideia.usuarios_que_reportaram.add(request.user)
        messages.success(request, 'Denúncia recebida. Agradecemos sua colaboração!')
        return redirect('app:detalhe_ideia', ideia_id=ideia.id)
    return redirect('app:detalhe_ideia', ideia_id=ideia.id)
    
@login_required
def reportar_problema(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)
    if request.method == 'POST':
        problema.usuarios_que_reportaram.add(request.user)
        messages.success(request, 'Denúncia recebida. Agradecemos sua colaboração!')
        return redirect('app:detalhe_problema', problema_id=problema.id)
    return redirect('app:detalhe_problema', problema_id=problema.id)