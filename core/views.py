import requests
import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import FormularioCliente, FormularioProprietario, FormularioSalao
from .models import Cliente, Proprietario, Salon, DiasFuncionamento, Servicos
from django.shortcuts import get_object_or_404
from django.db.models import Q
from functools import reduce
import base64
from PIL import Image
from io import BytesIO
import tempfile
from django.core.files.base import ContentFile

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
            dados_cep = None

            # Faz uma nova requisição para verificar a veracidade do cep
            try:
                cep = requests.get(f"https://viacep.com.br/ws/{form_cliente.data['cep'].replace('-','')}/json/")
                
                dados_cep = cep.json()
                if dados_cep.get('erro'):
                    raise Exception()
            except:
                messages.error(request, 'CEP inválido')
                return render(request, 'page_login/cadastro_cliente.html', {'form': form_cliente})
            
            # Realiza o cadastro do cliente 
            if User.objects.filter(username=username).exists():
                messages.warning(request, f'Usuário {username} já existe!')
                return render(request, 'page_login/cadastro_cliente.html', {'form': form_cliente})
            else:
                user = User.objects.create_user(username, email, senha)
                cliente = form_cliente.save(commit=False)

                cliente.user = user
                cliente.cidade = dados_cep['localidade']
                cliente.uf = dados_cep['uf']

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
                    if dados['status'] == 'ERROR':
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
    verifica = True
    if not request.user.is_authenticated:
        return redirect('login')
    
    #verifica = true (cliente) / false (proprietario)
    verifica = Cliente.objects.filter(user=request.user.id).exists()

    if not verifica:
        prop = Proprietario.objects.get(user_id=request.user.id)

    context = {
        'verificacao': verifica,
        'cliente': Cliente.objects.get(user_id=request.user.id) if verifica else None,
        'proprietario': prop if not verifica else None,
        'form': FormularioSalao() if not verifica else None,
        'saloes': Salon.objects.all() if verifica else Salon.objects.filter(proprietario_id=prop.id),
        'quantidade': Salon.objects.all().count() if verifica else Salon.objects.filter(proprietario_id=prop.id).count()
    }

    return render(request, 'page/principal.html', context)

def criar_salao(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = FormularioSalao(request.POST)

    if form.is_valid():
        dados = []
        
        # Obter os valores das caixas de seleção
        dias_selecionados = request.POST.getlist('segunda') + request.POST.getlist('terca') + request.POST.getlist('quarta') + request.POST.getlist('quinta') + request.POST.getlist('sexta') + request.POST.getlist('sabado') + request.POST.getlist('domingo')


        # Obter as horas de abertura e fechamento para o dia atual
        for dia in dias_selecionados:
            abertura = request.POST.get(f'temp_aberto_{dia[:3].lower()}')
            fechamento = request.POST.get(f'temp_fecha_{dia[:3].lower()}')
            dados.append([dia, abertura, fechamento])

        salao = Salon.objects.create(
            proprietario=Proprietario.objects.get(user_id=request.user.id),
            nome_salao=form.cleaned_data['nome_salao'],
            descricao=form.cleaned_data['descricao'],
            cidade=form.cleaned_data['cidade'],
            rua=form.cleaned_data['rua'],
            pais=form.cleaned_data['pais'],
            bairro=form.cleaned_data['bairro'],
            numero=form.cleaned_data['numero']
        )

        # verifica o estado da imagem enviada
        salao_status = request.POST.get('img_salao')
         
        if salao_status == '':
            salao.imagem_salao = 'fotos_salao/default.jpg'
        else:
            imagem_decodificada = decode_base64_image(salao_status)
            with tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False) as temp_file:
                imagem_decodificada.save(temp_file, format='JPEG')
                temp_file.seek(0)
                file_content = temp_file.read()
            
            content_file = ContentFile(file_content)
            salao.imagem_salao.save(temp_file.name, content_file)
            
        for obj in dados:
            dia = DiasFuncionamento.objects.create(dia_semana=obj[0],abertura=obj[1] if obj[1] else '00:00:00', fechamento=obj[2] if obj[2] else '00:00:00')
            salao.dias_funcionamento.add(dia)
        
        # Obter os valores dos inputs serviços
        input_servicos = request.POST.getlist('servicos[]')
        input_precos = request.POST.getlist('precos[]')

        for i, obj in enumerate(input_servicos):
            salao.servico.add(Servicos.objects.create(servico=obj, preco=input_precos[i]))
        
        salao.save()
        messages.success(request, f'Salão {salao.nome_salao.upper()} cadastrado com sucesso')
        return redirect('principal')
    else:
        messages.warning(request, 'Formulário inválido')
        return redirect('principal')

