# Generated by Django 4.1.7 on 2023-04-22 23:27

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import stdimage.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiasFuncionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia_semana', models.CharField(max_length=20)),
                ('abertura', models.TimeField(verbose_name='Horário de abertura')),
                ('fechamento', models.TimeField(verbose_name='Horário de fechamento')),
            ],
        ),
        migrations.CreateModel(
            name='Proprietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100)),
                ('cnpj', models.CharField(max_length=18)),
                ('foto_perfil', stdimage.models.StdImageField(default='fotos_perfil/default.thumbnail.png', force_min_size=False, upload_to=core.models.get_file_path_profile, variations={'thumbnail': (60, 60, True)}, verbose_name='foto_perfil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'proprietario',
                'verbose_name_plural': 'proprietarios',
            },
        ),
        migrations.CreateModel(
            name='Servicos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servico', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_salao', models.CharField(default='Salão', max_length=100)),
                ('descricao', models.TextField(default='Descrição do salão')),
                ('salao_image', stdimage.models.StdImageField(default='fotos_salao/default.thumbnail.jpg', force_min_size=False, upload_to=core.models.get_file_path_salon, variations={'thumbnail': (700, 200, True)}, verbose_name='salao_image')),
                ('dias_funcionamento', models.ManyToManyField(to='core.diasfuncionamento', verbose_name='dias_funcionamento')),
                ('proprietario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.proprietario')),
                ('servico', models.ManyToManyField(to='core.servicos', verbose_name='servicos')),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_completo', models.CharField(max_length=100)),
                ('foto_perfil', stdimage.models.StdImageField(default='fotos_perfil/default.thumbnail.png', force_min_size=False, upload_to=core.models.get_file_path_profile, variations={'thumbnail': (60, 60, True)}, verbose_name='foto_perfil')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
    ]
