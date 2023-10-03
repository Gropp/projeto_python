from django.shortcuts import redirect, render
from django.http import HttpResponse
# vamos importar o model do proprio djando da tabela usuarios do sqlite
from django.contrib.auth.models import User
# importar as constantes do django - messages de erro
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.

def cadastro(request):
    print(request.POST)
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