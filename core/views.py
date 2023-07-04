import base64
import re
import requests
import tempfile
from functools import reduce
from io import BytesIO
from datetime import datetime, date, timedelta

from django.http import HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from PIL import Image

from .forms import FormularioCliente, FormularioProprietario, FormularioSalao
from .models import Cliente, Proprietario, Salon, DiasFuncionamento, Servicos, Agendamento, CacheAgendamentos


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

@login_required(login_url='login')
def logout_view(request):
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
                cliente.sexo = form_cliente.data['sexo']

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

@login_required(login_url='login')
def tela_principal(request):
    agendamentos_cliente = None
    agendamentos_salao_id = []
    verifica_horarios_funcionamento = []
    agendamentos_disponiveis = []
    cache_agendamentos = []

    verifica = Cliente.objects.filter(user=request.user.id).exists() # true (cliente) / false (proprietario)

    if verifica: # Caracteríticas do cliente
        agendamentos_cliente = Agendamento.objects.filter(cliente=Cliente.objects.get(user=request.user.id))

        # pega os ids do salão para saber quais possuem agendamentos
        for obj in agendamentos_cliente:
            agendamentos_salao_id.append(obj.salao.id)
        
        # verifica os horários de funcionamento, retorna os ids inválidos (fechar salão)
        for i in Salon.objects.all():
            for j in i.dias_funcionamento.all():
                abertura = j.abertura
                fechamento = j.fechamento
                if (abertura > fechamento) or (abertura == fechamento):
                    verifica_horarios_funcionamento.append(i.id)
                    break
            
    else: # Caracteríticas do proprietário
        prop = Proprietario.objects.get(user_id=request.user.id)

        agendamento = Agendamento.objects.filter(proprietario=prop)

        for obj in agendamento:
            salao_id = obj.salao.id
            ocorrencias = agendamento.filter(salao_id=salao_id).count()
            agendamentos_salao_id.append({'id':salao_id, 'ocorrencias': ocorrencias})
            agendamentos_disponiveis.append(salao_id)
        
        # remove ids duplicados
        agendamentos_salao_id = list({item['id']: item for item in agendamentos_salao_id}.values())

        # adiciona os ids dos salões que tem agendamentos em cache
        cache = CacheAgendamentos.objects.filter(proprietario=prop)
        for obj in cache:
            cache_agendamentos.append(obj.salao.id)

    context = {
        'verificacao': verifica,
        'cliente': Cliente.objects.get(user_id=request.user.id) if verifica else None,
        'proprietario': prop if not verifica else None,
        'form': FormularioSalao() if not verifica else None,
        'saloes': Salon.objects.all() if verifica else Salon.objects.filter(proprietario_id=prop.id),
        'quantidade': Salon.objects.all().count() if verifica else Salon.objects.filter(proprietario_id=prop.id).count(),
        'agendamentos_salao_id': agendamentos_salao_id,
        'quantidade_agendamentos': agendamento.count() if not verifica else None,
        'agendamentos_disponiveis': agendamentos_disponiveis if not verifica else None,
        'agendamentos_cliente': agendamentos_cliente if verifica else None,
        'verifica_horarios': verifica_horarios_funcionamento if verifica else None,
        'cache_agendamentos': cache_agendamentos if not verifica else None,
    }

    return render(request, 'page/principal.html', context)

@login_required(login_url='login')
def criar_salao(request):
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
        servicos = request.POST.getlist('servicos[]')
        precos = request.POST.getlist('precos[]')
        duracao_servico_homem = request.POST.getlist('duracao_homem[]')
        duracao_servico_mulher = request.POST.getlist('duracao_mulher[]')

        for i, obj in enumerate(servicos):
            salao.servico.add(Servicos.objects.create(servico=obj, preco=precos[i], duracao_maxima_homem=duracao_servico_homem[i], duracao_maxima_mulher=duracao_servico_mulher[i]))
        
        salao.save()
        messages.success(request, f'Salão {salao.nome_salao.upper()} cadastrado com sucesso')
        return redirect('principal')
    else:
        messages.warning(request, 'Formulário inválido')
        return redirect('principal')

