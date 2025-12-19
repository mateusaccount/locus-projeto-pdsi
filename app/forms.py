from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, User 
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
        fields = ['texto']
        labels = {
            'texto': ''
        }
        widgets = {
            'texto': forms.Textarea(attrs={
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

class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(
        label="Nome de Usuário", 
        required=True, 
        help_text="Será usado para fazer login.",
        widget=forms.TextInput(attrs={'placeholder': 'Seu login de acesso'})
    )
    first_name = forms.CharField(
        label="Nome", 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Seu primeiro nome'})
    )
    last_name = forms.CharField(
        label="Sobrenome", 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': 'Seu sobrenome'})
    )
    email = forms.EmailField(label="E-mail", required=True)
    curso_departamento = forms.CharField(label="Curso ou Departamento", required=False)

    class Meta:
        model = CustomUsuario
        fields = ['username', 'first_name', 'last_name', 'email', 'curso_departamento']

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and self.instance.is_superuser:
            self.fields['email'].required = False

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if self.instance.is_superuser and not email:
            return ""
            
        if email and CustomUsuario.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este e-mail já está em uso por outro usuário.")
            
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and CustomUsuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso. Escolha outro.")
            
        return username
    
class CadastroForm(UserCreationForm):
    first_name = forms.CharField(label="Nome Completo", max_length=150, required=True)
    email = forms.EmailField(label="E-mail", required=True)

    class Meta:
        model = CustomUsuario
        fields = ('username', 'first_name', 'email')