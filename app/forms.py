from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Ideia, CustomUsuario, Problema, Comentario

class IdeiaForm(forms.ModelForm):
    class Meta:
        model = Ideia
        fields = ['titulo', 'descricao', 'problema_alvo']
        labels = { 'titulo': '', 'descricao': '', 'problema_alvo': '' }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = "w-full bg-white/10 border-2 border-white/30 rounded-xl p-4 text-white placeholder-white/70 focus:ring-2 focus:ring-white focus:bg-white/20 transition"
        
        self.fields['titulo'].widget.attrs.update({
            'placeholder': 'Título da ideia:',
            'class': common_classes
        })
        self.fields['descricao'].widget.attrs.update({
            'placeholder': 'Descreva a sua ideia em detalhes:',
            'class': common_classes
        })
        self.fields['problema_alvo'].widget.attrs.update({
            'class': common_classes
        })
        self.fields['problema_alvo'].empty_label = "Esta ideia resolve qual problema? (Opcional)"

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUsuario
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'tipo', 'curso_departamento')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'Nome',
            'username': 'Usuário',
            'email': 'Email',
            'password1': 'Senha',
            'password2': 'Confirmar senha',
        }
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs['placeholder'] = placeholder
                self.fields[field_name].label = ''
        
        if 'tipo' in self.fields:
            self.fields['tipo'].widget = forms.HiddenInput()
            self.fields['tipo'].initial = 'aluno'
        
        if 'curso_departamento' in self.fields:
            self.fields['curso_departamento'].widget = forms.HiddenInput()
            self.fields['curso_departamento'].required = False
            
        if 'last_name' in self.fields:
            self.fields['last_name'].widget = forms.HiddenInput()
            self.fields['last_name'].required = False

class ProblemaForm(forms.ModelForm):
    class Meta:
        model = Problema
        fields = ['titulo', 'descricao', 'area', 'localizacao']
        labels = { 'titulo': '', 'descricao': '', 'area': '', 'localizacao': '' }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_classes = "w-full bg-white/10 border-2 border-white/30 rounded-xl p-4 text-white placeholder-white/70 focus:ring-2 focus:ring-white focus:bg-white/20 transition"
        
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
        self.fields['area'].empty_label = "Em qual área este problema se encaixa?"

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        labels = {
            'conteudo': ''
        }
        widgets = {
            'conteudo': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Escreva seu comentário aqui...',
                'class': 'w-full bg-white/10 border-2 border-white/30 rounded-xl p-4 text-white placeholder-white/70 focus:ring-2 focus:ring-white focus:bg-white/20 transition'
            }),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de usuário'
        self.fields['username'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password'].label = ''