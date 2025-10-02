from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Ideia, CustomUsuario

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