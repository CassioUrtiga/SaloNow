from model_mommy import mommy
from core.views import verificar_formato_email
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User

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



