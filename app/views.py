from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Count, Q, F
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from .models import Ideia, Comentario, Votacao, Problema, CustomUsuario
from .forms import IdeiaForm, ProblemaForm, EditarPerfilForm, CadastroForm

# ==============================================================================
# AUTENTICAÇÃO E PERFIL
# ==============================================================================

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('app:dashboard')
    else:
        form = CadastroForm()
    
    return render(request, 'registration/cadastro.html', {'form': form})

@login_required
def perfil_usuario(request):
    ideias = Ideia.objects.filter(autor=request.user).order_by('-data_criacao')
    problemas = Problema.objects.filter(autor=request.user).order_by('-data_criacao')

    total_atividades = ideias.count() + problemas.count()
    
    meta_engajamento = 10 
    porcentagem = int((total_atividades / meta_engajamento) * 100)
    porcentagem = min(porcentagem, 100)
    
    nivel = "Iniciante"
    if porcentagem >= 30: nivel = "Participativo"
    if porcentagem >= 70: nivel = "Veterano"
    if porcentagem >= 100: nivel = "Líder Comunitário"

    context = {
        'minhas_ideias': ideias,
        'meus_problemas': problemas,
        'total_ideias': ideias.count(),
        'total_problemas': problemas.count(),
        'porcentagem_engajamento': porcentagem,
        'nivel_engajamento': nivel,
    }
    return render(request, 'usuarios/perfil.html', context)

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('app:perfil')
        else:
            print("ERRO AO SALVAR PERFIL:", form.errors) 
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'usuarios/editar.html', {'form': form})
# ==============================================================================
# CORE & DASHBOARD
# ==============================================================================

@login_required
def dashboard(request):
    problemas_recentes = Problema.objects.order_by('-data_criacao')[:5]
    
    todas_ideias = Ideia.objects.all()
    ideias_destaque = sorted(todas_ideias, key=lambda i: i.pontuacao, reverse=True)[:4]

    return render(request, 'dashboard.html', {
        'problemas_carousel': problemas_recentes,
        'ideias_destaque': ideias_destaque
    })

def pesquisa(request):
    query = request.GET.get('q', '')
    ideias = []
    problemas = []
    total = 0

    if query:
        ideias = Ideia.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        ).order_by('-data_criacao')
        
        problemas = Problema.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query) | Q(localizacao__icontains=query)
        ).order_by('-data_criacao')

        total = len(ideias) + len(problemas)

    return render(request, 'pesquisa.html', {
        'query': query,
        'ideias': ideias,
        'problemas': problemas,
        'total_resultados': total
    })

def api_live_search(request):
    query = request.GET.get('q', '')
    results = []

    if len(query) > 1:
        ideias = Ideia.objects.filter(titulo__icontains=query)[:5]
        for item in ideias:
            results.append({
                'titulo': item.titulo,
                'tipo': 'Ideia',
                'url': reverse('app:detalhe_ideia', args=[item.id]),
                'cor': 'text-green-600 bg-green-50 border-green-200'
            })

        problemas = Problema.objects.filter(titulo__icontains=query)[:5]
        for item in problemas:
            results.append({
                'titulo': item.titulo,
                'tipo': 'Problema',
                'url': reverse('app:detalhe_problema', args=[item.id]),
                'cor': 'text-red-600 bg-red-50 border-red-200'
            })

    return JsonResponse({'results': results})

def api_pesquisa(request):
    query = request.GET.get('q', '')
    resultados = []

    if query:
        ideias = Ideia.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query),
            status='aprovada'
        )[:5]
        problemas = Problema.objects.filter(
            Q(titulo__icontains=query) | Q(descricao__icontains=query)
        )[:5]
        
        for item in ideias:
            resultados.append({'titulo': item.titulo, 'tipo': 'Ideia', 'url': f'/ideia/{item.id}/'})
        for item in problemas:
            resultados.append({'titulo': item.titulo, 'tipo': 'Problema', 'url': f'/problemas/{item.id}/'})
            
    return JsonResponse(resultados, safe=False)

# ==============================================================================
# MÓDULO: IDEIAS
# ==============================================================================

def lista_ideias(request):
    filtro = request.GET.get('filtro', 'recentes')
    
    queryset = Ideia.objects.annotate(
        ups=Count('votos', filter=Q(votos__tipo='upvote')),
        downs=Count('votos', filter=Q(votos__tipo='downvote'))
    ).annotate(
        saldo=F('ups') - F('downs')
    )

    if filtro == 'populares':
        queryset = queryset.order_by('-saldo', '-data_criacao')
    else:
        queryset = queryset.order_by('-data_criacao')

    return render(request, 'ideias/lista.html', {
        'ideias': queryset,
        'filtro_atual': filtro
    })

def detalhe_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, id=ideia_id)
    comentarios = Comentario.objects.filter(ideia=ideia).order_by('-data_criacao')
    
    voto_usuario = None
    if request.user.is_authenticated:
        voto = Votacao.objects.filter(ideia=ideia, usuario=request.user).first()
        if voto:
            voto_usuario = voto.tipo

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('app:login')
        
        if request.POST.get('tipo_acao') == 'comentar':
            texto = request.POST.get('texto_comentario')
            if texto:
                Comentario.objects.create(ideia=ideia, autor=request.user, texto=texto)
                messages.success(request, 'Comentário enviado!')
                return redirect('app:detalhe_ideia', ideia_id=ideia.id)

    return render(request, 'ideias/detalhe.html', {
        'ideia': ideia,
        'comentarios': comentarios,
        'voto_usuario': voto_usuario,
    })

