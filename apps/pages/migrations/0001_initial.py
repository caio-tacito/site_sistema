# Generated by Django 5.1.2 on 2024-12-08 13:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conteudo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, help_text='Nome do conteúdo para identificar na lista.', max_length=100, null=True)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='paginas/imagem/')),
                ('icone', models.CharField(blank=True, help_text='Codigo do Icon, Ex: fas fa-user', max_length=100, null=True)),
                ('cor_label', models.CharField(blank=True, help_text='Codigo do RGB, Ex: #FA4343', max_length=100, null=True)),
                ('titulo_1', models.CharField(blank=True, help_text='Titulo', max_length=100, null=True)),
                ('titulo_2', models.CharField(blank=True, help_text='Subtitulo', max_length=200, null=True)),
                ('descricao_1', models.CharField(blank=True, help_text='Descrição mais curta até 200 caracteres', max_length=200, null=True)),
                ('descricao_2', models.TextField(blank=True, help_text='Descrição mais longa', null=True)),
                ('titulo_botao_1', models.CharField(blank=True, help_text='Titulo do Botão 1', max_length=50, null=True)),
                ('rota_botao_1', models.CharField(blank=True, help_text='Nome da Rota que configurou no urls.py', max_length=50, null=True)),
                ('titulo_botao_2', models.CharField(blank=True, help_text='Titulo do Botão 2', max_length=50, null=True)),
                ('rota_botao_2', models.CharField(blank=True, help_text='Nome da Rota que configurou no urls.py', max_length=50, null=True)),
            ],
            options={
                'verbose_name': '2 - Conteúdo',
                'verbose_name_plural': '2 - Conteúdo',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Pagina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Digite o nome da pagina. Ex: Inicio, Contato...', max_length=100)),
            ],
            options={
                'verbose_name': '0 - Paginas',
                'verbose_name_plural': '0 - Paginas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='TipoBloco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(help_text='Digite o nome do bloco. Ex: SLIDE, BANNER_1...', max_length=100)),
            ],
            options={
                'verbose_name': '1 - Tipo de Bloco',
                'verbose_name_plural': '1 - Tipo de Bloco',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Blocos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordem', models.CharField(help_text='Ordem de exibição do bloco', max_length=3, null=True)),
                ('titulo', models.CharField(help_text='Titulo pode ser exibido no template', max_length=100)),
                ('descricao', models.TextField(blank=True, help_text='Descrição do bloco', null=True)),
                ('ativo', models.BooleanField(default=True)),
                ('conteudo', models.ManyToManyField(to='pages.conteudo')),
                ('pagina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagina_conteudo', to='pages.pagina')),
                ('bloco', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bloco_conteudo', to='pages.tipobloco')),
            ],
            options={
                'verbose_name': '3 - Blocos',
                'verbose_name_plural': '3 - Blocos',
                'ordering': ['id'],
            },
        ),
    ]