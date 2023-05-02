from model_mommy import mommy
from core.views import verificar_formato_email
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from ..views import login_view
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from core.models import Cliente, Salon, Proprietario, DiasFuncionamento, Servicos
from core.forms import FormularioCliente, FormularioSalao
import datetime

class VerificarFormatoEmailTestCase(TestCase):

    def test_verificar_formato_email_valido(self):
        email = 'exemplo@exemplo.com'
        resultado = verificar_formato_email(email)
        self.assertTrue(resultado)

    def test_verificar_formato_email_invalido(self):
        email = 'exemplo'
        resultado = verificar_formato_email(email)
        self.assertFalse(resultado)

class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = mommy.make(User)
        self.client.force_login(self.user)
    
    def test_logout_view(self):
        response = self.client.get(reverse('deslogar'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inicio'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class TelaPrincipalTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = mommy.make(User)
        self.cliente = mommy.make(Cliente, user=self.user)
        self.salon = mommy.make(Salon)
        self.url = reverse('principal')

    def test_tela_principal(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('principal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page/principal.html')
        self.assertEqual(response.context['verificacao'], True)
        self.assertEqual(response.context['cliente'], self.cliente)
        self.assertEqual(response.context['proprietario'], None)
        self.assertQuerysetEqual(response.context['saloes'], Salon.objects.all())
        self.assertEqual(response.context['quantidade'], Salon.objects.all().count())

    def test_usuario_nao_autenticado(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, '/login/')

class CriarSalaoTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = mommy.make('auth.User')
        self.client.force_login(self.user)
        self.proprietario = mommy.make(Proprietario, user=self.user)
        self.url = reverse('criar-salao')
        self.salao = mommy.make(Salon)
        self.time = datetime.time(0, 0)
    
    def test_criar_salao_com_sucesso(self):
        form_data = {
            'nome_salao': 'Salão',
            'descricao': 'Descrição do salão',
            'salao_image': 'fotos_salao/default.jpg',
            'cidade': 'Sem local',
            'rua': 'Sem local',
            'pais': 'Sem local',
            'bairro': 'Sem local',
            'numero': 0,
            'segunda': ['segunda'],
            'temp_aberto_seg': self.time,
            'temp_fecha_seg': self.time,
            'terca': ['terca'],
            'temp_aberto_ter': self.time,
            'temp_fecha_ter': self.time,
            'quarta': ['quarta'],
            'temp_aberto_qua': self.time,
            'temp_fecha_qua': self.time,
            'quinta': ['quinta'],
            'temp_aberto_qui': self.time,
            'temp_fecha_qui': self.time,
            'sexta': ['sexta'],
            'temp_aberto_sex': self.time,
            'temp_fecha_sex': self.time,
            'sabado': ['sabado'],
            'temp_aberto_sab': self.time,
            'temp_fecha_sab': self.time,
            'domingo': ['domingo'],
            'temp_aberto_dom': self.time,
            'temp_fecha_dom': self.time,
            'servicos[]': ['Corte de cabelo', 'Manicure'],
        }
        form = FormularioSalao(data=form_data)
        self.assertTrue(form.is_valid())
        
        response = self.client.post(self.url, data=form_data, format='multipart')
        self.assertRedirects(response, reverse('principal'))
        
        
        self.assertEqual(self.salao.nome_salao, form_data['nome_salao'])
        self.assertEqual(self.salao.descricao, form_data['descricao'])
        self.assertEqual(self.salao.salao_image, form_data['salao_image'])
        self.assertEqual(self.salao.cidade, form_data['cidade'])
        self.assertEqual(self.salao.rua, form_data['rua'])
        self.assertEqual(self.salao.pais, form_data['pais'])
        self.assertEqual(self.salao.bairro, form_data['bairro'])
        self.assertEqual(self.salao.numero, form_data['numero'])

        dias_funcionamento = DiasFuncionamento.objects.all()
        self.assertEqual(len(dias_funcionamento), 7)
        for obj in dias_funcionamento:
            if obj.dia_semana == 'segunda':
                self.assertEqual(obj.abertura, form_data['temp_aberto_seg'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_seg'])
            elif obj.dia_semana == 'terca':
                self.assertEqual(obj.abertura, form_data['temp_aberto_ter'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_ter'])
            elif obj.dia_semana == 'quarta':
                self.assertEqual(obj.abertura, form_data['temp_aberto_qua'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_qua'])
            elif obj.dia_semana == 'quinta':
                self.assertEqual(obj.abertura, form_data['temp_aberto_qui'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_qui'])
            elif obj.dia_semana == 'sexta':
                self.assertEqual(obj.abertura, form_data['temp_aberto_sex'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_sex'])
            elif obj.dia_semana == 'sabado':
                self.assertEqual(obj.abertura, form_data['temp_aberto_sab'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_sab'])
            elif obj.dia_semana == 'domingo':
                self.assertEqual(obj.abertura, form_data['temp_aberto_dom'])
                self.assertEqual(obj.fechamento, form_data['temp_fecha_dom'])
        
        servicos = Servicos.objects.all()
        self.assertEqual(len(servicos), 2)
        for obj in servicos:
            self.assertIn(obj.servico, form_data['servicos[]'])
    
    def test_usuario_nao_autenticado(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, '/login/')

class ExcluirSalaoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = mommy.make('auth.User')
        self.user.set_password('password123')
        self.user.save()
        self.proprietario = mommy.make(Proprietario, user=self.user)
        self.salon = mommy.make(Salon, proprietario=self.proprietario)
        self.url = reverse('excluir-salao', args=[self.salon.id])
    
    def test_usuario_nao_autenticado(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertRedirects(response, '/login/')

    def test_usuario_autenticado(self):
        self.client.login(username=self.user.username, password='password123')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Salon.objects.filter(pk=self.salon.pk).exists())

class FiltrarSalaoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.cliente = mommy.make(Cliente, user=self.user)
        self.salon1 = mommy.make(Salon, cidade='São Paulo', bairro='Vila Mariana', rua='Rua Vergueiro', numero='100', pais='Brasil')
        self.salon2 = mommy.make(Salon, cidade='Rio de Janeiro', bairro='Copacabana', rua='Avenida Atlântica', numero='200', pais='Brasil')
        self.salon3 = mommy.make(Salon, cidade='Belo Horizonte', bairro='Savassi', rua='Rua Pernambuco', numero='300', pais='Brasil')

    def test_filtrar_salao(self):
        url = reverse('filtrar-salao')
        data = {'filtro': 'São Paulo, Vergueiro'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'São Paulo')
        self.assertContains(response, 'Vila Mariana')
        self.assertContains(response, 'Rua Vergueiro')
        self.assertContains(response, '100')
        self.assertNotContains(response, 'Rio de Janeiro')
        self.assertNotContains(response, 'Belo Horizonte')

class LoginTestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('carlos', 'carlos@gmail.com', 'carlospass')
        self.login_url = reverse('login')
    # Verifica se a página de login pode ser acessada com sucesso
    def testLogin(self):
        self.client.login(username='carlos', password='carlospass')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)    

    # Envia uma solicitação POST com usuário e senha inválidos
    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {'usuario': 'usuario_teste', 'senha': 'senha_incorreta'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page_login/login.html')

    def test_login_view_post_invalid_password(self):
        # cria um usuário com email válido e senha inválida
        user = User.objects.create_user(username='carlosvini', email='carlos@exemplo.com', password='password')

        # envia solicitação POST com senha incorreta
        login_data = {'usuario': 'carlos@exemplo.com', 'senha': 'wrongpassword'}
        response = self.client.post(reverse('login'), data=login_data, follow=True)

        # verifica se a resposta tem status code 200
        self.assertEqual(response.status_code, 200)

        # verifica se a mensagem de erro é exibida corretamente
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário ou senha incorreta')