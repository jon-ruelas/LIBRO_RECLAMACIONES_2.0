# Generated by Django 5.0.7 on 2024-07-31 20:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0021_alter_entidadreclamo_codigo_registro'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entidadreclamo',
            name='codigo_registro',
        ),
    ]
