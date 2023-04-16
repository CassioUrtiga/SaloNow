from django.shortcuts import render, redirect
from .forms import FormularioCliente,FormularioProprietario

# Create your views here.
def tela_inicial(request):
    return render(request, 'page_inicial/pg_inicial.html')

def login(request):
    return render(request, 'page_login/pg_login.html')

def cadastrar(request):
    form_proprietario = FormularioProprietario(request.POST)
    form_cliente = FormularioCliente(request.POST)

    context = {
        'form_cliente': form_cliente, 
        'form_proprietario': form_proprietario
    }
    return render(request, 'page_login/pg_cadastro.html',context)

