# Generated by Django 5.0.7 on 2024-07-31 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0013_entidadreclamo_expediente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entidadreclamo',
            name='expediente',
            field=models.FileField(blank=True, null=True, upload_to='C:/Users/DIRISLS/Desktop/Trabajo Ruelas/RECLAMACIONES/media'),
        ),
    ]
