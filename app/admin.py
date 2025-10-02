from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario, Problema, Ideia, Comentario, Votacao

class CustomUserAdmin(UserAdmin):
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('tipo', 'curso_departamento')}),
    )
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo', 'curso_departamento')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo')

class IdeiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'data_criacao', 'problema_alvo')
    list_filter = ('status', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'autor__username')
    ordering = ('-data_criacao',)

admin.site.register(CustomUsuario, CustomUserAdmin)
admin.site.register(Problema)
admin.site.register(Ideia, IdeiaAdmin)
admin.site.register(Comentario)
admin.site.register(Votacao)