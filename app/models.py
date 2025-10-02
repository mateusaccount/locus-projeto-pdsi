from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUsuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('aluno', 'Aluno'),
        ('servidor', 'Servidor'),
        ('externo', 'Comunidade Externa'),
    ]
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    curso_departamento = models.CharField(max_length=100, blank=True, null=True, help_text="Curso (se aluno) ou Departamento (se servidor)")

    def __str__(self):
        return self.username


class Problema(models.Model):
    AREA_CHOICES = [
        ('educacao', 'Educação'),
        ('meio_ambiente', 'Meio Ambiente'),
        ('saude', 'Saúde'),
        ('infraestrutura', 'Infraestrutura'),
        ('outro', 'Outro'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    area = models.CharField(max_length=50, choices=AREA_CHOICES)
    localizacao = models.CharField(max_length=255, help_text="Ex: Bairro, Cidade, Campus")
    usuarios_que_reportaram = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='problemas_reportados',
        blank=True
    )
    
    @property
    def total_reports(self):
        return self.usuarios_que_reportaram.count()

    def __str__(self):
        return self.titulo


class Ideia(models.Model):
    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('em_avaliacao', 'Em Avaliação'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problema_alvo = models.ForeignKey(
        Problema,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Vincule a um problema existente, se aplicável."
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='rascunho')
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuarios_que_reportaram = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='ideias_reportadas',
        blank=True
    )

    @property
    def pontuacao_total(self):
        upvotes = self.votos.filter(tipo='upvote').count()
        downvotes = self.votos.filter(tipo='downvote').count()
        return upvotes - downvotes

    @property
    def total_reports(self):
        return self.usuarios_que_reportaram.count()
        
    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    ideia = models.ForeignKey(Ideia, related_name='comentarios', on_delete=models.CASCADE)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.autor.username} em '{self.ideia.titulo}'"


class Votacao(models.Model):
    TIPO_VOTO_CHOICES = [
        ('upvote', 'Upvote'),
        ('downvote', 'Downvote'),
    ]
    ideia = models.ForeignKey(Ideia, related_name='votos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_VOTO_CHOICES)

    class Meta:
        unique_together = ('ideia', 'usuario')

    def __str__(self):
        return f"{self.usuario.username} votou '{self.tipo}' em '{self.ideia.titulo}'"
