# Generated by Django 5.0.7 on 2024-07-31 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0016_alter_entidadreclamo_expediente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entidadreclamo',
            name='codigo_registro',
        ),
    ]
