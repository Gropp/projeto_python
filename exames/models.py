from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.utils.safestring import mark_safe
from secrets import token_urlsafe

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

class AcessoMedico(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    identificacao = models.CharField(max_length=50)
    tempo_de_acesso = models.IntegerField() # Em horas
    criado_em = models.DateTimeField()
    data_exames_iniciais = models.DateField()
    data_exames_finais = models.DateField()
    token = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.token
    
    # sobreescreve o metodo SAVE da MODELS para esse modelo AcessoMedico
    # acrescenta ao metodo salvar a geracao de um token ANTES do salvamento
    def save(self, *args, **kwargs):
        if not self.token:
            # esse token serve para garantir a origem da requesicao
            self.token = token_urlsafe(6)
        # no final ele executa o SAVE da bibliote PAI (original)
        # nao contem caracteres inseguros para usar na URL
        super(AcessoMedico, self).save(*args, **kwargs)

    # como esse metodo tem apenas um retorno, para nao precisarmos chama-lo acesso_medico.status(), com parenteses, entao com um decorador podemos transforma-lo em uma propriedade do acesso_medico e chama-lo direto acesso_medico.status
    @property
    # até a cor altera no vscode
    def status(self):
        # verificar se o timezone > que a data de criacao
        # timedelta permite colocar um valor em horas que pode ser somado a data
        # neste caso estamos passando o tempo de acesso liberado para o medico
        # if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)):
        #     return 'Expirado'
        # else:
        #     return 'Ativo'

        #  PODEMOS FAZER O IF ACIMA DE FORMA DIRETA:
        return 'Expirado' if timezone.now() > (self.criado_em + timedelta(hours=self.tempo_de_acesso)) else 'Ativo'

    @property

    def url(self):
        return f'http://127.0.0.1:8000/exames/acesso_medico/{self.token}'
    # para aplicar essa classe rodar no terminal:
    # python3 manage.py makemigrations
    # python3 manage.py migrate