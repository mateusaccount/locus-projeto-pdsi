from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'

urlpatterns = [
    # Rotas do App
    path('', views.dashboard, name='dashboard'),
    path('ideias/', views.lista_ideias, name='lista_ideias'),
    path('ideia/<int:ideia_id>/', views.detalhe_ideia, name='detalhe_ideia'),
    path('submeter/', views.submeter_ideia, name='submeter_ideia'),
    path('ideia/<int:ideia_id>/votar/<str:tipo_voto>/', views.votar_ideia, name='votar_ideia'),

    # Rotas de Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),

    # --- ROTAS DE PROBLEMAS ---
    path('problemas/', views.lista_problemas, name='lista_problemas'),
    path('problemas/relatar/', views.relatar_problema, name='relatar_problema'),

    # --- ROTA DO DASHBOARD ---
    path('dashboard/', views.dashboard, name='dashboard'),

     # --- ROTA DE DETALHES DO PROBLEMA ---
    path('problemas/<int:problema_id>/', views.detalhe_problema, name='detalhe_problema'),

    # --- ROTA DE REPORT DE IDEIA ---
    path('ideia/<int:ideia_id>/reportar/', views.reportar_ideia, name='reportar_ideia'),
    path('submeter/', views.submeter_ideia, name='submeter_ideia'),
    
    # --- ROTA DE REPORT DE PROBLEMA ---
    path('problemas/<int:problema_id>/reportar/', views.reportar_problema, name='reportar_problema'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('pesquisa/', views.pesquisa, name='pesquisa'),
    path('api/pesquisa/', views.api_pesquisa, name='api_pesquisa'),

    # --- ROTAS DE RECUPERAÇÃO DE SENHA ATUALIZADAS ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/recuperacao_senha_form.html',
        email_template_name='registration/recuperacao_senha_email.html',
        subject_template_name='registration/recuperacao_senha_assunto.txt',
        success_url=reverse_lazy('app:password_reset_done')
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/recuperacao_senha_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/recuperacao_senha_confirmada.html',
        success_url=reverse_lazy('app:password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/recuperacao_senha_completa.html'
    ), name='password_reset_complete'),

    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
]