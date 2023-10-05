from django.shortcuts import render
from django.http import HttpResponse
# biblioteca de usuarios - testar se esta ou nao logado, entre outras funcoes
# from django.contrib.auth.models import User
# IMPORTANDO UM DECORET DO PYTHON, PODEMOS FAZE QUE DE FORMA AUTOMATICA SOMENTE USUARIOS LOGADOS ACESSEM ESSA VIEW, SEM A NECESSIDADE DE CODIGOS DE TESTE
from django.contrib.auth.decorators import login_required
# importamos o model do banco de dados TiposExames
from .models import TiposExames
import datetime


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
        data_hoje = datetime.date.today()

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
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    print(exames_id)
    return HttpResponse('Fechar pedido')