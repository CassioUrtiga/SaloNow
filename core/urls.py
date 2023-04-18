from django.urls import path

from .views import tela_inicial, tela_principal, login_view, cadastrar_cliente, cadastrar_proprietario, aguardar, logout_view

urlpatterns = [
    path('', tela_inicial, name='inicio'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='deslogar'),
    path('cadastrar-cliente/', cadastrar_cliente, name= 'cadastrar-cliente'),
    path('cadastrar-proprietario/', cadastrar_proprietario, name= 'cadastrar-proprietario'),
    path('tela-principal/', tela_principal, name='principal'),
    path('aguarde/', aguardar, name='aguarde')
]
