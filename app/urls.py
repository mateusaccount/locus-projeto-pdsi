from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'

urlpatterns = [
    # ==============================================================================
    # CORE & DASHBOARD
    # ==============================================================================
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'), # Rota alternativa

    # ==============================================================================
    # AUTENTICAÇÃO E CONTA
    # ==============================================================================
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
    
    # Perfil do Usuário
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),

    # Recuperação de Senha (Fluxo Completo)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        success_url=reverse_lazy('app:password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url=reverse_lazy('app:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # ==============================================================================
    # MÓDULO: IDEIAS
    # ==============================================================================
    path('ideias/', views.lista_ideias, name='lista_ideias'),
    path('ideia/<int:ideia_id>/', views.detalhe_ideia, name='detalhe_ideia'),
    path('submeter/', views.submeter_ideia, name='submeter_ideia'),
    
    # Interações (Voto, Comentário, Report)
    path('ideia/<int:ideia_id>/votar/<str:tipo_voto>/', views.votar_ideia, name='votar_ideia'),
    path('ideia/<int:ideia_id>/comentar-ajax/', views.adicionar_comentario_ajax, name='adicionar_comentario_ajax'),
    path('ideia/<int:ideia_id>/reportar/', views.reportar_ideia, name='reportar_ideia'),

    # ==============================================================================
    # MÓDULO: PROBLEMAS
    # ==============================================================================
    path('problemas/', views.lista_problemas, name='lista_problemas'),
    path('problemas/<int:problema_id>/', views.detalhe_problema, name='detalhe_problema'),
    path('problemas/relatar/', views.relatar_problema, name='relatar_problema'),
    path('problemas/<int:problema_id>/reportar/', views.reportar_problema, name='reportar_problema'),

    # ==============================================================================
    # PESQUISA & API
    # ==============================================================================
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('api/live-search/', views.api_live_search, name='api_live_search'),
    path('api/pesquisa/', views.api_pesquisa, name='api_pesquisa'),

    # ==============================================================================
    # ÁREA ADMINISTRATIVA (GESTÃO)
    # ==============================================================================
    path('gestao-interna/', views.painel_admin, name='painel_admin'),
    path('gestao-interna/lista/<str:categoria>/', views.admin_lista, name='admin_lista'),
    path('gestao-interna/delete/<str:tipo>/<int:id_item>/', views.admin_delete, name='admin_delete'),
]