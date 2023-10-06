from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
# Herdam a classe do models.model - geram os sqls
# python3 manage.py makemigrations
class TiposExames(models.Model):
    # enumereite - opçoes para uma variavel
    tipo_choices = (
        ('I', 'Exame de imagem'),
        ('S', 'Exame de sangue')
    )
    nome = models.CharField(max_length=50)
    tipo = models.CharField(max_length=1, choices=tipo_choices)
    preco = models.FloatField()
    disponivel = models.BooleanField(default=True)
    horario_inicial = models.IntegerField()
    horario_final = models.IntegerField()

    # mostra o nome da classe e nao o endereço no banco de dados
    # sem essa string ele coloca o nome do objeto como referencia no BD
    # SAO DOIS UNDERLINES DE CADA LADO __
    def __str__(self):
        return self.nome

class SolicitacaoExame(models.Model):
    choice_status = (
        ('E', 'Em análise'),
        ('F', 'Finalizado')
    )
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exame = models.ForeignKey(TiposExames, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=2, choices=choice_status)
    resultado = models.FileField(upload_to="resultados", null=True, blank=True)
    requer_senha = models.BooleanField(default=False)
    senha = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f'{self.usuario} | {self.exame.nome}'
    
    # definindo a formatacao do status com o bootstrap
    def badge_template(self):
        if self.status == 'E':
            classes = 'bg-warning text-dark'
            texto = "Em analise"
        elif self.status == 'F':
            classes = 'bg-success'
            texto = "Finalizado"
        
        # mark_safe faz o djando reenderizar como html o texto formatado
        return mark_safe(f'<span class="badge {classes}">{texto}</span>')

class PedidosExames(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    exames = models.ManyToManyField(SolicitacaoExame)
    agendado = models.BooleanField(default=True)
    data = models.DateField()

    def __str__(self):
      return f'{self.usuario} | {self.data}'