@login_required(login_url='login')
def excluirSalao(request, id):
    salao = get_object_or_404(Salon, proprietario=Proprietario.objects.get(user_id=request.user.id), pk=id)
    messages.error(request, f'Salão {salao.nome_salao.upper()} foi exluído')
    salao.delete()

    return redirect('principal')

@login_required(login_url='login')
def filtrar_salao(request):
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

@login_required(login_url='login')
def editar_salao(request, id):
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
        servicos = request.POST.getlist('servicos[]')
        precos = request.POST.getlist('precos[]')
        duracao_servico_homem = request.POST.getlist('duracao_homem[]')
        duracao_servico_mulher = request.POST.getlist('duracao_mulher[]')
        
        for i, obj in enumerate(servicos):
            salao.servico.add(Servicos.objects.create(servico=obj, preco=precos[i], duracao_maxima_homem=duracao_servico_homem[i], duracao_maxima_mulher=duracao_servico_mulher[i]))

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

@login_required(login_url='login')
def atualizar_cep_cliente(request):
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

@login_required(login_url='login')
def realizar_agendamento(request):
    try:
        id_salao = request.POST.get('id_salao')
        faixa_idade = request.POST.get('idade')
        total = request.POST.get('total')
        servicos_selecionados = request.POST.getlist('servicos_selecionados[]')
        dia = request.POST.get('dia_selecionado')
        horario = request.POST.get('horario')

        agendamento = Agendamento.objects.create(
            proprietario = Salon.objects.get(pk=int(id_salao)).proprietario,
            cliente = Cliente.objects.get(user_id=request.user.id),
            salao = Salon.objects.get(pk=int(id_salao)),
            idade = faixa_idade,
            total_pagar = float(total),
            dia_selecionado = dia,
            horario_selecionado = datetime.strptime(horario, "%H:%M").time(),
        )

        for i, obj in enumerate(servicos_selecionados):
            agendamento.servico.add(Servicos.objects.get(pk=int(obj)))
        
        agendamento.save()
        
        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('principal')
    except:
        messages.error(request, 'Não foi possível efetuar o agendamento')
        return redirect('principal')

@login_required(login_url='login')
def agendamento_cliente(request, id):
    cliente = Cliente.objects.get(user_id=request.user.id)
    salao = Salon.objects.get(pk=id)
    agendamentos = Agendamento.objects.filter(salao=salao)
    horarios_ocupados = [] # [[dia_selecionado, horario_inicial, horario_final]]
    servicos = []

    for obj in salao.servico.all():
        servicos.append({
            'id': obj.id,
            'servico': obj.servico,
            'preco': obj.preco,
            'duracao_maxima': obj.duracao_maxima_homem.strftime('%H:%M') if cliente.sexo == 'M' else obj.duracao_maxima_mulher.strftime('%H:%M')
        })

    # pega os horários que já tem agendamentos
    for agendamento in agendamentos:
        if agendamento.cliente.sexo == 'F':
            soma = '00:00'
            horario_inicial = agendamento.horario_selecionado
            for servico in agendamento.servico.all():
                soma = somar_horarios(soma, servico.duracao_maxima_mulher.strftime('%H:%M'))
            horarios_ocupados.append([agendamento.dia_selecionado, horario_inicial.strftime('%H:%M'), somar_horarios(horario_inicial.strftime('%H:%M'), soma)])
        else:
            soma = '00:00'
            horario_inicial = agendamento.horario_selecionado
            for servico in agendamento.servico.all():
                soma = somar_horarios(soma, servico.duracao_maxima_homem.strftime('%H:%M'))
            horarios_ocupados.append([agendamento.dia_selecionado, horario_inicial.strftime('%H:%M'), somar_horarios(horario_inicial.strftime('%H:%M'), soma)])

    context = {
        'nome': cliente.nome_completo,
        'email': request.user.email,
        'servicos': servicos,
        'dias_funcionamento': salao.dias_funcionamento.all(),
        'horarios_ocupados': horarios_ocupados,
    }

    return render(request,'page/agendamento_cliente.html', context)

