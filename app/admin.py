# app/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario, Problema, Ideia, Comentario, Votacao

# --- Customizando a exibição do nosso Usuário ---

# Para que o nosso campo "tipo" e "curso_departamento" apareçam no admin,
# precisamos customizar a classe que gerencia o usuário.
class CustomUserAdmin(UserAdmin):
    # Adiciona os novos campos ao formulário de criação de usuário
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo', 'curso_departamento')}),
    )
    # Adiciona os novos campos ao formulário de edição de usuário
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo', 'curso_departamento')}),
    )
    # Adiciona os campos à lista de exibição de usuários
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo')


# --- Customizando a exibição das Ideias ---

class IdeiaAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista de ideias
    list_display = ('titulo', 'autor', 'status', 'data_criacao', 'problema_alvo')
    # Adiciona um filtro na lateral direita para facilitar a busca por status
    list_filter = ('status', 'data_criacao')
    # Adiciona uma barra de pesquisa
    search_fields = ('titulo', 'descricao', 'autor__username')
    # Define a ordem padrão de exibição (as mais novas primeiro)
    ordering = ('-data_criacao',)


# --- Registrando os models ---

# admin.site.register() é a função que "ativa" o model no painel de admin.
admin.site.register(CustomUsuario, CustomUserAdmin)
admin.site.register(Problema)
admin.site.register(Ideia, IdeiaAdmin) # Usamos a classe customizada aqui
admin.site.register(Comentario)
admin.site.register(Votacao)