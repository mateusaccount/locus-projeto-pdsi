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
        fields = UserCreationForm.Meta.fields + ('tipo', 'curso_departamento', 'first_name', 'last_name', 'email')

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'descricao', 'area', 'localizacao']
        labels = {
            'titulo': 'Qual é o problema?',
            'descricao': 'Descreva o problema em detalhes',
            'area': 'Em qual área este problema se encaixa?',
            'localizacao': 'Onde este problema ocorre? (Bairro, Cidade, Campus, etc.)'
        }

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