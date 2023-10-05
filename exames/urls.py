from django.urls import path
# importa do app atual o views
from . import views

urlpatterns = [
    # cria uma url que aponta para a funcao solicitar_exames dentro da views deste app
    # podemos passar argumentos para dentro da URL como em cancelar pedido
    path("solicitar_exames/", views.solicitar_exames, name="solicitar_exames"),
    path("fechar_pedido/", views.fechar_pedido, name="fechar_pedido"),
    path("gerenciar_pedidos/", views.gerenciar_pedidos, name="gerenciar_pedidos"),
    path("cancelar_pedido/<int:pedido_id>", views.cancelar_pedido, name="cancelar_pedido")
]
