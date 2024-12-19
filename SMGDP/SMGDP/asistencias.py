
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Fichas, UnidadProgramacion, Aprendices, EstadoAsistencias, Asistencias, Usuario
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages  # Importa el sistema de mensajes
from django.shortcuts import render, get_object_or_404


@login_required
def preregistrar_asistencia(request, ficha_id, unidad_id):
    # Obtén la ficha y la unidad de programación usando los ID
    ficha = get_object_or_404(Fichas, numero=ficha_id)
    unidad_programacion = get_object_or_404(UnidadProgramacion, id=unidad_id)

    # Obtén los aprendices asociados a la ficha
    aprendices = Aprendices.objects.filter(ficha=ficha)

    # Obtén los estados de asistencia
    estados_asistencias = EstadoAsistencias.objects.all()

    # Renderiza el template con la información necesaria
    return render(request, 'Asistencias/RegistrarAsistencias.html', {
        'ficha': ficha,
        'unidad_programacion': unidad_programacion,
        'aprendices': aprendices,
        'estadoAsistencias': estados_asistencias,
    })


@login_required
def registrar_asistencia(request, ficha_id, unidad_id):
    ficha = get_object_or_404(Fichas, numero=ficha_id)
    unidad_programacion = get_object_or_404(UnidadProgramacion, id=unidad_id, ficha=ficha)
    aprendices = Aprendices.objects.filter(ficha=ficha)
    estado_asistencias = EstadoAsistencias.objects.all()

    # Obtener la jornada de la ficha
    jornada = ficha.jornada.nombre_jornada

    # Determinar la hora actual ajustada a la zona horaria
    hora_actual = timezone.now() - timedelta(hours=5)
    hora_actual_str = hora_actual.strftime("%H:%M")  # Formato de 24 horas HH:MM

    # Definir los rangos de hora por jornada
    if jornada == "MIXTA":
        # Jornada Mixta: 6:00 AM a 6:00 PM
        hora_inicio = "06:00"
        hora_fin = "18:00"
    elif jornada == "DIURNA":
        # Jornada Diurna: 6:00 AM a 12:00 PM
        hora_inicio = "06:00"
        hora_fin = "12:00"
    elif jornada == "NOCTURNA":
        # Jornada Nocturna: 6:00 PM a 10:00 PM
        hora_inicio = "18:00"
        hora_fin = "22:00"
    else:
        # Si la jornada no es válida, redirigimos o mostramos un error.
        return redirect('vistaFichasInstUnidadProgramacion')

    # Verificamos si la hora actual está dentro del rango permitido
    if not (hora_inicio <= hora_actual_str <= hora_fin):
        # Si no está dentro del rango, mostrar un mensaje de error específico
        mensaje_error = (
            f"La ficha {ficha.numero} no tiene permitido el registro de asistencias "
            f"a esta hora del día. Recuerda que la asistencia se debe tomar al iniciar "
            f"las clases de otros horarios."
        )
        # Usar el sistema de mensajes para pasar el error
        messages.error(request, mensaje_error)
        
        # Redirigir a la página de consultas o a donde desees después del error
        return redirect('vistaFichasInstUnidadProgramacion')  # Asegúrate de que la URL esté correctamente configurada

    if request.method == 'POST':
        observaciones = request.POST.get('observaciones', '')
        usuario = request.user  # Usuario que está realizando el registro

        for aprendiz in aprendices:
            estado_id = request.POST.get(f'asistencia_{aprendiz.id}')
            estado_asistencia = get_object_or_404(EstadoAsistencias, id=estado_id)

            # Crear y guardar la asistencia para cada aprendiz
            Asistencias.objects.create(
                usuario=usuario,
                fecha=hora_actual.date(),
                hora=hora_actual.time(),
                unidad_programacion=unidad_programacion,
                observaciones=observaciones,
                aprendiz=aprendiz,
                estado_asistencia=estado_asistencia
            )

        # Redirigir a otra página después de guardar
        return redirect('vistaFichasInstUnidadProgramacion')

    context = {
        'ficha': ficha,
        'unidad_programacion': unidad_programacion,
        'aprendices': aprendices,
        'estadoAsistencias': estado_asistencias,
    }
    return render(request, 'Asistencias/RegistrarAsistencias.html', context)




