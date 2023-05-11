import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django.dispatch import receiver
from django.db.models.signals import pre_delete


def get_file_path_profile(instance, filename):
    return os.path.join("fotos_perfil", f"{uuid.uuid4()}.{filename.split('.')[-1]}")

def get_file_path_salon(instance, filename):
    return os.path.join("fotos_salao", f"{uuid.uuid4()}.{filename.split('.')[-1]}")


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)
    foto_perfil = StdImageField('foto_perfil', upload_to=get_file_path_profile, variations={'thumbnail': (60, 60, True)}, default='fotos_perfil/default.png')

    class Meta:
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'

    def __str__(self) -> str:
        return self.nome_completo

@receiver(pre_delete, sender=Cliente)
def cliente_delete_img(sender, instance, **kwargs):
    if instance.foto_perfil and instance.foto_perfil.path:
        if os.path.basename(instance.foto_perfil.path) != 'default.png':
            if os.path.isfile(instance.foto_perfil.path):
                os.remove(instance.foto_perfil.path)
            instance.foto_perfil.delete_variations()

class Proprietario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=100, null=False)
    cnpj = models.CharField(max_length=18, null=False)
    foto_perfil = StdImageField('foto_perfil', upload_to=get_file_path_profile, variations={'thumbnail': (60, 60, True)}, default='fotos_perfil/default.png')

    class Meta:
        verbose_name = 'proprietario'
        verbose_name_plural = 'proprietarios'

    def __str__(self) -> str:
        return self.nome_completo

@receiver(pre_delete, sender=Proprietario)
def proprietario_delete_img(sender, instance, **kwargs):
    if instance.foto_perfil and instance.foto_perfil.path:
        if os.path.basename(instance.foto_perfil.path) != 'default.png':
            if os.path.isfile(instance.foto_perfil.path):
                os.remove(instance.foto_perfil.path)
            instance.foto_perfil.delete_variations()

class DiasFuncionamento(models.Model):
    dia_semana = models.CharField(max_length=20)
    abertura = models.TimeField(verbose_name='Horário de abertura')
    fechamento = models.TimeField(verbose_name='Horário de fechamento')

class Servicos(models.Model):
    servico = models.CharField(max_length=50)
    preco = models.FloatField(default=0.00)

class Salon(models.Model):
    proprietario = models.ForeignKey(Proprietario, on_delete=models.CASCADE)
    nome_salao = models.CharField(max_length=100, default='Salão')
    descricao = models.TextField(default='Descrição do salão')
    dias_funcionamento = models.ManyToManyField(DiasFuncionamento, verbose_name='dias_funcionamento')
    servico = models.ManyToManyField(Servicos, verbose_name='servicos')
    salao_image = StdImageField('salao_image', upload_to=get_file_path_salon, variations={'thumbnail': (700, 200, True)}, default='fotos_salao/default.jpg')
    cidade = models.CharField(max_length=30, default='Sem local')
    rua = models.CharField(max_length=100, default='Sem local')
    pais = models.CharField(max_length=30, default='Sem local')
    bairro = models.CharField(max_length=30, default='Sem local')
    numero = models.SmallIntegerField(default=0)
    
    def __str__(self) -> str:
        return self.nome_salao

@receiver(pre_delete, sender=Salon)
def salon_delete_img(sender, instance, **kwargs):
    if instance.salao_image and instance.salao_image.path:
        if os.path.basename(instance.salao_image.path) != 'default.jpg':
            if os.path.isfile(instance.salao_image.path):
                os.remove(instance.salao_image.path)
            instance.salao_image.delete_variations()
