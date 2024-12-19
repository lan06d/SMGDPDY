from django.shortcuts import render, redirect
from .models import Usuario, Programas, Jornadas, Fichas, UnidadProgramacion, Trimestre, Aprendices, EstadoAcademicoSofia, EstadoAsistencias, Asistencias, Quejas, Notificacion
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.utils import timezone


# inicio 

def inicio(request):
    return render(request, 'inicio/index.html')

def vistaRecuperacionClave(request):
    return render(request, 'inicio/recuperacionClave.html')

#usuarios 
@never_cache
@login_required
def vistaRegistroUsuarios(request):
    return render(request, 'usuarios/registroUsuarios.html')

@never_cache
@login_required
def VistaImportacion(request):
    return render(request, 'importaciones/importacionUser.html')


def buscar_usuarios(request, query):
    usuarios = Usuario.objects.all()
    if query:
        usuarios = usuarios.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(documento__icontains=query)
        )

        # Verifica si no hay resultados
        if not usuarios.exists():
            messages.error(request, "No se encontraron usuarios que coincidan con la búsqueda.")

    return usuarios


def paginar_usuarios(request, usuarios_list, elementos_por_pagina=10):
    page_number = request.GET.get('page')  # Obtiene el número de página de la URL
    paginator = Paginator(usuarios_list, elementos_por_pagina)
    return paginator.get_page(page_number)
@never_cache
@login_required
def VistaCoordinador(request):
    query = request.GET.get('buscar', '')  # Obtener el término de búsqueda
    usuarios = buscar_usuarios(request, query)  # Llamada a la función de búsqueda

    # Aplicar paginación a los usuarios encontrados
    paginator = Paginator(usuarios, 10)  # Cambia 10 al número de usuarios por página que desees
    page_number = request.GET.get('page')

    try:
        usuarios_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        usuarios_paginados = paginator.page(1)
    except EmptyPage:
        usuarios_paginados = paginator.page(paginator.num_pages)
    
    # Obtener notificaciones no leídas para el usuario actual
    notificaciones = Notificacion.objects.filter(usuario=request.user, leido=False)

    data = {
        'usuarios': usuarios_paginados,
        'query': query,  # Mantener el término de búsqueda en el contexto
        'notificaciones': notificaciones,
    }

    return render(request, 'coordinador/inicioCoordinador.html', data)

from django.shortcuts import get_object_or_404



def marcar_leido(request, notificacion_id):
    notificacion = get_object_or_404(Notificacion, id=notificacion_id)
    if notificacion.usuario == request.user:
        notificacion.leido = True
        notificacion.save()
    return redirect('VistaCoordinador')



#Programas 
@never_cache
@login_required
def vistaImportacionProgramas(request):
    return render(request, 'importaciones/importacionProgramas.html')

@never_cache
@login_required
def vistaProgramas(request):
    # Obtener el término de búsqueda desde el formulario (GET)
    busqueda = request.GET.get('buscar')

    # Si hay un término de búsqueda, filtrar los programas por 'nombre_programa'
    if busqueda:
        programas = Programas.objects.filter(nombre_programa__icontains=busqueda)
    else:
        programas = Programas.objects.all()

    # Configurar la paginación (5 programas por página)
    paginator = Paginator(programas, 15)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        page_obj = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera de rango, mostrar la última página de resultados
        page_obj = paginator.page(paginator.num_pages)

    # Pasar la búsqueda actual y los programas paginados al contexto
    context = {
        'programas': page_obj,
        'buscar': busqueda  # Para mantener el término de búsqueda en el input del formulario
    }

    return render(request, 'programas/ConsultarProgramas.html', context)


@never_cache
@login_required
def vistaRegistroProgramas(request):
    return render(request, 'programas/RegistroPrograma.html')

#jornadas 
from django.core.paginator import Paginator

def VistaJornadas(request):
    jornadas = Jornadas.objects.all()  
    paginator = Paginator(jornadas, 3)  
    
    page_number = request.GET.get('page')
    jornadas_page = paginator.get_page(page_number)  
    data = {
        "jornadas": jornadas_page  
    }
    return render(request, 'jornadas/ConsultarJornadas.html', data)
@never_cache
@login_required
def vistaRegistroJornadas(request):
    return render(request, 'jornadas/registroJornadas.html')

# Fichas 
@never_cache
@login_required
def vistaFichasIns(request):#Fichasinstructor
    return render(request, 'instrutor/ConsultasFichasInstructor.html')

