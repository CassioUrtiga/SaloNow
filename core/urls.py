from django.urls import path

from .views import (
    tela_inicial, tela_principal, aguardar, 
    cadastrar_cliente, cadastrar_proprietario, 
    login_view, logout_view, criar_salao, 
    excluirSalao, filtrar_salao, editar_salao,
    atualizar_cep_cliente, agendamento_cliente
)

urlpatterns = [
    path('', tela_inicial, name='inicio'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='deslogar'),
    path('cadastrar-cliente/', cadastrar_cliente, name= 'cadastrar-cliente'),
    path('cadastrar-proprietario/', cadastrar_proprietario, name= 'cadastrar-proprietario'),
    path('tela-principal/', tela_principal, name='principal'),
    path('aguarde/', aguardar, name='aguarde'),
    path('criar-salao/', criar_salao, name='criar-salao'),
    path('excluir-salao/<int:id>/', excluirSalao, name='excluir-salao'),
    path('filtrar-salao/', filtrar_salao, name='filtrar-salao'),
    path('editar-salao/<int:id>/', editar_salao, name='editar-salao'),
    path('atualizar-cep-cliente/', atualizar_cep_cliente, name='atualizar-cep-cliente'),
    path('agendamento-cliente/<int:id>/', agendamento_cliente, name='agendamento-cliente')
]
