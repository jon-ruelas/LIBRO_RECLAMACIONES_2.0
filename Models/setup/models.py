from django.db import models


class Entidad(models.Model):
    id = models.IntegerField,
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100, null=True)
    numero_reclamos = models.IntegerField(null=True)

    def __str__(self):
        return self.nombre
