from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ideia, CustomUsuario, Problema, Comentario

class IdeiaForm(forms.ModelForm):
    class Meta:
        model = Ideia
        fields = ['titulo', 'descricao', 'problema_alvo']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'titulo': 'Título da Ideia',
            'descricao': 'Descreva sua Ideia em Detalhes',
            'problema_alvo': 'Esta ideia busca resolver qual problema?'
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsuario
        # Garante que todos os campos necessários estejam aqui
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'tipo', 'curso_departamento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dicionário de placeholders para os campos do formulário
        placeholders = {
            'first_name': 'Nome',
            'username': 'Usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Confirmar senha',
        }
        
        # Aplica os placeholders e remove os labels
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
                self.fields[field_name].label = ''
        
        # Lógica para os campos customizados que não estão no design
        if 'tipo' in self.fields:
            # Esconde o campo 'tipo' e define um valor padrão
            self.fields['tipo'].widget = forms.HiddenInput()
            self.fields['tipo'].initial = 'aluno' # Define 'aluno' como padrão, pode ser 'externo' também
        
        if 'curso_departamento' in self.fields:
            # Esconde o campo e o torna não-obrigatório
            self.fields['curso_departamento'].widget = forms.HiddenInput()
            self.fields['curso_departamento'].required = False
            
        if 'last_name' in self.fields:
            # Esconde o campo e o torna não-obrigatório
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['last_name'].required = False

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'descricao', 'area', 'localizacao']
        # Removemos os labels daqui, pois usaremos placeholders
        labels = {
            'titulo': '',
            'descricao': '',
            'area': '',
            'localizacao': ''
        }
        # Aumentamos o tamanho do campo de descrição
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Estilo padrão para todos os campos
        common_classes = "w-full bg-white/10 border-2 border-white/30 rounded-xl p-4 text-white placeholder-white/70 focus:ring-2 focus:ring-white focus:bg-white/20 transition"
        
        # Adiciona placeholders e classes de estilo a cada campo
        self.fields['titulo'].widget.attrs.update({
            'placeholder': 'Título do problema:',
            'class': common_classes
        })
        self.fields['descricao'].widget.attrs.update({
            'placeholder': 'Descreva o problema em detalhes:',
            'class': common_classes
        })
        self.fields['area'].widget.attrs.update({
            'class': common_classes
        })
        self.fields['localizacao'].widget.attrs.update({
            'placeholder': 'Em que Campus/Bairro esse problema ocorre?',
            'class': common_classes
        })
        
        # Adiciona uma opção "vazia" no topo do dropdown de área
        self.fields['area'].empty_label = "Em qual área este problema se encaixa?"

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escreva seu comentário aqui...'}),
        }
        labels = {
            'conteudo': ''
        }