def excluirSalao(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    salao = get_object_or_404(Salon, proprietario=Proprietario.objects.get(user_id=request.user.id), pk=id)
    messages.error(request, f'Salão {salao.nome_salao.upper()} foi exluído')
    salao.delete()
    return redirect('principal')

def filtrar_salao(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    filtro = str(request.POST.get('filtro')).split(',')
    filtro = [s.strip() for s in filtro]

    condicoes = [
        Q(cidade__icontains=termo) | 
        Q(bairro__icontains=termo) | 
        Q(rua__icontains=termo) | 
        Q(numero__icontains=termo) |
        Q(pais__icontains=termo)
        for termo in filtro
    ]

    saloes = Salon.objects.filter(reduce(lambda x, y: x | y, condicoes))

    context = {
        'verificacao': True,
        'cliente': Cliente.objects.get(user_id=request.user.id),
        'saloes': saloes,
        'quantidade': saloes.count(),
    }

    if context["quantidade"] == 0:
        messages.warning(request, 'Nenhum resultado para a busca')
        return redirect('principal')

    
    messages.success(request, f'Foram encontrados {context["quantidade"]} resultados para a busca')
    return render(request, 'page/principal.html', context)

def editar_salao(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    form = FormularioSalao(request.POST, request.FILES)

    if form.is_valid():
        dados = []
        salao = get_object_or_404(Salon, proprietario=Proprietario.objects.get(user_id=request.user.id), pk=id)

        # Obter os valores das caixas de seleção
        dias_selecionados = request.POST.getlist('segunda') + request.POST.getlist('terca') + request.POST.getlist('quarta') + request.POST.getlist('quinta') + request.POST.getlist('sexta') + request.POST.getlist('sabado') + request.POST.getlist('domingo')

        # Obter as horas de abertura e fechamento para o dia atual
        for dia in dias_selecionados:
            abertura = request.POST.get(f'temp_aberto_{dia[:3].lower()}')
            fechamento = request.POST.get(f'temp_fecha_{dia[:3].lower()}')
            dados.append([dia, abertura, fechamento])
        
        salao.nome_salao = form.cleaned_data['nome_salao']
        salao.descricao = form.cleaned_data['descricao']
        salao.cidade = form.cleaned_data['cidade']
        salao.rua = form.cleaned_data['rua']
        salao.pais = form.cleaned_data['pais']
        salao.bairro = form.cleaned_data['bairro']
        salao.numero = form.cleaned_data['numero']
        
        salao.dias_funcionamento.clear()
        for obj in dados:
            dia = DiasFuncionamento.objects.create(dia_semana=obj[0],abertura=obj[1] if obj[1] else '00:00:00', fechamento=obj[2] if obj[2] else '00:00:00')
            salao.dias_funcionamento.add(dia)
        
        # Obter os valores dos inputs serviços
        salao.servico.clear()
        input_servicos = request.POST.getlist('servicos[]')
        input_precos = request.POST.getlist('precos[]')
        
        for i, obj in enumerate(input_servicos):
            salao.servico.add(Servicos.objects.create(servico=obj, preco=input_precos[i]))

        # verifica o estado da imagem enviada
        salao_status = request.POST.get('img_salao')
        
        if salao_status != 'null':
            if 'default.jpg' not in salao.imagem_salao.url:
                salao.imagem_salao.delete()

            if salao_status == '':
                salao.imagem_salao = 'fotos_salao/default.jpg'
            else:
                imagem_decodificada = decode_base64_image(salao_status)
                with tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False) as temp_file:
                    imagem_decodificada.save(temp_file, format='JPEG')
                    temp_file.seek(0)
                    file_content = temp_file.read()
                
                content_file = ContentFile(file_content)
                salao.imagem_salao.save(temp_file.name, content_file)

        salao.save()
        messages.success(request, f'Salão {salao.nome_salao.upper()} foi alterado com sucesso')
        return redirect('principal')
    else:
        messages.warning(request, 'Formulário inválido')
        return redirect('principal')

def atualizar_cep_cliente(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    item1 = request.POST.get('validation_message1')
    item2 = request.POST.get('validation_message2')

    local = ''

    if item1:
        local = item1
    elif item2:
        local = item2

    if not local:
        return redirect('principal')
    
    local_array = str(local).split(',')
    cliente = Cliente.objects.get(user_id=request.user.id)

    cliente.cep = local_array[0]
    cliente.cidade = local_array[1]
    cliente.uf = local_array[2]

    cliente.save()

    return redirect('principal')

def aguardar(request):
    return render(request, 'page/aguarde.html')

def agendamento_cliente(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request,'page/agendamento_cliente.html')


# Functions
def verificar_formato_email(email):
    padrao = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
    if re.match(padrao, email):
        return True
    else:
        return False

def decode_base64_image(base64_string):
    encoded_data = base64_string.split(',')[1]

    image_data = base64.b64decode(encoded_data)

    image = Image.open(BytesIO(image_data))

    return image