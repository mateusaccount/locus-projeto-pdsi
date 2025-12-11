# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Count, Q
from .models import Ideia, Comentario, Votacao, Problema
from .forms import IdeiaForm, CustomUserCreationForm, ProblemaForm, ComentarioForm, EditarPerfilForm
from django.contrib import messages
from django.http import JsonResponse


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
    # 1. Busca a ideia ou dá erro 404 se não existir
    ideia = get_object_or_404(Ideia, id=ideia_id)
    
    # 2. Processamento do Formulário de Comentário (POST)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('app:login')
            
        # Verifica se a ação é realmente comentar (pelo input hidden do HTML)
        tipo_acao = request.POST.get('tipo_acao')
        
        if tipo_acao == 'comentar':
            texto_recebido = request.POST.get('texto_comentario')
            
            if texto_recebido:
                # Cria e salva o comentário no banco
                Comentario.objects.create(
                    ideia=ideia,
                    autor=request.user,
                    texto=texto_recebido  # Certifique-se que no models.py o campo é 'texto'
                )
                messages.success(request, 'Comentário enviado com sucesso!')
                # Recarrega a página para mostrar o novo comentário
                return redirect('app:detalhe_ideia', ideia_id=ideia.id)

    # 3. Busca os comentários para exibir (ATENÇÃO AQUI)
    # Buscamos todos os comentários ligados a esta ideia, ordenados do mais novo para o mais antigo
    lista_comentarios = Comentario.objects.filter(ideia=ideia).order_by('-data_criacao')

    # 4. Renderiza o template passando os dados
    return render(request, 'detalhe_ideia.html', {
        'ideia': ideia,
        'comentarios': lista_comentarios, # Essa chave 'comentarios' deve ser igual ao usado no {% for %} do HTML
    })

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
    if request.method == 'POST':
        ideia = get_object_or_404(Ideia, id=ideia_id)
        
        # Mapeia 'cima'/'baixo' da URL para 'upvote'/'downvote' do Modelo
        tipo_modelo = 'upvote' if tipo_voto == 'cima' else 'downvote'
        
        # Tenta pegar o voto existente desse usuário nessa ideia
        voto_existente = Votacao.objects.filter(usuario=request.user, ideia=ideia).first()
        
        if voto_existente:
            if voto_existente.tipo == tipo_modelo:
                # Se clicou no mesmo botão, remove o voto (toggle)
                voto_existente.delete()
                messages.info(request, 'Voto removido.')
            else:
                # Se mudou o voto (de cima pra baixo ou vice-versa), atualiza
                voto_existente.tipo = tipo_modelo
                voto_existente.save()
                messages.success(request, 'Voto atualizado!')
        else:
            # Se não existe voto, cria um novo
            Votacao.objects.create(usuario=request.user, ideia=ideia, tipo=tipo_modelo)
            messages.success(request, 'Voto computado!')
        
    return redirect('app:detalhe_ideia', ideia_id=ideia_id)

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
            novo_problema = form.save(commit=False)
            novo_problema.autor = request.user
            novo_problema.save()
            return redirect('app:lista_problemas')
    else:
        form = ProblemaForm()
    
    contexto = {
        'form': form
    }
    return render(request, 'relatar_problema.html', contexto)

@login_required
def dashboard(request):
    problemas_recentes = Problema.objects.order_by('-data_criacao')[:5]
    todas_ideias = Ideia.objects.all()
    ideias_destaque = sorted(todas_ideias, key=lambda i: i.pontuacao, reverse=True)[:4]

    return render(request, 'dashboard.html', {
        'problemas_carousel': problemas_recentes,
        'ideias_destaque': ideias_destaque
    })

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

@login_required
def perfil_usuario(request):
    ideias = Ideia.objects.filter(autor=request.user).order_by('-data_criacao')
    problemas = Problema.objects.filter(autor=request.user).order_by('-data_criacao')

    total_ideias = ideias.count()
    total_problemas = problemas.count()
    total_atividades = total_ideias + total_problemas
    meta_engajamento = 10 
    porcentagem_engajamento = int((total_atividades / meta_engajamento) * 100)
    if porcentagem_engajamento > 100:
        porcentagem_engajamento = 100
    nivel_engajamento = "Iniciante"
    if porcentagem_engajamento >= 30: nivel_engajamento = "Participativo"
    if porcentagem_engajamento >= 70: nivel_engajamento = "Veterano"
    if porcentagem_engajamento >= 100: nivel_engajamento = "Líder Comunitário"

    context = {
        'minhas_ideias': ideias,
        'meus_problemas': problemas,
        'total_ideias': total_ideias,
        'total_problemas': total_problemas,
        'porcentagem_engajamento': porcentagem_engajamento,
        'nivel_engajamento': nivel_engajamento,
    }
    return render(request, 'perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('app:perfil')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'editar_perfil.html', {'form': form})

def pesquisa(request):
    query = request.GET.get('q', '')
    resultados = []
    if query:
        ideias = Ideia.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        ).filter(status='aprovada')
        problemas = Problema.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        )
        for item in ideias:
            resultados.append({'item': item, 'tipo': 'Ideia'})
        
        for item in problemas:
            resultados.append({'item': item, 'tipo': 'Problema'})

    contexto = {
        'query': query,
        'resultados': resultados,
    }
    return render(request, 'pesquisa.html', contexto)

def api_pesquisa(request):
    query = request.GET.get('q', '')
    resultados_finais = []

    if query:
        ideias = Ideia.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query),
            status='aprovada'
        )[:5]
        problemas = Problema.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        )[:5]
        for ideia in ideias:
            resultados_finais.append({
                'titulo': ideia.titulo,
                'tipo': 'Ideia',
                'url': f'/ideia/{ideia.id}/'
            })
        
        for problema in problemas:
            resultados_finais.append({
                'titulo': problema.titulo,
                'tipo': 'Problema',
                'url': f'/problemas/{problema.id}/'
            })
            
    return JsonResponse(resultados_finais, safe=False)