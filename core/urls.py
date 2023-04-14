from django.urls import path

from .views import tela_inicial, login, cadastrar_cliente,cadastrar_proprietario

urlpatterns = [
    path('', tela_inicial, name='inicio'),
    path('login/', login, name='login'),
    path('cadastrar-cliente/', cadastrar_cliente, name= 'cadastrar-cliente'),
    path('cadastrar-proprietario/', cadastrar_proprietario, name= 'cadastrar-proprietario'),
]