def vistaRegistroFichas(request):
    programas = Programas.objects.all()
    jornadas = Jornadas.objects.all()
    
    context = {
        'programas': programas,
        'jornadas': jornadas,
    }
    
    return render(request, 'fichas/registroFichas.html', context)

@never_cache
@login_required
def vistaImportacioFichas(request):
    return render(request, 'importaciones/ImportacionFichas.html')

@never_cache
@login_required
def consultaFichas(request):
    buscar = request.GET.get('buscar', '')  # Obtiene el término de búsqueda
    fichas = Fichas.objects.all()

    # Filtrar fichas si se ingresó un término de búsqueda
    if buscar:
        fichas = fichas.filter(
            Q(numero__icontains=buscar) |
            Q(programa__nombre_programa__icontains=buscar) |
            Q(jornada__nombre_jornada__icontains=buscar)
        )

    # Paginación
    paginator = Paginator(fichas, 8) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'buscar': buscar  # Mantiene el término de búsqueda en el input
    }

    return render(request, 'fichas/consultasFichas.html', context)


from django.shortcuts import render, get_object_or_404
from .models import Usuario, UnidadProgramacion, Fichas

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UnidadProgramacion
from django.http import HttpRequest

@never_cache
@login_required
def vistaFichasInstUnidadProgramacion(request: HttpRequest):
    usuario = request.user

    # Obtener los filtros de la solicitud (si existen)
    unidad_nombre = request.GET.get('unidad_nombre', '')  # Filtrar por nombre de unidad
    ficha_numero = request.GET.get('ficha_numero', '')  # Filtrar por número de ficha

    # Filtrar las unidades de programación basadas en los parámetros de búsqueda
    unidades_programacion = UnidadProgramacion.objects.filter(usuario=usuario)

    if unidad_nombre:
        unidades_programacion = unidades_programacion.filter(unidad_programacion__icontains=unidad_nombre)
    
    if ficha_numero:
        unidades_programacion = unidades_programacion.filter(ficha__numero__icontains=ficha_numero)

    return render(request, 'instrutor/ConsultasFichasInstructor.html', {
        'unidades_programacion': unidades_programacion,
        'unidad_nombre': unidad_nombre,
        'ficha_numero': ficha_numero,
    })


# Unidad de Programacion 
@never_cache
@login_required
def consultaUnidadProgramacion(request):
    # Obtener el término de búsqueda de la URL
    buscar = request.GET.get('buscar', '')
    
    # Obtener todas las unidades de programación
    unidades = UnidadProgramacion.objects.all()

    # Filtrar por ficha, unidad de programación o usuario si hay un término de búsqueda
    if buscar:
        unidades = unidades.filter(
            Q(ficha__numero__icontains=buscar) | 
            Q(usuario__username__icontains=buscar)
        )

    # Configurar la paginación (por ejemplo, 5 unidades por página)
    paginator = Paginator(unidades, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'buscar': buscar  # Pasar el término de búsqueda al contexto
    }

    return render(request, 'unidadProgramacion/cosultarUnidadProgramacion.html', context)

@never_cache
@login_required
def VistaRegistoUnidadProgramacion(request):
    # Obtener todas las fichas y usuarios para llenar los select
    fichas = Fichas.objects.all()
    usuarios = Usuario.objects.all()
    

    context = {
        'fichas': fichas,
        'usuarios': usuarios,
    }

    return render(request, 'unidadProgramacion/RegistrarUnidad.html', context)

#Trimestres

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Trimestre

def buscar_trimestres(query):
    trimestres = Trimestre.objects.all()  # Obtener todos los trimestres
    if query:
        trimestres = trimestres.filter(
            Q(nombre_trimestre__icontains=query) |
            Q(fecha_inicio__icontains=query) |
            Q(fecha_fin__icontains=query)
        )
    return trimestres

@never_cache
@login_required
def VistaConsultarTrimestres(request):
    query = request.GET.get('buscar', '')  # Obtener el término de búsqueda
    trimestres = buscar_trimestres(query)  # Llamada a la función de búsqueda

    # Aplicar paginación a los trimestres encontrados
    paginator = Paginator(trimestres, 10)  # Cambia 10 al número de trimestres por página que desees
    page_number = request.GET.get('page')

    try:
        trimestres_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        trimestres_paginados = paginator.page(1)
    except EmptyPage:
        trimestres_paginados = paginator.page(paginator.num_pages)

    data = {
        'trimestres': trimestres_paginados,
        'query': query,  # Mantener el término de búsqueda en el contexto
    }

    return render(request, 'trimestre/consultarTrimestres.html', data)
