from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=14, primary_key=True)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.nome
    

class Proprietario(models.Model):
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, primary_key=True)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.nome
    
