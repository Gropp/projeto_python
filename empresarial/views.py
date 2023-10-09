from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import Value
from django.contrib.admin.views.decorators import staff_member_required
from exames.models import SolicitacaoExame
from django.http import HttpResponse, FileResponse

# Create your views here.

@staff_member_required

def gerenciar_clientes(request):
    clientes = User.objects.filter(is_staff=False)

    # dados vindo da URL para fazer o search
    nome_completo = request.GET.get('nome')
    email = request.GET.get('email')

    if email:
        # o contains - a string contem o email
        clientes = clientes.filter(email__contains = email)
    if nome_completo:
        # annoted cria um campo antes de fazer a pesquisa
        # concatena os campos do bd
        # O Value cria um valor como se fosse um campo do bd, nao da para simplesmente colocar um campo em branco nestas concatenacoes com BD
        # no final cria um filtro que utiliza o campo full_name criado pela concatenacao dos campos do BD, buscando somente o cliente que tenha esse nome completo
        clientes = clientes.annotate(full_name=Concat('first_name', Value(' '),'last_name')).filter(full_name__contains=nome_completo)
    
    return render(request, 'gerenciar_clientes.html', {'clientes' : clientes})

@staff_member_required

def cliente(request, cliente_id):
    cliente = User.objects.get(id=cliente_id)
    exames = SolicitacaoExame.objects.filter(usuario=cliente)
    return render(request, 'cliente.html', {'cliente': cliente, 'exames': exames})

@staff_member_required

def exame_cliente(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    return render(request, 'exame_cliente.html', {'exame': exame})

def proxy_pdf(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    # passando o id do exame é possivel pegar o campo resultado e mandar abrir o pdf
    response = exame.resultado.open()
    return HttpResponse(response)