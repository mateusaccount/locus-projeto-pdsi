from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'app'

urlpatterns = [
    # Rotas do App
    path('', views.lista_ideias, name='lista_ideias'),
    path('ideia/<int:ideia_id>/', views.detalhe_ideia, name='detalhe_ideia'),
    path('submeter/', views.submeter_ideia, name='submeter_ideia'),
    path('ideia/<int:ideia_id>/votar/<str:tipo_voto>/', views.votar_ideia, name='votar_ideia'),

    # Rotas de Autenticação
    # Correção: Removido 'app/' do caminho do template
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
]