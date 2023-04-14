from django.shortcuts import render, redirect
from .forms import FormularioCliente,FormularioProprietario

# Create your views here.
def tela_inicial(request):
    return render(request, 'page_inicial/pg_inicial.html')

def login(request):
    return render(request, 'page_login/login.html')

def cadastrar_cliente(request):
    form_cliente = FormularioCliente(request.POST)
    context = {
        'form': form_cliente
    }
    return render(request, 'page_login/cadastro_cliente.html',context)

def cadastrar_proprietario(request):
    form_proprietario = FormularioProprietario(request.POST)
    context = {
        'form': form_proprietario
    }
    return render(request, 'page_login/cadastro_proprietario.html',context)
