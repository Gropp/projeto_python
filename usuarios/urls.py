from django.urls import path
# importa o arquivo views do app cadastro que é onde estao as funçoes do app usuarios
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro")
]