from django.urls import path
# importa do app atual o views
from . import views

urlpatterns = [
    # cria uma url que aponta para a funcao solicitar_exames dentro da views deste app
    path("solicitar_exames/", views.solicitar_exames, name="solicitar_exames"),
    path("fechar_pedido/", views.fechar_pedido, name="fechar_pedido"),
    path("gerenciar_pedidos/", views.gerenciar_pedidos, name="gerenciar_pedidos")
]
