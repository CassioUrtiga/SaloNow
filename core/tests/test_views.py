from model_mommy import mommy
from core.views import verificar_formato_email, decode_base64_image
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Cliente, Salon, Proprietario, DiasFuncionamento, Servicos
from core.forms import FormularioSalao
import datetime
from django.core.files.base import ContentFile
import tempfile

class VerificarFormatoEmailTestCase(TestCase):

    def test_verificar_formato_email_valido(self):
        email = 'exemplo@exemplo.com'
        resultado = verificar_formato_email(email)
        self.assertTrue(resultado)

    def test_verificar_formato_email_invalido(self):
        email = 'exemplo'
        resultado = verificar_formato_email(email)
        self.assertFalse(resultado)

class LogoutTestCase(TestCase):
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
        expected_url = reverse('login') + '?next=' + reverse('principal')
        self.assertRedirects(response, expected_url)

class CriarSalaoTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = mommy.make('auth.User')
        self.client.force_login(self.user)
        self.proprietario = mommy.make(Proprietario, user=self.user)
        self.url = reverse('criar-salao')
        self.salao = mommy.make(Salon)
        self.time = datetime.time(0, 0)
    
    def test_usuario_nao_autenticado(self):
        self.client.logout()
        response = self.client.post(self.url)
        expected_url = reverse('login') + '?next=' + reverse('criar-salao')
        self.assertRedirects(response, expected_url)

class SalaoImageTestCase(TestCase):
    def test_salao_imagem_salao_default(self):
        salao = mommy.make(Salon)
        self.assertEqual(salao.imagem_salao.name, 'fotos_salao/default.jpg')

    def test_salao_imagem_salao_upload(self):
        salao_status = ''
        salao = mommy.make(Salon)

        if salao_status == '':
            self.assertEqual(salao.imagem_salao.name, 'fotos_salao/default.jpg')
        else:
            imagem_decodificada = decode_base64_image(salao_status)
            with tempfile.NamedTemporaryFile(suffix='.jpeg', delete=False) as temp_file:
                imagem_decodificada.save(temp_file, format='JPEG')
                temp_file.seek(0)
                file_content = temp_file.read()

            content_file = ContentFile(file_content)
            salao.imagem_salao.save(temp_file.name, content_file)

            self.assertNotEqual(salao.imagem_salao.name, 'fotos_salao/default.jpg')

class ExcluirSalaoTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.proprietario = mommy.make(Proprietario, user=self.user)
        self.salon = mommy.make(Salon, proprietario=self.proprietario)
        self.url = reverse('excluir-salao', args=[self.salon.id])
    
    def test_usuario_nao_autenticado(self):
        self.client.logout()
        response = self.client.post(self.url)
        expected_url = reverse('login')
        expected_url += '?next=' + reverse('excluir-salao', args=[self.salon.id])
        self.assertRedirects(response, expected_url)

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

class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('carlos', 'carlos@gmail.com', 'carlospass')
        self.login_url = reverse('login')
    
    def testLogin(self):
        self.client.login(username='carlos', password='carlospass')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)    

    def test_login_view_post_failure(self):
        response = self.client.post(self.login_url, {'usuario': 'usuario_teste', 'senha': 'senha_incorreta'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'page_login/login.html')

    def test_login_view_post_invalid_password(self):
        self.user = User.objects.create_user(username='carlosvini', email='carlos@exemplo.com', password='password')
        login_data = {'usuario': 'carlos@exemplo.com', 'senha': 'wrongpassword'}
        response = self.client.post(reverse('login'), data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Usuário ou senha incorreta')
