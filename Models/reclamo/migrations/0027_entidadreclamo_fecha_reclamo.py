# Generated by Django 5.0.7 on 2024-08-20 20:56

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0026_remove_entidadreclamo_fecha_reclamo'),
    ]

    operations = [
        migrations.AddField(
            model_name='entidadreclamo',
            name='fecha_reclamo',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
