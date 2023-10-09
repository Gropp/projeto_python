from django.shortcuts import redirect, render
from django.http import HttpResponse
# vamos importar o model do proprio djando da tabela usuarios do sqlite
from django.contrib.auth.models import User
# importar as constantes do django - messages de erro
from django.contrib.messages import constants
from django.contrib import messages
# importar biblioteca do django que autentica os usuarios no banco
# a funcao login que faz o resto apos autenticar o usuario
from django.contrib.auth import authenticate, login

# Create your views here.

def cadastro(request):
    # print(request.POST)
    # request.POST.get("primeiro_nome")
    if request.method == 'GET':
        return render(request, "cadastro.html")
    elif request.method == 'POST':
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        email = request.POST.get('email')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem.')
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'As senhas devem ter no minimo 6 caracteres.')
            return redirect('/usuarios/cadastro')
        
        try:
            # TODO: Validar se o username do usuario nao existe no BD
            # acho que deu certo :)
            verifica_user = User.objects.get(username=username)
            if verifica_user:
                messages.add_message(request, constants.ERROR, 'Usuário já está cadastrado.')
                return redirect('/usuarios/cadastro')
            else:    
                user = User.objects.create_user(
                    first_name = primeiro_nome,
                    last_name = ultimo_nome,
                    username = username,
                    email=email,
                    password=senha
                )
                messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
        except:
            messages.add_message(request, constants.ERROR, 'Erro ao cadastrar usuário, contato o suporte.')
            return redirect('/usuarios/cadastro')
        
        return redirect('/usuarios/cadastro')

# o django tem uma funcao nativa chamada login
def logar(request):
    # antes de carregar o html testa o tipo de requisicao
    # get carrega a pagina de login
    if request.method == "GET":
        return render(request, 'login.html')
    # post envia os dados do formulario
    elif request.method == "POST":
        # usar os nomes definidos no form do html
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(username=username, password=senha)
        if user:
            #loga com o usuario
            login(request, user)
            return redirect('/exames/solicitar_exames/')
        else:
            #avisa que o username ou senha estão invalidos
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos.')
            return redirect('/usuarios/login')
        
    #print(user)
    #testar o request:
    #return HttpResponse(f'{username} - {senha}')
