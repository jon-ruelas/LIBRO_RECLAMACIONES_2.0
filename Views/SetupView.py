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


def listar_entidad_por_id():
    ID_ENTIDADES = {
        1: ' C.S.M.C. BARRANCO ',
        2: ' C.S. GAUDENCIO BERNASCONI* ',
        3: ' C.S. ALICIA LASTRES DE LA TORR ',
        4: ' C.S. GUSTAVO LANATTA LUJAN ',
        5: ' C.M.I. VIRGEN DEL CARMEN ',
        6: ' P.S. ARMATAMBO ',
        7: ' C.E. SAN PEDRO DE LOS CHORRILLOS ',
        8: ' C.M.I. BUENOS AIRES DE VILLA ',
        9: ' C.S. DELICIAS DE VILLA ',
        10: ' C.S. SAN GENARO DE VILLA ',
        11: ' P.S. VISTA ALEGRE DE VILLA ',
        12: ' P.S. SANTA ISABEL DE VILLA ',
        13: ' C.S. TUPAC AMARU DE VILLA ',
        14: ' P.S. SAN JUAN DE LA LIBERTAD ',
        15: ' P.S. MATEO PUMACAHUA ',
        16: ' P.S. SANTA TERESA DE CHORRILLOS ',
        17: ' P.S. VILLA VENTURO ',
        18: ' P.S. NUEVA CALEDONIA ',
        19: ' P.S. LOS INCAS ',
        20: ' P.S. DEFENSORES DE LIMA ',
        21: ' C.S.M.C. SAN SEBASTIAN ',
        22: ' C.S.M.C. COMUNITARIO NANCY REYES BAHAMONETE ',
        23: ' C.S. SANTIAGO DE SURCO ',
        24: ' P.S. SAN CARLOS ',
        25: ' P.S. SAN ROQUE ',
        26: ' P.S. LOS VIÑEDOS DE SURCO ',
        27: ' P.S. LAS FLORES ',
        28: ' P.S. LAS DUNAS ',
        29: ' C.S. SAN JUAN DE MIRAFLORES ',
        30: ' P.S. DESIDERIO MOSCOSO CASTILLO ',
        31: ' P.S. VILLA SOLIDARIDAD ',
        32: ' P.S. VALLE SHARON ',
        33: ' P.S. PAMPAS DE SAN JUAN ',
        34: ' C.S. TREBOL AZUL ',
        35: ' P.S. HEROES DEL PACIFICO ',
        36: ' P.S. PARAISO ',
        37: ' P.S. SANTA URSULA ',
        38: ' P.S. RICARDO PALMA ',
        39: ' P.S. LADERAS DE VILLA ',
        40: ' C.S. VILLA SAN LUIS ',
        41: ' C.S. LEONOR SAAVEDRA ',
        42: ' C.S. JESUS PODEROSO ',
        43: ' P.S. EL BRILLANTE ',
        44: ' P.S. 6 DE JULIO ',
        45: ' C.M.I. MANUEL BARRETO ',
        46: ' P.S. VIRGEN DEL BUEN PASO ',
        47: ' P.S. SAN FRANCISCO DE LA CRUZ ',
        48: ' P.S. MARIANNE PREUSS DE STARK ',
        49: ' C.M.I. OLLANTAY ',
        50: ' P.S. LA RINCONADA ',
        51: ' P.S. LEONCIO PRADO ',
        52: ' P.S. JOSE M. ARGUEDAS ',
        53: ' P.S. 5 DE MAYO ',
        54: ' C.M.I. VILLA MARIA DEL TRIUNFO ',
        55: ' P.S. 12 DE JUNIO ',
        56: ' P.S. SANTA ROSA DE BELEN ',
        57: ' C.M.I. JOSE CARLOS MARIATEGUI ',
        58: ' P.S. VILLA LIMATAMBO ',
        59: ' P.S. JUAN CARLOS SOBERON ',
        60: ' P.S. BUENOS AIRES ',
        61: ' P.S. VALLE ALTO ',
        62: ' P.S. PARAISO ALTO ',
        63: ' C.S.M.C. 12 DE NOVIEMBRE ',
        64: ' P.S. VALLE BAJO ',
        65: ' C.M.I. JOSE GALVEZ ',
        66: ' P.S. MODULO I ',
        67: ' P.S. NUEVO PROGRESO ',
        68: ' P.S. CIUDAD DE GOSEN ',
        69: ' C.S. NUEVA ESPERANZA ',
        70: ' P.S. VIRGEN DE LOURDES ',
        71: ' P.S. CESAR VALLEJO II ',
        72: ' P.S. NUEVA ESPERANZA ALTA ',
        73: ' C.M.I.  DANIEL A. CARRION ',
        74: ' P.S. TORRES DE MELGAR ',
        75: ' P.S. MICAELA BASTIDAS ',
        76: ' C.M.I. TABLADA DE LURIN ',
        77: ' P.S. SANTA ROSA DE LAS CONCHITAS ',
        78: ' C.S.M.C. SAN GABRIEL ALTO ',
        79: ' *** CAM. TAYTA WASI ',
        80: ' P.S. DAVID GUERRERO DUARTE ',
        81: ' C.S.M.C. MOSEÑOR JOSE RAMON GURRUCHAGA ',
        82: ' C.M.I. SAN JOSE ',
        83: ' P.S. SEÑOR DE LOS MILAGROS ',
        84: ' P.S LLANAVILLA ',
        85: ' C.S.M.C. EL SOL DE VILLA ',
        86: ' C.S.M.C. VILLA EL SALVADOR ',
        87: ' C.S. SAN MARTIN DE PORRES ',
        88: ' P.S. VIRGEN DE LA ASUNCION ',
        89: ' P.S. SAGRADA FAMILIA ',
        90: ' C.M.I. JUAN PABLO II ',
        91: ' P.S.  FERNANDO LUYO SIERRA ',
        92: ' P.S. CRISTO SALVADOR ',
        93: ' P.S. SARITA COLONIA ',
        94: ' P.S. OASIS DE VILLA ',
        95: ' P.S. SASBI ',
        96: ' C.M.I.  CESAR LOPEZ SILVA ',
        97: ' P.S. PRINCIPE DE ASTURIAS ',
        98: ' P.S. PACHACAMAC ',
        99: ' P.S. EDILBERTO RAMOS ',
        100: ' C.S. HEROES DEL  CENEPA ',
        101: ' P.S. BRISAS DE PACHACAMAC ',
        102: ' C.M.I. LURIN ',
        103: ' P.S. BUENA VISTA ',
        104: ' CLAS JULIO C TELLO ',
        105: ' C.S. VILLA ALEJANDRO ',
        106: ' P.S. MARTHA MILAGROS BAJA ',
        107: ' C.S. NUEVO LURIN KM. 40 (CLAS) ',
        108: ' C.S.M.C. LA MEDALLA MILAGROSA ',
        109: ' C.S.M.C. SANTA ROSA DE MANCHAY ',
        110: ' C.S. PACHACAMAC ',
        111: ' P.S.VILLA LIBERTAD (CLAS) ',
        112: ' P.S. PAMPA GRANDE ',
        113: ' P.S. QUEBRADA VERDE ',
        114: ' P.S. GUAYABO ',
        115: ' P.S. PICA PIEDRA ',
        116: ' P.S. CARDAL ',
        117: ' P.S. MANCHAY ALTO ',
        118: ' P.S. TAMBO INGA ',
        119: ' C.S. PORTADA DE MANCHAY ',
        120: ' P.S. HUERTOS DE MANCHAY ',
        121: ' C.S. CLAS JUAN PABLO II ',
        122: ' P.S. COLLANAC ',
        123: ' P.S. PARQUES DE MANCHAY ',
        124: ' C.S. SAN BARTOLO ',
        125: ' C.S. PUCUSANA ',
        126: ' C.S. BENJAMIN DOIG ',
        127: ' P.S. PUNTA HERMOSA ',
        128: ' C.S. PUNTA NEGRA ',
        129: ' P.S. VILLA MERCEDES ',
        130: ' C.S.M.C VIRGEN DE LA MERCED ',
        131: ' C.S.M.C  CRL. SAN. WILELMO PEDRO ZORRILLA HUAMAN ',
        132: ' CSMC  BALNEARIOS DEL SUR ',
        133: ' PS.BELLA ESMERALDA ',
        134: ' CSMC RICARDO PALMA ',
        135: ' CSMC SAN PEDRO DE LURIN ',

    }

    dicc_id_entidad = ID_ENTIDADES
    return dicc_id_entidad


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
        entidad_id = request.POST.get("inputestablecimiento")
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
        context = {
            'entidad': listar_entidades(),
            'id_entidad': listar_entidad_por_id(),

            'entidad_id': entidad_id,
            'nombres_usuario': nombres_usuario,
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
