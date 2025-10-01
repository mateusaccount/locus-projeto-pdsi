# app/forms.py

from django import forms
from .models import Ideia

class IdeiaForm(forms.ModelForm):
    """
    Este é um ModelForm. Ele se constrói automaticamente
    a partir do modelo 'Ideia' que definimos.
    """
    class Meta:
        model = Ideia
        # Aqui listamos os campos do nosso modelo que devem aparecer no formulário.
        # Note que não incluímos 'autor', 'status' ou 'data_criacao'.
        # O 'autor' será o usuário logado (definido na view).
        # O 'status' tem um valor padrão ('rascunho') definido no model.
        # A 'data_criacao' é preenchida automaticamente.
        fields = ['titulo', 'descricao', 'problema_alvo']

        # Opcional: Podemos adicionar 'widgets' para customizar o HTML do formulário.
        # Por exemplo, para que a 'descricao' seja uma área de texto maior.
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 5}),
        }

        # Opcional: Rótulos personalizados para os campos.
        labels = {
            'titulo': 'Título da Ideia',
            'descricao': 'Descreva sua Ideia em Detalhes',
            'problema_alvo': 'Esta ideia busca resolver qual problema?'
        }