@login_required(login_url='login')
def visualizar_agendamento_pg_proprietario(request):
    agrupamentos = []
    novo_agrupamento = []

    for obj in Agendamento.objects.filter(proprietario=Proprietario.objects.get(user_id=request.user.id)):
        salao_id = obj.salao.id
        encontrado = False

        for grupo in agrupamentos:
            if salao_id in grupo:
                grupo[salao_id].append(obj)
                encontrado = True
                break

        if not encontrado:
            agrupamentos.append({salao_id: [obj]})
    
    for i in agrupamentos:
        for j in i.values():
            novo_agrupamento.append(j)

    context = {
        'agendamentos': novo_agrupamento,
        'dia_atual': obter_dia_atual(),
    }
    
    return render(request,'page/detalhes_agendamento_pg_proprietario.html', context)

@login_required(login_url='login')
def visualizar_agendamento_especifico(request, id):
    agendamento = Agendamento.objects.filter(salao=Salon.objects.get(pk=id))

    context = {
        'agendamento': agendamento,
        'dia_atual': obter_dia_atual(),
    }
    
    return render(request,'page/detalhes_agendamento_especifico.html', context)

@login_required(login_url='login')
def excluir_agendamento(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    agendamento.delete()

    if Agendamento.objects.filter(proprietario=Proprietario.objects.get(user_id=request.user.id)).count() == 0:
        messages.warning(request, 'Nenhum agendamento encontrado')
        return redirect('principal')

    messages.success(request, f'Agendamento de ( {agendamento.cliente.nome_completo.upper()} ) foi excluído')
    return redirect('detalhes-agendamento-proprietario')

@login_required(login_url='login')
def excluir_agendamento_especifico(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    agendamento.delete()

    if Agendamento.objects.filter(salao=agendamento.salao.id).count() == 0:
        messages.warning(request, f'Nenhum agendamento encontrado no salão ({agendamento.salao.nome_salao.upper()})')
        return redirect('principal')

    messages.success(request, f'Agendamento de ({agendamento.cliente.nome_completo.upper()}) foi excluído')
    return redirect('detalhes-agendamento-especifico', id=agendamento.salao.id)

@login_required(login_url='login')
def cancelar_agendamento(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    agendamento.delete()

    messages.success(request, f'Agendamento do salão ( {agendamento.salao.nome_salao.upper()} ) foi cancelado')
    return redirect('principal')

@login_required(login_url='login')
def cancelar_todos_agendamentos(request):
    agendamentos = Agendamento.objects.filter(cliente=Cliente.objects.get(user_id=request.user.id))
    
    for agendamento in agendamentos:
        agendamento.delete()

    messages.success(request, 'Todos os agendamentos foram cancelados')
    return redirect('principal')

@login_required(login_url='login')
def concluir_agendamento(request, id):
    agendamento = Agendamento.objects.get(pk=id)
    
    cache_agendamento = CacheAgendamentos(
        proprietario = agendamento.proprietario,
        cliente = agendamento.cliente,
        salao = agendamento.salao,
        idade = agendamento.idade,
        total_pagar = agendamento.total_pagar,
        dia_selecionado = agendamento.dia_selecionado,
        horario_selecionado = agendamento.horario_selecionado,
        data_concluido = date.today()
    )

    cache_agendamento.save()

    for i in agendamento.servico.all():
        cache_agendamento.servico.add(i)

    agendamento.delete()

    if Agendamento.objects.filter(salao=agendamento.salao.id).count() == 0:
        messages.warning(request, f'Nenhum agendamento encontrado no salão ({agendamento.salao.nome_salao.upper()})')
        return redirect('principal')

    messages.success(request, f'Agendamento de ({agendamento.cliente.nome_completo.upper()}) concluído no salão ({agendamento.salao.nome_salao.upper()})')
    return redirect('detalhes-agendamento-especifico', id=agendamento.salao.id)

@login_required(login_url='login')
def gerar_relatorio(request, id, index):
    salao = Salon.objects.get(pk=id)
    data = date.today()
    tipo = ''
    dados = []
    sub_dados = []
    servico_preferido = []
    total_servicos = 0
    renda = 0.0

    filtro = CacheAgendamentos.objects.filter(
        salao=salao,
        proprietario_id=Proprietario.objects.get(user_id=request.user.id).id,
    )

    # verifica se o agendamento passou de 1 ano, para excluir
    for obj in filtro:
        if subtrair_datas(data, obj.data_concluido) > 365:
            obj.delete()


    if index == 0:
        tipo = 'Diária'

        filtro = CacheAgendamentos.objects.filter(
            salao=salao,
            proprietario_id=Proprietario.objects.get(user_id=request.user.id).id,
            data_concluido=data
        )
    elif index == 1:
        tipo = 'Semanal'
        ids_filtrados = []

        filtro = CacheAgendamentos.objects.filter(
            salao=salao,
            proprietario_id=Proprietario.objects.get(user_id=request.user.id).id,
        )
        
        for obj in filtro:
            if subtrair_datas(data, obj.data_concluido) <= 7:
                ids_filtrados.append(obj.id)
        
        filtro = CacheAgendamentos.objects.filter(id__in=ids_filtrados)
    elif index == 2:
        tipo = 'Mensal'
        
        filtro = CacheAgendamentos.objects.filter(
            salao=salao,
            proprietario_id=Proprietario.objects.get(user_id=request.user.id).id,
            data_concluido__month=data.month
        )
    elif index == 3:
        tipo = 'Anual'

        filtro = CacheAgendamentos.objects.filter(
            salao=salao,
            proprietario_id=Proprietario.objects.get(user_id=request.user.id).id,
            data_concluido__year=data.year
        )
    else:
        return HttpResponseNotFound("A página solicitada não foi encontrada.")
    
    for obj in filtro:
        servicos = obj.servico.all()
        dados.append([
            obj.cliente.nome_completo,
            obj.idade,
            servicos.count(),
            obj.data_concluido,
            obj.total_pagar
        ])
        renda += obj.total_pagar
        for servico in servicos:
            total_servicos += 1
            servico_preferido.append(servico.servico)
    
    if len(servico_preferido) == 0:
        servico_preferido.append('Nenhum')

    sub_dados.append([
        filtro.count(),
        max(set(servico_preferido),key=servico_preferido.count),
        total_servicos,
        renda
    ])

    context = {
        'tipo': tipo,
        'proprietario': salao.proprietario.nome_completo,
        'cnpj': salao.proprietario.cnpj,
        'nome': salao.nome_salao,
        'cidade': salao.cidade,
        'rua': salao.rua,
        'bairro': salao.bairro,
        'pais': salao.pais,
        'numero': salao.numero,
        'data_atual': data,
        'hora': datetime.today().strftime('%H:%M'),
        'dados': dados,
        'sub_dados': sub_dados
    }
    
    return render(request, 'relatorio.html', context)

@login_required(login_url='login')
def limpar_cache(request, id, index):
    if index == 0:
        filtro = Salon.objects.filter(proprietario_id=Proprietario.objects.get(user_id=request.user.id))
        CacheAgendamentos.objects.filter(salao__in=filtro).delete()

        messages.success(request, 'Todo o cache de agendamentos foi exluído')
        return redirect('principal')
    else:
        salao = Salon.objects.get(pk=id)
        CacheAgendamentos.objects.filter(salao=salao).delete()

        messages.success(request, f'Todo o cache de agendamentos do salão ({salao.nome_salao.upper()}) foi exluído')
        return redirect('principal')

def aguardar(request):
    return render(request, 'page/detalhes_agendamento_especifico.html')

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

def obter_dia_atual():
    dias = {
        0: 'segunda-feira',
        1: 'terça-feira',
        2: 'quarta-feira',
        3: 'quinta-feira',
        4: 'sexta-feira',
        5: 'sabado',
        6: 'domingo'
    }

    return dias[date.today().weekday()]

def somar_horarios(horario1, horario2):
    formato = "%H:%M"
    tempo1 = datetime.strptime(horario1, formato).time()
    tempo2 = datetime.strptime(horario2, formato).time()

    soma = datetime.combine(datetime.min, tempo1) + timedelta(hours=tempo2.hour, minutes=tempo2.minute)

    return soma.time().strftime(formato)

def subtrair_datas(data1, data2):
    valor = data1 - data2
    return valor.days
