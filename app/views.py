# app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Count, Q, F
from .models import Ideia, Comentario, Votacao, Problema, CustomUsuario
from .forms import IdeiaForm, CustomUserCreationForm, ProblemaForm, ComentarioForm, EditarPerfilForm, CadastroForm
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse


def lista_ideias(request):
    filtro = request.GET.get('filtro', 'recentes')
    
    # 1. Cria a consulta base "ensinando" o banco a contar votos
    # annotate cria campos virtuais 'ups', 'downs' e 'saldo' direto na query
    ideias_list = Ideia.objects.annotate(
        ups=Count('votos', filter=Q(votos__tipo='upvote')),
        downs=Count('votos', filter=Q(votos__tipo='downvote'))
    ).annotate(
        saldo=F('ups') - F('downs')
    )

    # 2. Aplica a ordenação baseada no filtro
    if filtro == 'populares':
        # Ordena pelo saldo (maior para menor)
        ideias_list = ideias_list.order_by('-saldo', '-data_criacao')
    else:
        # Ordena por data (padrão)
        ideias_list = ideias_list.order_by('-data_criacao')

    return render(request, 'lista_ideias.html', {
        'ideias': ideias_list,
        'filtro_atual': filtro # Passamos para o template saber qual botão pintar
    })

def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, id=ideia_id)
    comentarios = Comentario.objects.filter(ideia=ideia).order_by('-data_criacao')
    
    # Verifica se o usuário logado já votou nessa ideia
    voto_usuario = None
    if request.user.is_authenticated:
        # Tenta pegar o voto do usuário nesta ideia
        voto = Votacao.objects.filter(ideia=ideia, usuario=request.user).first()
        if voto:
            voto_usuario = voto.tipo # Vai ser 'upvote' ou 'downvote'

    # Lógica de Salvar Comentário (Mantida igual)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('app:login')
        
        tipo_acao = request.POST.get('tipo_acao')
        if tipo_acao == 'comentar':
            texto_recebido = request.POST.get('texto_comentario')
            if texto_recebido:
                Comentario.objects.create(ideia=ideia, autor=request.user, texto=texto_recebido)
                messages.success(request, 'Comentário enviado!')
                return redirect('app:detalhe_ideia', ideia_id=ideia.id)

    return render(request, 'detalhe_ideia.html', {
        'ideia': ideia,
        'comentarios': comentarios,
        'voto_usuario': voto_usuario, # Passamos essa informação nova para o template
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
        
        # Converte o parametro da URL para o valor do banco
        tipo_modelo = 'upvote' if tipo_voto == 'cima' else 'downvote'
        
        # Busca voto existente
        voto_existente = Votacao.objects.filter(usuario=request.user, ideia=ideia).first()
        
        if voto_existente:
            if voto_existente.tipo == tipo_modelo:
                # Se clicou no MESMO botão que já tinha votado -> Remove o voto (Toggle)
                voto_existente.delete()
            else:
                # Se clicou no OUTRO botão -> Atualiza o voto (Switch)
                voto_existente.tipo = tipo_modelo
                voto_existente.save()
        else:
            # Se não tinha voto -> Cria novo
            Votacao.objects.create(usuario=request.user, ideia=ideia, tipo=tipo_modelo)
        
        # Não precisamos salvar ideia.pontuacao aqui pois ela é calculada automaticamente (@property)
        
    # Redireciona de volta para a ideia (com âncora para não rolar a página pro topo, opcional)
    return redirect('app:detalhe_ideia', ideia_id=ideia_id)

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Faz o login automático após o cadastro (opcional, mas recomendado)
            login(request, user)
            return redirect('app:dashboard') # Ou 'app:lista_ideias' se preferir
    else:
        form = CadastroForm()
    
    return render(request, 'registration/cadastro.html', {'form': form})

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
    ideias = []
    problemas = []
    total_resultados = 0

    if query:
        # Busca em Ideias (Título ou Descrição)
        ideias = Ideia.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        ).order_by('-data_criacao')
        
        # Busca em Problemas (Título, Descrição ou Localização)
        problemas = Problema.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(localizacao__icontains=query)
        ).order_by('-data_criacao')

        total_resultados = len(ideias) + len(problemas)

    return render(request, 'pesquisa.html', {
        'query': query,
        'ideias': ideias,
        'problemas': problemas,
        'total_resultados': total_resultados
    })

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

