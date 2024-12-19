from django.db.models import Count, Q
from django.shortcuts import render
from .models import Aprendices, Asistencias, Notificaciones, Usuario

def listar_aprendices_inasistentes(request):
    # Filtrar aprendices con más de 3 inasistencias
    aprendices_inasistentes = (
        Aprendices.objects.annotate(
            total_inasistencias=Count(
                'asistencias',
                filter=Q(asistencias__estado_asistencia__estado_asistencia='Inasistencia')
            )
        )
        .filter(total_inasistencias__gt=3)
    )

    # Crear notificaciones para el usuario logueado (puedes cambiar el rol si es necesario)
    for aprendiz in aprendices_inasistentes:
        mensaje = f"El aprendiz {aprendiz.nombres} {aprendiz.apellidos} tiene más de 3 inasistencias."
        Notificaciones.objects.get_or_create(
            usuario=request.Usuario,  # Cambiar si las notificaciones son para otro usuario
            mensaje=mensaje,
        )

    # Renderizar la lista de aprendices
    return render(request, 'listar_aprendices_inasistentes.html', {
        'aprendices_inasistentes': aprendices_inasistentes,
    })
