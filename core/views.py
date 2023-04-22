import requests
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import FormularioCliente, FormularioProprietario


# Views
def tela_inicial(request):
    return render(request, 'page/inicial.html')

def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = authenticate(request, username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect('principal')
        else:
            user = User.objects.filter(email=usuario).first()
            if user is not None:
                user = authenticate(username=user.username, password=senha)
                if user is not None:
                    login(request, user)
                    return redirect('principal')
                else:
                    messages.error(request, 'Usuário ou senha incorreta')
                    return render(request, 'page_login/login.html')
            else:
                messages.error(request, 'Usuário ou senha incorreta')
                return render(request, 'page_login/login.html')
    else:
        return render(request, 'page_login/login.html')


def logout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    logout(request)
    return redirect('inicio')

def cadastrar_cliente(request):
    if request.method == "POST":
        form_cliente = FormularioCliente(request.POST)
        if form_cliente.is_valid():
            username = form_cliente.data['username']
            email = form_cliente.data['email']
            senha = form_cliente.data['senha']

            if User.objects.filter(username=username).exists():
                messages.warning(request, f'Usuário {username} já existe!')
                return render(request, 'page_login/cadastro_cliente.html', {'form': form_cliente})
            else:
                user = User.objects.create_user(username, email, senha)
                cliente = form_cliente.save(commit=False)
                cliente.user = user

                user.save()
                cliente.save()
                
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('login') 
        else:
            if (verificar_formato_email(form_cliente.data['email'])):
                messages.error(request, 'Formulário inválido!')
                return render(request, 'page_login/cadastro_cliente.html', {'form': FormularioCliente()})
            else:
                messages.error(request, 'E-mail inválido!')
                return render(request, 'page_login/cadastro_cliente.html', {'form': form_cliente})
    else:
        return render(request, 'page_login/cadastro_cliente.html', {'form': FormularioCliente()})

def cadastrar_proprietario(request):
    if request.method == "POST":
        form_proprietario = FormularioProprietario(request.POST)
        if form_proprietario.is_valid():
            username = form_proprietario.data['username']
            email = form_proprietario.data['email']
            senha = form_proprietario.data['senha']

            if User.objects.filter(username=username).exists():
                messages.warning(request, f'Usuário {username} já existe!')
                return render(request, 'page_login/cadastro_proprietario.html', {'form': form_proprietario})
            else:
                try:
                    cnpj = str(form_proprietario.data['cnpj']).replace('.','').replace('/','').replace('-','')
                    resposta = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}")

                    dados = resposta.json()
                    if resposta.status_code != 200 or dados['status'] == 'ERROR':
                        messages.error(request, 'CNPJ inválido')
                        return render(request, 'page_login/cadastro_proprietario.html', {'form': form_proprietario})
                except:
                    return redirect('aguarde')

                user = User.objects.create_user(username, email, senha)
                proprietario = form_proprietario.save(commit=False)
                proprietario.user = user

                user.save()
                proprietario.save()

                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('login')
        else:
            if (verificar_formato_email(form_proprietario.data['email'])):
                messages.error(request, 'Formulário inválido!')
                return render(request, 'page_login/cadastro_proprietario.html', {'form': FormularioProprietario()})
            else:
                messages.error(request, 'E-mail inválido!')
                return render(request, 'page_login/cadastro_proprietario.html', {'form': form_proprietario})
    else:
        return render(request, 'page_login/cadastro_proprietario.html', {'form': FormularioProprietario()})

def tela_principal(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'page/principal.html')
    
def aguardar(request):
    return render(request, 'page/aguarde.html')


# Functions
def verificar_formato_email(email):
    padrao = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
    if re.match(padrao, email):
        return True
    else:
        return False
