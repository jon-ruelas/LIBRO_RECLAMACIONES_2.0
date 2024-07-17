from email.message import EmailMessage
import os
from django.db import connection
from django.http import JsonResponse
import requests
from django.conf import settings
from django.template.loader import get_template

from django.core.mail import EmailMultiAlternatives

from Models.reclamo.models import Entidadreclamo
from newformulario import settings
from django.template.loader import render_to_string


from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage

from django_weasyprint import WeasyTemplateResponse
import pdfkit


def listar_entidades():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    # out_cur = django_cursor.connection.cursor()

    cursor.callproc("listar_entidad")

    lista = []
    for fila in cursor:
        lista.append(fila)

    return lista


def listar_tipo_documento():

    TIPOS_DOCUMENTO = {1: "DNI",
                       2: "CARNE DE EXTRANJERIA",
                       3: "PASAPORTE"}

    dicc_tipo_documento = TIPOS_DOCUMENTO

    return dicc_tipo_documento


def listar_tipo_servicio():
    SERVICIOS = {
        '01': 'CONSULTA EXTERNA',
        '02': 'HOSPITALIZACION',
        '03': 'EMERGENCIA',
        '04': 'CENTRO QUIRURGICO',
        '05': 'CENTRO OBSTÉTRICO',
        '06': 'UCI O UCIN',
        '07': 'FARMACIA',
        '08': 'SERVICIOS MEDICOS DE APOYO',
        '09': 'ATENCION A DOMICILIO CONSULTA AMBULATORIA',
        '10': 'ATENCION A DOMICILIO URGENCIA A EMERGENCIA',
        '11': 'OFICINAS O AREAS ADMINISTRATIVAS DE IAFAS A 1 IPRESS A UGIPRESS ',
        '12': 'INFRAESTRUCTURA',
        '13': 'REFERENCIA Y CONTRAREFERENCIA'
    }

    dicc_tipo_servicio = SERVICIOS

    return dicc_tipo_servicio


def listar_autorizacion_correo():
    AUTORIZACION = {
        0: "Sí autorizo que se me notifique el resultado del reclamo al email consignado",
        1: "No autorizo que se me notifique el resultado del reclamo al email consignado"
    }
    dicc_autorizacion = AUTORIZACION

    return dicc_autorizacion


def listar_distritos():
    DISTRITOS = {
        1: "Ancón",
        2: "Ate",
        3: "Barranco",
        4: "Breña",
        5: "Carabayllo",
        6: "Cercado de Lima",
        7: "Chaclacayo",
        8: "Chorrillos",
        9: "Cieneguilla",
        10: "Comas",
        11: "El agustino",
        12: "Independencia",
        13: "Jesús maría",
        14: "La molina",
        15: "La victoria",
        16: "Lince",
        17: "Los olivos",
        18: "Lurigancho",
        19: "Lurín",
        20: "Magdalena del mar",
        21: "Miraflores",
        22: "Pachacámac",
        23: "Pucusana",
        24: "Pueblo libre",
        25: "Puente piedra",
        26: "Punta hermosa",
        27: "Punta negra",
        28: "Rímac",
        29: "San bartolo",
        30: "San borja",
        31: "San isidro",
        32: "San Juan de Lurigancho",
        33: "San Juan de Miraflores",
        34: "San Luis",
        35: "San Martin de Porres",
        36: "San Miguel",
        37: "Santa Anita",
        38: "Santa María del Mar",
        39: "Santa Rosa",
        40: "Santiago de Surco",
        41: "Surquillo",
        42: "Villa el Salvador",
        43: "Villa Maria del Triunfo",
    }

    dicc_distritos = DISTRITOS
    return dicc_distritos


def obtener_dato(request):
    if request.method == 'POST':
        numero_documento_usuario = request.POST.get('inputdocumentousuario')
        # URL de la API externa
        api_url = 'https://previ.pe/previ/formularios/dniapi.php'

        # Hacer la solicitud a la API externa
        response = requests.post(
            api_url, data={'user_id': numero_documento_usuario})

        # Obtener el dato de la respuesta de la API externa
        if response.status_code == 200:
            data = response.json()
            dato_obtenido = data.get(
                'nombres', 'Dato no encontrado')
            dato_obtenido_2 = data.get(
                'apellidoPaterno')
            dato_obtenido_3 = data.get(
                'apellidoMaterno')

        else:
            dato_obtenido = 'Error al obtener el dato'

        return JsonResponse({'dato': dato_obtenido, 'dato2': dato_obtenido_2, 'dato3': dato_obtenido_3})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


