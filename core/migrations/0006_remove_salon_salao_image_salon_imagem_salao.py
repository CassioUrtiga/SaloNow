# Generated by Django 4.1.7 on 2023-05-22 16:10

import core.models
from django.db import migrations
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_cliente_cep_cliente_cidade_cliente_uf'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salon',
            name='salao_image',
        ),
        migrations.AddField(
            model_name='salon',
            name='imagem_salao',
            field=stdimage.models.StdImageField(default='fotos_salao/default.jpg', force_min_size=False, upload_to=core.models.get_file_path_salon, variations={}, verbose_name='imagem_salao'),
        ),
    ]