from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Fichas, Asistencias, Aprendices
from django.utils import timezone

def listar_asistencias_ficha(request, ficha_numero, unidad_id):
    # Obtener la ficha seleccionada
    ficha = get_object_or_404(Fichas, numero=ficha_numero)
    
    # Inicializar los filtros de fecha
    f_inicial = request.POST.get('f_inicial')
    f_fin = request.POST.get('f_fin')

    # Filtrar asistencias de aprendices para la ficha y unidad de programación específicas
    asistencias = Asistencias.objects.filter(aprendiz__ficha=ficha, unidad_programacion__id=unidad_id).select_related(
        'aprendiz', 'estado_asistencia', 'unidad_programacion'
    )
    
    # Aplicar el filtro de rango de fechas si ambos valores están presentes
    if f_inicial and f_fin:
        try:
            # Convertir las fechas en formato adecuado
            f_inicial = timezone.datetime.strptime(f_inicial, "%Y-%m-%d")
            f_fin = timezone.datetime.strptime(f_fin, "%Y-%m-%d")
            # Filtrar las asistencias por el rango de fechas
            asistencias = asistencias.filter(fecha__range=(f_inicial, f_fin))
        except ValueError:
            messages.error(request, "Las fechas proporcionadas no son válidas.")

    # Agrupar las asistencias por aprendiz
    asistencias_por_aprendiz = {}
    for asistencia in asistencias:
        aprendiz = asistencia.aprendiz
        if aprendiz not in asistencias_por_aprendiz:
            asistencias_por_aprendiz[aprendiz] = []
        asistencias_por_aprendiz[aprendiz].append(asistencia)

    context = {
        'ficha': ficha,
        'asistencias': asistencias_por_aprendiz
    }
    return render(request, 'Asistencias/ConsultarAsistencias.html', context)



def pre_editar_asistencia(request, asistencia_id):
    # Obtiene la asistencia específica del aprendiz
    asistencia = get_object_or_404(Asistencias, id=asistencia_id)

    # Obtiene todos los estados de asistencia
    estado_asistencias = EstadoAsistencias.objects.all()

    # Pasa los datos de la asistencia y los estados de asistencia al contexto
    context = {
        'asistencia': asistencia,
        'estadoAsistencias': estado_asistencias,  # Agregamos los estados de asistencia aquí
    }
    
    return render(request, 'Asistencias/EditarAsistencia.html', context)


def actualizar_asistencia(request, asistencia_id):
    # Obtiene la asistencia a través del id
    asistencia = get_object_or_404(Asistencias, id=asistencia_id)

    # Calcula la diferencia entre la fecha actual y la fecha de la asistencia
    diferencia_dias = (timezone.now().date() - asistencia.fecha).days

    # Verifica si han pasado más de 8 días
    if diferencia_dias > 8:
        # Si han pasado más de 8 días, se muestra un mensaje de error o se redirige
        mensaje_error = (
            f"la Asistencias no puede modificar por el tiempo limite de modificacion"
        )
        # Usar el sistema de mensajes para pasar el error
        messages.error(request, mensaje_error)
        return redirect('vistaFichasInstUnidadProgramacion')

    if request.method == 'POST':
        # Si el formulario es enviado, actualiza la asistencia
        estado_asistencia_id = request.POST.get(f'asistencia_{asistencia.aprendiz.id}')
        estado_asistencia = get_object_or_404(EstadoAsistencias, id=estado_asistencia_id)
        observaciones = request.POST.get('observaciones')

        # Actualiza la asistencia con los nuevos valores
        asistencia.estado_asistencia = estado_asistencia
        asistencia.observaciones = observaciones
        asistencia.save()

        # Redirige después de la actualización exitosa
        return redirect('listar_asistencias_ficha', ficha_numero=asistencia.unidad_programacion.ficha.numero, unidad_id=asistencia.unidad_programacion.id)

    # Si el método no es POST, renderiza el formulario con los datos actuales
    estado_asistencias = EstadoAsistencias.objects.all()
    context = {
        'asistencia': asistencia,
        'estadoAsistencias': estado_asistencias,
    }
    return render(request, 'Asistencias/EditarAsistencia.html', context)