def obtener_dato2(request):
    if request.method == 'POST':
        numero_documento_presenta = request.POST.get('inputdocumentopresenta')
        # URL de la API externa
        api_url = 'https://previ.pe/previ/formularios/dniapi.php'

        # Hacer la solicitud a la API externa
        response = requests.post(
            api_url, data={'user_id': numero_documento_presenta})

        # Obtener el dato de la respuesta de la API externa
        if response.status_code == 200:
            data = response.json()
            dato_obtenido = data.get(
                'nombres', 'Dato no encontrado')
            dato_obtenido_2 = data.get(
                'apellidoPaterno')
            dato_obtenido_3 = data.get(
                'apellidoMaterno')

        else:
            dato_obtenido = 'Error al obtener el dato'

        return JsonResponse({'dato': dato_obtenido, 'dato2': dato_obtenido_2, 'dato3': dato_obtenido_3})
    return JsonResponse({'error': 'Método no permitido'}, status=405)


"""
def send_email(mail):
    context = {'mail': mail

               }

    template = get_template('correo.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Asunto del correo',  # AQUI VA EL ASUNTO
        'Su documento pdf es este:',
        settings.EMAIL_HOST_USER,
        [mail]
    )

    email.attach_alternative(
        content, 'text/html')
    email.send()
"""

"""
def generate_pdf_and_send_email(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombres_usuario = request.POST.get('inputapellidopaterno', '')
        apellido = request.POST.get('inputapellidopaterno', '')
        correo = request.POST.get('inputcorreousuario', '')

        # Renderizar la plantilla HTML con los datos del formulario
        template = get_template('correo.html')
        html_content = template.render(
            {'inputnombreusuario': nombres_usuario, 'inputapellidopaterno': apellido, 'inputcorreousuario': correo})

        # Convertir la plantilla HTML a PDF
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
        }
        pdf = pdfkit.from_string(html_content, False, options=options)

        # Enviar el PDF por correo electrónico
        email_subject = 'Formulario en PDF'
        email_body = 'Adjunto encontrarás el formulario en formato PDF.'

        email = EmailMessage(email_subject, email_body,
                             'settings.EMAIL_HOST_USER', [correo])
        email.attach('formulario.pdf', pdf, 'application/pdf')
        email.send()

        return HttpResponse('El PDF fue generado y enviado correctamente por correo.')

    return render(request, 'formulario.html')
"""


def generate_pdf_and_send_email(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombres_usuario = request.POST.get('inputnombreusuario')
        apellido_paterno_usuario = request.POST.get('inputapellidopaterno')
        apellido_materno_usuario = request.POST.get('inputapellidomaterno')
        correo_usuario = request.POST.get("inputcorreousuario")
        direccion_usuario = request.POST.get('inputdireccionusuario')
        distrito_usuario = request.POST.get('inputdistritousuario')
        tipo_documento_usuario = request.POST.get("inputtipodocusuario")
        numero_documento_usuario = request.POST.get("inputdocumentousuario")
        telefono_usuario = request.POST.get("inputtelefonousuario")

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

        # Renderizar la plantilla HTML con los datos del formulario
        context = {'nombres_usuario': nombres_usuario,
                   'apellido_paterno_usuario': apellido_paterno_usuario,
                   'apellido_materno_usuario': apellido_materno_usuario,
                   'direccion_usuario': direccion_usuario,
                   'distrito_usuario': distrito_usuario,
                   'correo_usuario': correo_usuario,
                   'tipo_documento_usuario': tipo_documento_usuario,
                   'numero_documento_usuario': numero_documento_usuario,
                   'telefono_usuario': telefono_usuario,

                   'nombres_presenta': nombres_presenta,
                   'apellido_paterno_presenta': apellido_paterno_presenta,
                   'apellido_materno_presenta': apellido_materno_presenta,
                   'domicilio_presenta': domicilio_presenta,
                   'distrito_presenta': distrito_presenta,
                   'correo_presenta': correo_presenta,
                   'tipo_documento_presenta': tipo_documento_presenta,
                   'numero_documento_presenta': numero_documento_presenta,
                   'celular_presenta': celular_presenta,
                   'detalle_reclamo': detalle_reclamo,
                   'autorizacion_notificacion_correo': autorizacion_notificacion_correo,





                   }
        html_template = render_to_string('correo.html', context)

        # Convertir la plantilla HTML a PDF
        options = {
            'page-size': 'Letter',
            'encoding': 'UTF-8',
        }
        pdf = pdfkit.from_string(html_template, False, options=options)

        # Enviar el PDF por correo electrónico
        email_subject = 'Su reclamo fue ingresado'
        email_body = 'Se adjunto archivo pdf con el detalle de su reclamo a continuación:'

        email = EmailMessage(email_subject, email_body,
                             'settings.EMAIL_HOST_USER', [correo_usuario])
        email.attach('formulario.pdf', pdf, 'application/pdf')
        email.send()

        return HttpResponse('El PDF fue generado y enviado correctamente por correo.')

    return render(request, 'formulario.html')
