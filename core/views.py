from django.shortcuts import render, redirect

# Create your views here.
def tela_inicial(request):
    return render(request, 'page_inicial/pg_inicial.html')

def login(request):
    return render(request, 'page_login/pg_login.html')

def cadastrar(request):
    return render(request, 'page_login/pg_cadastro.html')