def api_live_search(request):
    query = request.GET.get('q', '')
    results = []

    if len(query) > 1:
        ideias = Ideia.objects.filter(titulo__icontains=query)[:5]
        for ideia in ideias:
            results.append({
                'titulo': ideia.titulo,
                'tipo': 'Ideia',
                'url': reverse('app:detalhe_ideia', args=[ideia.id]),
                'cor': 'text-green-600 bg-green-50 border-green-200'
            })

        problemas = Problema.objects.filter(titulo__icontains=query)[:5]
        for problema in problemas:
            results.append({
                'titulo': problema.titulo,
                'tipo': 'Problema',
                'url': reverse('app:detalhe_problema', args=[problema.id]),
                'cor': 'text-red-600 bg-red-50 border-red-200'
            })

    return JsonResponse({'results': results})

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def painel_admin(request):
    # Estatísticas Gerais
    total_users = CustomUsuario.objects.count()
    total_ideias = Ideia.objects.count()
    total_problemas = Problema.objects.count()
    total_comentarios = Comentario.objects.count()

    # Listas Recentes (para o Dashboard Admin)
    ultimos_usuarios = CustomUsuario.objects.order_by('-date_joined')[:5]
    ultimas_ideias = Ideia.objects.order_by('-data_criacao')[:5]
    ultimos_problemas = Problema.objects.order_by('-data_criacao')[:5]

    return render(request, 'painel_admin.html', {
        'total_users': total_users,
        'total_ideias': total_ideias,
        'total_problemas': total_problemas,
        'total_comentarios': total_comentarios,
        'ultimos_usuarios': ultimos_usuarios,
        'ultimas_ideias': ultimas_ideias,
        'ultimos_problemas': ultimos_problemas,
    })

@login_required
@user_passes_test(is_superuser)
def admin_lista(request, categoria):
    # Gerencia as listas completas (clicando na Sidebar)
    items = []
    titulo = ""
    
    if categoria == 'ideias':
        items = Ideia.objects.all().order_by('-data_criacao')
        titulo = "Gerenciar Ideias"
    elif categoria == 'problemas':
        items = Problema.objects.all().order_by('-data_criacao')
        titulo = "Gerenciar Problemas"
    elif categoria == 'usuarios':
        items = CustomUsuario.objects.all().order_by('-date_joined')
        titulo = "Gerenciar Usuários"
    elif categoria == 'comentarios':
        items = Comentario.objects.all().order_by('-data_criacao')
        titulo = "Gerenciar Comentários"
    
    return render(request, 'admin_lista.html', {
        'items': items,
        'categoria': categoria,
        'titulo': titulo
    })

@login_required
@user_passes_test(is_superuser)
def admin_delete(request, tipo, id_item):
    # Função genérica para deletar itens
    if tipo == 'usuario':
        item = get_object_or_404(CustomUsuario, id=id_item)
    elif tipo == 'ideia':
        item = get_object_or_404(Ideia, id=id_item)
    elif tipo == 'problema':
        item = get_object_or_404(Problema, id=id_item)
    elif tipo == 'comentario':
        item = get_object_or_404(Comentario, id=id_item)
    
    item.delete()
    messages.success(request, 'Item removido com sucesso.')
    
    # Tenta voltar para a página anterior, se não der, vai pro painel
    return redirect(request.META.get('HTTP_REFERER', 'app:painel_admin'))