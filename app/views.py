# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm, CustomUserCreationForm, ProblemaForm, ComentarioForm
from django.contrib import messages

# View para a página inicial
def lista_ideias(request):
    # ... (código da view lista_ideias)
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

# View para detalhes da ideia
def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    comentarios = ideia.comentarios.all().order_by('data_criacao')
    
    # Lógica para o formulário de novo comentário
    if request.method == 'POST':
        # Apenas usuários logados podem comentar
        if not request.user.is_authenticated:
            return redirect('app:login') # Redireciona para o login se não estiver logado

        comment_form = ComentarioForm(request.POST)
        if comment_form.is_valid():
            # Cria o objeto de comentário mas não salva no banco ainda
            novo_comentario = comment_form.save(commit=False)
            # Define o autor como o usuário logado
            novo_comentario.autor = request.user
            # Define a ideia como a ideia da página atual
            novo_comentario.ideia = ideia
            # Agora salva o comentário completo no banco de dados
            novo_comentario.save()
            # Redireciona para a mesma página para ver o novo comentário
            return redirect('app:detalhe_ideia', ideia_id=ideia.id)
    else:
        # Se não for POST, apenas cria um formulário em branco
        comment_form = ComentarioForm()

    contexto = {
        'ideia': ideia,
        'comentarios': comentarios,
        'comment_form': comment_form, # Passa o formulário para o template
    }
    return render(request, 'detalhe_ideia.html', contexto)

# View para submeter ideia
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
        form = IdeiaForm()
    contexto = {
        'form': form
    }
    return render(request, 'submeter_ideia.html', contexto)

# View para votar
@login_required
def votar_ideia(request, ideia_id, tipo_voto):
    # ... (código da view votar_ideia)
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

# View para cadastro de usuário
def cadastro(request):
    # ... (código da view cadastro)
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

# --- VIEWS PARA PROBLEMAS ---

def lista_problemas(request):
    problemas = Problema.objects.all().order_by('-id')
    contexto = {
        'problemas': problemas,
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
    # Por enquanto, esta view apenas renderiza o template.
    # No futuro, poderíamos adicionar lógicas como "suas ideias", "seus comentários", etc.
    return render(request, 'dashboard.html')

def detalhe_problema(request, problema_id):
    # Pega o objeto do problema específico, ou mostra um erro 404 se não existir.
    problema = get_object_or_404(Problema, pk=problema_id)

    # Pega todas as ideias associadas a este problema.
    # Usamos problema.ideia_set.all() para acessar a relação reversa.
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
        # adiciona o usuário ao campo ManyToMany
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