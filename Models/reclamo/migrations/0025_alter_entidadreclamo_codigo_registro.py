# Generated by Django 5.0.7 on 2024-08-07 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0024_alter_entidadreclamo_codigo_registro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidadreclamo',
            name='codigo_registro',
            field=models.CharField(editable=False, max_length=100, unique=True),
        ),
    ]
