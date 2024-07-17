from email import message
from pyexpat.errors import messages
from django.contrib import messages

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template


from Models.reclamo.models import Entidadreclamo
from Views.SetupView import generate_pdf_and_send_email,  listar_autorizacion_correo, listar_distritos, listar_entidades, listar_tipo_documento, listar_tipo_servicio


class HomeView():

    def home(self):
        plantilla = get_template('index.html')
        return HttpResponse(plantilla.render())

    def pagina1(self):

        return HttpResponse('Hoal2')

    def pagina2(self, parametro1):
        return HttpResponse("HOLA DESDE PARAMETRO" + str(parametro1))

    def formulario(self):
        plantilla = get_template('formulario.html')
        return HttpResponse(plantilla.render())

    def registroReclamo(request):
        data = {
            'entidad': listar_entidades(),
            'tipo_documento': listar_tipo_documento(),
            'tipo_servicio': listar_tipo_servicio(),
            'autorizacion': listar_autorizacion_correo(),
            'distritos': listar_distritos(),



        }

        if (request.method == 'POST'):
            entidad_id = request.POST.get("inputestablecimiento")
            servicio_hecho_reclamo = request.POST.get("inputtiposervicio")

            tipo_documento_usuario = request.POST.get("inputtipodocusuario")
            numero_documento_usuario = request.POST.get(
                "inputdocumentousuario")
            nombres_usuario = request.POST.get("inputnombreusuario")
            apellido_paterno_usuario = request.POST.get("inputapellidopaterno")
            apellido_materno_usuario = request.POST.get("inputapellidomaterno")
            correo_usuario = request.POST.get("inputcorreousuario")
            # CREAR CAMPO EN BASE DE DATOS
            telefono_usuario = request.POST.get(
                "inputtelefonousuario")  # CREAR CAMPO EN BASE DE DATOS
            # CREAR CAMPO EN BASE DE DATOS
            distrito_usuario = request.POST.get(
                "inputdistritousuario")  # CREAR CAMPO EN BASE DE DATOS
            # CREAR CAMPO EN BASE DE DATOS
            direccion_usuario = request.POST.get(
                "inputdireccionusuario")  # CREAR CAMPO EN BASE DE DATOS
            # CREAR CAMPO EN BASE DE DATOS

            tipo_documento_presenta = request.POST.get("inputtipodocpresenta")
            numero_documento_presenta = request.POST.get(
                "inputdocumentopresenta")
            nombres_presenta = request.POST.get("inputusuario")
            apellido_paterno_presenta = request.POST.get(
                "inputapellidopaterno_presenta")
            apellido_materno_presenta = request.POST.get(
                "inputapellidomaterno_presenta")
            correo_presenta = request.POST.get("inputcorreopresenta")
            celular_presenta = request.POST.get("inputtelefonopresenta")
            distrito_presenta = request.POST.get(
                "inputdistritopresenta")  # CREAR CAMPO EN BASE DE DATOS
            # CREAR CAMPO EN BASE DE DATOS
            domicilio_presenta = request.POST.get("inputdireccionpresenta")

            detalle_reclamo = request.POST.get("detallereclamo")

            autorizacion_notificacion_correo = request.POST.get(
                "inputautoriza")

            Entidadreclamo(
                entidad_id=entidad_id,
                servicio_hecho_reclamo=servicio_hecho_reclamo,

                tipo_documento_usuario=tipo_documento_usuario,
                numero_documento_usuario=numero_documento_usuario,
                nombres_usuario=nombres_usuario,
                apellido_paterno_usuario=apellido_paterno_usuario,
                apellido_materno_usuario=apellido_materno_usuario,

                correo_usuario=correo_usuario,  # CREAR CAMPO EN BASE DE DATOS
                telefono_usuario=telefono_usuario,  # CREAR CAMPO EN BASE DE DATOS
                distrito_usuario=distrito_usuario,  # CREAR CAMPO EN BASE DE DATOS
                direccion_usuario=direccion_usuario,  # CREAR CAMPO EN BASE DE DATOS

                tipo_documento_presenta=tipo_documento_presenta,
                numero_documento_presenta=numero_documento_presenta,
                nombres_presenta=nombres_presenta,
                apellido_paterno_presenta=apellido_paterno_presenta,
                apellido_materno_presenta=apellido_materno_presenta,
                correo_presenta=correo_presenta,
                celular_presenta=celular_presenta,
                distrito_presenta=distrito_presenta,  # CREAR CAMPO EN BASE DE DATOS
                domicilio_presenta=domicilio_presenta,

                detalle_reclamo=detalle_reclamo,

                autorizacion_notificacion_correo=autorizacion_notificacion_correo,

            ).save()

            """send_email(correo_usuario)"""
            generate_pdf_and_send_email(request)

            messages.success(
                request, 'Se registró el reclamo correctamente.')

            return render(request, 'formulario.html', data)
        else:

            return render(request, 'formulario.html', data)