@login_required
def submeter_ideia(request):
    if request.method == 'POST':
        form = IdeiaForm(request.POST, request.FILES)
        if form.is_valid():
            nova = form.save(commit=False)
            nova.autor = request.user
            nova.status = 'aprovada'
            nova.save()
            return redirect('app:detalhe_ideia', ideia_id=nova.id)
    else:
        initial_data = {}
        if request.GET.get('problema'):
            initial_data['problema_alvo'] = request.GET.get('problema')
        form = IdeiaForm(initial=initial_data)
        
    return render(request, 'ideias/form.html', {'form': form})

@login_required
def reportar_ideia(request, ideia_id):
    ideia = get_object_or_404(Ideia, pk=ideia_id)
    if request.method == 'POST':
        ideia.usuarios_que_reportaram.add(request.user)
        messages.success(request, 'Denúncia recebida. Agradecemos sua colaboração!')
    return redirect('app:detalhe_ideia', ideia_id=ideia.id)

# ==============================================================================
# MÓDULO: PROBLEMAS
# ==============================================================================

def lista_problemas(request):
    area_selecionada = request.GET.get('area')
    problemas = Problema.objects.all().order_by('-data_criacao')
    
    if area_selecionada:
        problemas = problemas.filter(area=area_selecionada)
        
    return render(request, 'problemas/lista.html', {
        'problemas': problemas,
        'areas': Problema.AREA_CHOICES,
        'area_selecionada': area_selecionada,
    })

def detalhe_problema(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)

    ideias_relacionadas = problema.ideia_set.filter(status='aprovada').annotate(
        saldo=Count('votos', filter=Q(votos__tipo='upvote')) - Count('votos', filter=Q(votos__tipo='downvote'))
    ).order_by('-saldo')

    return render(request, 'problemas/detalhe.html', {
        'problema': problema,
        'ideias': ideias_relacionadas,
    })

@login_required
def relatar_problema(request):
    if request.method == 'POST':
        form = ProblemaForm(request.POST, request.FILES)
        if form.is_valid():
            novo = form.save(commit=False)
            novo.autor = request.user
            novo.save()
            return redirect('app:lista_problemas')
    else:
        form = ProblemaForm()
    
    return render(request, 'problemas/form.html', {'form': form})

@login_required
def reportar_problema(request, problema_id):
    problema = get_object_or_404(Problema, pk=problema_id)
    if request.method == 'POST':
        problema.usuarios_que_reportaram.add(request.user)
        messages.success(request, 'Denúncia recebida.')
    return redirect('app:detalhe_problema', problema_id=problema.id)

# ==============================================================================
# INTERAÇÕES (API/AJAX)
# ==============================================================================

@login_required
def votar_ideia(request, ideia_id, tipo_voto):
    if request.method == 'POST':
        ideia = get_object_or_404(Ideia, id=ideia_id)
        tipo_modelo = 'upvote' if tipo_voto == 'cima' else 'downvote'
        
        voto_existente = Votacao.objects.filter(usuario=request.user, ideia=ideia).first()
        
        if voto_existente:
            if voto_existente.tipo == tipo_modelo:
                voto_existente.delete()
                estado_atual = 'nenhum'
            else:
                voto_existente.tipo = tipo_modelo
                voto_existente.save()
                estado_atual = tipo_modelo
        else:
            Votacao.objects.create(usuario=request.user, ideia=ideia, tipo=tipo_modelo)
            estado_atual = tipo_modelo
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'total_upvotes': ideia.total_upvotes,
                'total_downvotes': ideia.total_downvotes,
                'voto_usuario': estado_atual,
                'status': 'ok'
            })
            
    return redirect('app:detalhe_ideia', ideia_id=ideia_id)

@login_required
def adicionar_comentario_ajax(request, ideia_id):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        ideia = get_object_or_404(Ideia, id=ideia_id)
        texto = request.POST.get('texto_comentario')
        
        if texto:
            comentario = Comentario.objects.create(
                ideia=ideia,
                autor=request.user,
                texto=texto
            )
            return JsonResponse({
                'status': 'ok',
                'autor_nome': request.user.first_name or request.user.username,
                'autor_inicial': request.user.username[0].upper(),
                'texto': comentario.texto,
                'data': 'Agora mesmo',
                'total_comentarios': ideia.comentarios.count()
            })
            
    return JsonResponse({'status': 'erro'}, status=400)

# ==============================================================================
# ÁREA ADMINISTRATIVA (GESTÃO)
# ==============================================================================

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def painel_admin(request):
    ctx = {
        'total_users': CustomUsuario.objects.count(),
        'total_ideias': Ideia.objects.count(),
        'total_problemas': Problema.objects.count(),
        'total_comentarios': Comentario.objects.count(),
        'ultimos_usuarios': CustomUsuario.objects.order_by('-date_joined')[:5],
        'ultimas_ideias': Ideia.objects.order_by('-data_criacao')[:5],
        'ultimos_problemas': Problema.objects.order_by('-data_criacao')[:5],
    }
    return render(request, 'gestao/painel.html', ctx)

@login_required
@user_passes_test(is_superuser)
def admin_lista(request, categoria):
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
    
    return render(request, 'gestao/lista.html', {
        'items': items,
        'categoria': categoria,
        'titulo': titulo
    })

@login_required
@user_passes_test(is_superuser)
def admin_delete(request, tipo, id_item):
    model_map = {
        'usuario': CustomUsuario,
        'ideia': Ideia,
        'problema': Problema,
        'comentario': Comentario
    }
    
    if tipo in model_map:
        item = get_object_or_404(model_map[tipo], id=id_item)
        item.delete()
        messages.success(request, 'Item removido com sucesso.')
    
    return redirect(request.META.get('HTTP_REFERER', 'app:painel_admin'))