@never_cache
@login_required
def VistaRegistroTrimestres(request):
    fichas = Fichas.objects.all()

    context = {
        'fichas': fichas,
    }
    return render(request, 'trimestre/registroTrimestres.html', context)





# Método para buscar estados académicos de Sofia
def buscar_estado_sofia(request):
    query = request.POST.get('buscar', '')
    estados = EstadoAcademicoSofia.objects.all()
    
    if query:
        estados = estados.filter(estado__icontains=query)
    
    return estados, query

# Método para paginar la lista de estados
def paginar_estado_sofia(request, estados):
    paginator = Paginator(estados, 10)  
    page = request.GET.get('page')
    
    try:
        estados_paginados = paginator.page(page)
    except PageNotAnInteger:
        estados_paginados = paginator.page(1)
    except EmptyPage:
        estados_paginados = paginator.page(paginator.num_pages)

    return estados_paginados

# Vista principal para consultar EstadoAcademicoSofia
@never_cache
@login_required
def ConsultarEstadoSofia(request):
    # Búsqueda
    estados, query = buscar_estado_sofia(request)
    
    # Paginación
    estados_paginados = paginar_estado_sofia(request, estados)

    # Contexto para pasar a la plantilla
    data = {
        'estados': estados_paginados,
        'query': query,
        'mensaje_no_encontrado': "No se encontraron estados académicos que coincidan con la búsqueda." if not estados.exists() else ""
    }

    return render(request, 'EstadoSofia/ConsultarEstado.html', data)

@never_cache
@login_required
def RegistroEstadoAcademicoSofia(request):
    return render(request, 'EstadoSofia/RegistrarEstado.html')

#Aprendices 
def buscar_aprendices(request):
    aprendices = Aprendices.objects.all()
    busqueda = request.POST.get('buscar')
    print("Valor de búsqueda:", busqueda)  # Depuración

    if busqueda:
        # Filtrar aprendices según los campos
        aprendices = aprendices.filter(
            Q(nombres__icontains=busqueda) | 
            Q(apellidos__icontains=busqueda) | 
            Q(correo__icontains=busqueda) | 
            Q(no_documento__icontains=busqueda)|
            Q(ficha__numero__icontains=busqueda)
        )

        # Verifica si no hay resultados
        if not aprendices.exists():
            messages.error(request, "No se encontraron aprendices que coincidan con la búsqueda.")

    return aprendices


# Método para paginar los aprendices
def paginar_aprendices(request, aprendices):
    paginator = Paginator(aprendices, 10)  
    page_number = request.GET.get('page')

    try:
        aprendices_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        aprendices_paginados = paginator.page(1)
    except EmptyPage:
        aprendices_paginados = paginator.page(paginator.num_pages)

    return aprendices_paginados

# Vista principal para consultar aprendices
@never_cache
@login_required
def ConsultarAprendices(request):
    # Realizar la búsqueda
    aprendices = buscar_aprendices(request)
    # Paginación
    aprendices_paginados = paginar_aprendices(request, aprendices)

    data = {
        'aprendices': aprendices_paginados,
    }

    return render(request, 'Aprendices/ConsultarAprendices.html', data)

@never_cache
@login_required
def RegistroAprendices(request):
    aprendices = Aprendices.objects.all()
    fichas = Fichas.objects.all()
    estadoAcademi = EstadoAcademicoSofia.objects.all()

    context = {
        'aprendiz':aprendices,
        'fichas': fichas,
        'estadoAcadenico' : estadoAcademi
    }
    return render(request, 'Aprendices/RegistroAprendices.html', context)


@never_cache
@login_required
def consultar_asistencias_Aprendiz(request, documento):
    aprendiz = get_object_or_404(Aprendices, no_documento=documento)
    asistencias = Asistencias.objects.filter(aprendiz=aprendiz).order_by('-fecha')
    
    # Contar las inasistencias con el estado "IES"
    inasistencias_count = asistencias.filter(estado_asistencia__estado_asistencia="I").count()

    return render(request, 'Aprendices/CosultarAsistenciaAprendiz.html', {
        'aprendiz': aprendiz,
        'asistencias': asistencias,
        'inasistencias_count': inasistencias_count
    })
 
 
@never_cache
@login_required
def listar_aprendices_ficha(request, ficha_numero, unidad_id):
    # Obtener la ficha y la unidad de programación
    ficha = get_object_or_404(Fichas, numero=ficha_numero)
    unidad = get_object_or_404(UnidadProgramacion, id=unidad_id)

    # Obtener los aprendices relacionados con la ficha
    aprendices = Aprendices.objects.filter(ficha=ficha)

    context = {
        'ficha': ficha,
        'unidad': unidad,
        'aprendices': aprendices
    }
    return render(request, 'instrutor/aprendices.html', context)


