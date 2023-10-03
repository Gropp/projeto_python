from django.urls import path
# importa o arquivo views do app cadastro que é onde estao as funçoes do app usuarios
from . import views

urlpatterns = [
    # nas views é chamado o metodo que executa no path
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.logar, name="login"),
]