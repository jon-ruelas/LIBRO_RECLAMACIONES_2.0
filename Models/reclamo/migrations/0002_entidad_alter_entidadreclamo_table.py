# Generated by Django 4.1 on 2024-07-11 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reclamo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'setup_entidad',
            },
        ),
        migrations.AlterModelTable(
            name='entidadreclamo',
            table='reclamo_entidadreclamo',
        ),
    ]
