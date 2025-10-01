
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.lista_ideias, name='lista_ideias'),
    path('ideia/<int:ideia_id>/', views.detalhe_ideia, name='detalhe_ideia'),
    path('submeter/', views.submeter_ideia, name='submeter_ideia'),
    path('ideia/<int:ideia_id>/votar/<str:tipo_voto>/', views.votar_ideia, name='votar_ideia'),
]