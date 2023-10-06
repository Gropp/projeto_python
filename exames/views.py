from django.shortcuts import render, redirect
from django.http import HttpResponse
# biblioteca de usuarios - testar se esta ou nao logado, entre outras funcoes
# from django.contrib.auth.models import User
# IMPORTANDO UM DECORET DO PYTHON, PODEMOS FAZE QUE DE FORMA AUTOMATICA SOMENTE USUARIOS LOGADOS ACESSEM ESSA VIEW, SEM A NECESSIDADE DE CODIGOS DE TESTE
from django.contrib.auth.decorators import login_required
# importamos o model do banco de dados TiposExames, PedidosExames e SolicitacaoExame
from .models import TiposExames, PedidosExames, SolicitacaoExame
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


# Create your views here.

# decoretors
@login_required

def solicitar_exames(request):
    # testa se o usuario esta logado no sistema
    # usa o metodo da classe User is_autenticated
    # print(request.user.is_authenticated)
    # se estiver logado aparece o nome do usuario, se nao aparece AnonymousUser
    # com o .is_authenticated ele retorna True ou False
    # COM O DECORET IMPORTADO NÃO É NECESSARIO FAZER TESTES NA VIEW PARA VER SE O USUARIO ESTA LOGADO, POIS ELA JA SE ENCARREGA DE DEIXAR A VIEW SOMENTE ACESSIVEL PARA USUARIOS LOGADOS
    # if not request.user.is_authenticated:
        #  o return encerra o codigo
    #    return HttpResponse('Área exclusiva para usuarios logados!')

    # buscamos na tabela todos os tipos de exames (.filter para filtrar)
    # torna a variavel global para funcionar no IF e no ELIF
    # CRIAMOS UMA INSTANCIA DA TABELA/MODELO TiposExames
    tipos_exames = TiposExames.objects.all()

    # testa o tipo da requisicao. Se for carregar a pagina (GET) renderiza um HTML no templates
    # se for um envio de formulario (POST) faz outra coisa
    if request.method == "GET":
        # passamos esse dicionario para ser usado no html
        # somente do campo tipos exames que é o que interessa no momento
        return render(request, 'solicitar_exames.html', {'tipos_exames':tipos_exames})
    elif request.method == "POST":
        # DESAFIO DE POR A DATA
        # data atual
        data_hoje = datetime.now()

        exames_id = request.POST.getlist('exames')
        # aplica o filtro in no "select" da tabela TiposExames
        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        # print(exames_id)
        # print(solicitacao_exames)

        # TODO: Calcular somente para os dados disponiveis
        preco_total = 0
        for idx in solicitacao_exames:
            # so soma o preço se o exame estiver disponivel
            if idx.disponivel:
                preco_total += idx.preco
        # passamos esse dicionario para ser usado no html
        return render(request, 'solicitar_exames.html', {'tipos_exames':tipos_exames,
                                                         'solicitacao_exames':solicitacao_exames,
                                                         'preco_total':preco_total,
                                                         'data_atual': data_hoje})

@login_required

def fechar_pedido(request):
    # recebe do form os ids dos exames selecionados
    exames_id = request.POST.getlist('exames')
    # aplica o filtro in no "select" da tabela TiposExames e retorna todos campos desses exames
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)

    # CRIAMOS UMA INSTANCIA DA TABELA/MODELO PedidosExames
    pedido_exame = PedidosExames(
        # pegamos o usuario LOGADO
        usuario = request.user,
        # o  campo agendado ja é True por default
        data = datetime.now()
    )
    # para salvar o pedido exame no banco de dados
    pedido_exame.save()

    # VAMOS CRIAR UMA SOLICITACAO PARA CADA UM DOS EXAMES
    # INSTANCIA A TABELA DENTRO DO FOR PARA CADA EXAME
    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        # SALVAR NO BANCO
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)
    
    pedido_exame.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido de exame realizado com sucesso.')

    #print(exames_id)
    #print(request.user)
    return redirect('/exames/gerenciar_pedidos/')

@login_required

def gerenciar_pedidos(request):
    # instanciamos a tabela e trazemos os pedidos de exames do usuario LOGADO
    # o filter traz uma lista de dados
    pedidos_exames = PedidosExames.objects.filter(usuario=request.user)
    # enviamos esses pedidos para o HTML passando como argumento do render
    return render(request, 'gerenciar_pedidos.html', {'pedidos_exames':pedidos_exames})

@login_required

def cancelar_pedido(request, pedido_id):
    # instanciamos a tabela e trazemos o pedido de exame do usuario LOGADO
    # o get traz somente um pedido
    pedido = PedidosExames.objects.get(id=pedido_id)
    # por seguranca testamos se o usuario logado e o usuario do pedido sao os mesmos
    if not pedido.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'O pedido selecionado não pertence a esse usuário.')
        return redirect('/exames/gerenciar_pedidos/')
    # podemos alterar um valor de um campo no BD
    pedido.agendado = False
    # agora precisamos GRAVAR no BD a altercao
    pedido.save()
    messages.add_message(request, constants.SUCCESS, 'Pedido cancelado com sucesso.')
    return redirect('/exames/gerenciar_pedidos/')

@login_required

def gerenciar_exames(request):
    # instanciamos o banco e filtramos TODOS os exames do usurio LOGADO
    exames = SolicitacaoExame.objects.filter(usuario=request.user)
    # passamos esse objeto para o HTML como argumento
    return render(request, 'gerenciar_exames.html', {'exames': exames})

@login_required

def permitir_abrir_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    #TODO VERIFICAR SE O EXAME TEM PDF CADASTRADO
    if not exame.resultado:
        messages.add_message(request, constants.ERROR, 'O exame solicitado não está disponível. Contate um atendente para auxiliá-lo.')
        return redirect('/exames/gerenciar_exames/')
    elif not exame.requer_senha:
        return redirect(exame.resultado.url)
    else:
        # usar o f para passar o path e o argumento
        return redirect(f'/exames/solicitar_senha_exame/{exame.id}')

@login_required

def solicitar_senha_exame(request, exame_id):
    exame = SolicitacaoExame.objects.get(id=exame_id)
    if request.method == "GET":
        # passa a instancia do SolicitarExame - exame como context da URL
        # assim é possivel referenciar a tabela e tabelas relacionadas no HTML
        return render(request, 'solicitar_senha_exame.html', {'exame': exame})
    elif request.method == "POST":
        # o sistema só entra em solicitar_senha_exame, se tiver um PDF anexado
        # entao nao precisa testar novamente aqui dentro
        # recupera o valor do campo senha do HTML
        senha = request.POST.get('senha')
        if senha == exame.senha:
            return redirect(exame.resultado.url)
        else:
            messages.add_message(request, constants.ERROR, 'Senha Invalida.')
            # sempre ao redirecionar para um html com argumento, utilize o f antes do path
            return redirect(f'/exames/solicitar_senha_exame/{exame.id}')