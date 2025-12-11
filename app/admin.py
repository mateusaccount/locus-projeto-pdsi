from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsuario, Problema, Ideia, Comentario, Votacao

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo')

class ProblemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'area', 'contagem_reports')
    search_fields = ('titulo', 'descricao')
    readonly_fields = ('contagem_reports',)

    def contagem_reports(self, obj):
        return obj.usuarios_que_reportaram.count()
    contagem_reports.short_description = 'Nº de Denúncias'

class IdeiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'status', 'contagem_reports')
    list_filter = ('status', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'autor__username')
    ordering = ('-data_criacao',)
    readonly_fields = ('contagem_reports',)

    def contagem_reports(self, obj):
        return obj.usuarios_que_reportaram.count()
    contagem_reports.short_description = 'Nº de Denúncias'

# Removi o @admin.register aqui para evitar duplicidade
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'texto', 'ideia', 'data_criacao')
    search_fields = ('texto', 'autor__username')
    list_filter = ('data_criacao',)

# --- REGISTROS DO ADMIN ---
admin.site.register(CustomUsuario, CustomUserAdmin)
admin.site.register(Problema, ProblemaAdmin)
admin.site.register(Ideia, IdeiaAdmin)
# Agora registramos o Comentario passando a classe Admin dele explicitamente
admin.site.register(Comentario, ComentarioAdmin) 
admin.site.register(Votacao)