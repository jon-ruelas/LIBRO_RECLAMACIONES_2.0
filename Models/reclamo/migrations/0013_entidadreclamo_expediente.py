# Generated by Django 5.0.7 on 2024-07-31 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0012_alter_entidadreclamo_codigo_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidadreclamo',
            name='expediente',
            field=models.FileField(blank=True, null=True, upload_to='pdfs/'),
        ),
    ]
