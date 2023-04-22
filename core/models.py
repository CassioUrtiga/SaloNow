from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self) -> str:
        return self.nome_completo
    

class Proprietario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)
    cnpj = models.CharField(max_length=18, null=False)

    class Meta:
        verbose_name = 'proprietario'
        verbose_name_plural = 'proprietarios'

    def __str__(self) -> str:
        return self.nome_completo
