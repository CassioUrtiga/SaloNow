from django.urls import path

from .views import (
    tela_inicial, tela_principal, aguardar, 
    cadastrar_cliente, cadastrar_proprietario, 
    login_view, logout_view, criar_salao, 
    excluirSalao, filtrar_salao, editar_salao,
    atualizar_cep_cliente, agendamento_cliente,
    realizar_agendamento, visualizar_agendamento_pg_proprietario, visualizar_agendamento_especifico, excluir_agendamento, excluir_agendamento_especifico, cancelar_agendamento, cancelar_todos_agendamentos,
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
    path('agendamento-cliente/<int:id>/', agendamento_cliente, name='agendamento-cliente'),
    path('realizar-agendamento/', realizar_agendamento, name='realizar-agendamento'),
    path('detalhes-agendamento-proprietario/', visualizar_agendamento_pg_proprietario, name='detalhes-agendamento-proprietario'),
    path('detalhes-agendamento-especifico/<int:id>/', visualizar_agendamento_especifico, name='detalhes-agendamento-especifico'),
    path('excluir-agendamento/<int:id>/', excluir_agendamento, name='excluir-agendamento'),
    path('excluir-agendamento-especifico/<int:id>/', excluir_agendamento_especifico, name='excluir-agendamento-especifico'),
    path('cancelar-agendamento/<int:id>/', cancelar_agendamento, name='cancelar-agendamento'),
    path('cancelar-todos-agendamentos/', cancelar_todos_agendamentos, name='cancelar-todos-agendamentos'),
]
