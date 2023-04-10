from django.urls import path

from .views import tela_inicial, login, cadastrar

urlpatterns = [
    path('', tela_inicial, name='inicio'),
    path('login/', login, name='login'),
    path('cadastrar/', cadastrar, name='cadastrar')
]