#Estado Asistencia
@never_cache
@login_required
def ConsultarEstadoAsistencia(request):
    # Obtiene el término de búsqueda desde el formulario
    query = request.GET.get('buscar', '')
    # Realiza la búsqueda en el modelo EstadoAsistencias
    estados = EstadoAsistencias.objects.all()
    if query:
        estados = estados.filter(estado_asistencia__icontains=query)

    # Configura la paginación
    paginator = Paginator(estados, 10)  # Muestra 10 resultados por página
    page_number = request.GET.get('page')
    
    try:
        estados_paginados = paginator.page(page_number)
    except PageNotAnInteger:
        estados_paginados = paginator.page(1)
    except EmptyPage:
        estados_paginados = paginator.page(paginator.num_pages)

    # Configura el contexto con la paginación y el término de búsqueda
    context = {
        'estados': estados_paginados,
        'buscar': query,
        'no_resultados': not estados.exists() and query,  # Verifica si hay resultados y si se ha hecho una búsqueda
    }

    return render(request, 'EstadoAsistencia/ConsultarEstado.html', context)


@never_cache
@login_required
def VistaRegistroEstadoAsistencia(request):
    return render(request, 'EstadoAsistencia/RegistrarEstado.html') 




#Asistencia 
@never_cache
@login_required
def ConsultarAsistencias(request):
    return render(request, 'Asistencias/ConsultarAsistencias.html')


@never_cache
@login_required
def VistaRegistroAsistencias(request):
    return render(request, 'Asistencias/RegistrarAsistencias.html')



#Quejas
@never_cache
@login_required
def ConsultarQuejas(request):
 # Consultar todas las quejas
    quejas_list = Quejas.objects.all()  # Ordenamos por fecha de registro

    # Paginación
    paginator = Paginator(quejas_list, 10)  # Mostrar 10 quejas por página
    page_number = request.GET.get('page')
    quejas_page = paginator.get_page(page_number)

    return render(request, 'Quejas/ConsultarQuejas.html', {
        'quejas': quejas_page,
    })


def detalle_queja(request, queja_id):
    queja = get_object_or_404(Quejas, id=queja_id)
    return render(request, 'Quejas/DetalleQueja.html', {
        'queja': queja,
    })

@never_cache
@login_required
def vistaRegistroQuejas(request):
    programas = Programas.objects.all()
    jornadas = Jornadas.objects.all()
    aprendiz = Aprendices.objects.all()
    
    context = {
        'programas': programas,
        'jornadas': jornadas,
    }
    return render (request, 'Quejas/RegistroQuejas.html', context)

@never_cache
@login_required
def vistaInstruRegistroquejas(request):
    programas = Programas.objects.all()
    jornadas = Jornadas.objects.all()
    aprendiz = Aprendices.objects.all()
    
    context = {
        'programas': programas,
        'jornadas': jornadas,
    }
    return render (request, 'Quejas/InstruRegistroquejas.html', context)

#Evidencias de Quejas 
@never_cache
@login_required
def ConsultarEvidenciaQuejas(request):
    return render(request, 'EvidenciasQuejas/ConsultarEvidenciasQ.html')


@never_cache
@login_required
def VistaRegistrarEvidenciasQuejas(request):
    return render(request, 'EvidenciasQuejas/RegistroEvidenciasQ.html')

 #Observaciones Extra de las quejas 
@never_cache
@login_required
def ConsultarObservacionesEstrasQuejas(request):
    return render(request, 'ObservacionExtraQuejas/ConsultarObservacionesExtraQ.html')

@never_cache
@login_required
def VistaRegistroObservacionExtraQueja(request):
    return render(request, 'ObservacionExtraQuejas/RegistraObseravacinesExtraQ.html')
 

#Novedad del comite 
@never_cache
@login_required
def ConsultarNovedaComite(request):
    return render(request, 'NovedadComite/ConsultarNovedadC.html')

@never_cache
@login_required
def VistaRegistroNovedadComite(request):
    return render(request, 'NovedadComite/RegistrarNovedadC.html')

#Enviar correos 
@never_cache
@login_required
@login_required
def EnviarCorreosInstru(request):
    return render(request, 'instrutor/EnviarCorreos.html')

#Copia de seguridad 
@never_cache
@login_required
def vista_backup_restore(request):
    return render(request, 'BackupRestore/backupRestore.html')

#Vista Configuracion
@never_cache
@login_required
def VistaConfiguracion(request):
    return render(request, 'Configuracion/GestionAdmin.html')


