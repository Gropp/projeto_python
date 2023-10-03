from django.shortcuts import redirect, render
from django.http import HttpResponse
# vamos importar o model do proprio djando da tabela usuarios do sqlite
from django.contrib.auth.models import User

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
            return redirect('/usuarios/cadastro')
        
        if len(senha) < 6:
            return redirect('/usuarios/cadastro')
        user = User.objects.create_user(
            first_name = primeiro_nome,
            last_name = ultimo_nome,
            username = username,
            email=email,
            password=senha
        )

        return HttpResponse('Passou')