from django.db import models


class Entidadreclamo (models.Model):
    entidad_id = models.CharField(max_length=100)
    servicio_hecho_reclamo = models.CharField(max_length=100)

    tipo_documento_usuario = models.CharField(max_length=50)
    numero_documento_usuario = models.CharField(max_length=50)
    nombres_usuario = models.CharField(max_length=100)
    apellido_paterno_usuario = models.CharField(max_length=100)
    apellido_materno_usuario = models.CharField(max_length=100)
    correo_usuario = models.CharField(
        max_length=100)  # CREAR CAMPO EN BASE DE DATOS
    telefono_usuario = models.CharField(
        max_length=100)  # CREAR CAMPO EN BASE DE DATOS
    distrito_usuario = models.CharField(
        max_length=100)  # CREAR CAMPO EN BASE DE DATOS
    direccion_usuario = models.CharField(
        max_length=100)  # CREAR CAMPO EN BASE DE DATOS

    tipo_documento_presenta = models.CharField(max_length=50)
    numero_documento_presenta = models.CharField(max_length=50)
    nombres_presenta = models.CharField(max_length=100)
    apellido_paterno_presenta = models.CharField(max_length=100)
    apellido_materno_presenta = models.CharField(max_length=100)
    correo_presenta = models.CharField(max_length=100)
    celular_presenta = models.CharField(max_length=100)
    distrito_presenta = models.CharField(
        max_length=100)  # CREAR CAMPO EN BASE DE DATOS
    domicilio_presenta = models.CharField(max_length=100)

    detalle_reclamo = models.CharField(max_length=100)

    autorizacion_notificacion_correo = models.CharField(max_length=100)

    fecha_reclamo = models.DateTimeField(auto_now_add=True)

    codigo_registro = models.CharField(
        max_length=100, unique=True, editable=False)

    expediente = models.FileField(
        upload_to='pdfs/', blank=True, null=True)

    class Meta:
        db_table = 'reclamo_entidadreclamo_prueba'
