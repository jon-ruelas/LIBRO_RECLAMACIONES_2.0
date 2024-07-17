from django.db import models


class Entidad(models.Model):
    id = models.IntegerField,
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
