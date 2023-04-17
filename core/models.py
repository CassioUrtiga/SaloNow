from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)
    sobrenome = models.CharField(max_length=50, default=None)

    def __str__(self) -> str:
        return self.nome_completo
    

class Proprietario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)
    sobrenome = models.CharField(max_length=50, default=None)
    cnpj = models.CharField(max_length=18)

    def __str__(self) -> str:
        return self.nome_completo
    
