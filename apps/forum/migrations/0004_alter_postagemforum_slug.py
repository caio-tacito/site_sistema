# Generated by Django 5.1.2 on 2024-11-30 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_postagemforum_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postagemforum',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
