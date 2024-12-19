from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Usuario, Aprendices, UnidadProgramacion
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import (Fichas, Trimestre, EstadoAsistencias, Asistencias, Quejas, Programas, Jornadas, EstadoAcademicoSofia,
                     EvidenciaQueja, ObservacionesExtraQuejas, ObservacionBienestar, NovedadComite)

#Usuario
def eliminar_usuario(request, id):
    usuario = get_object_or_404(Usuario, id=id)
    usuario.delete()
    messages.success(request, f"El usuario {usuario.username} ha sido eliminado exitosamente.")
    return redirect('VistaCoordinador')  # Cambia esto al nombre de tu vista de listado de usuarios
#Aprendiz
def eliminarAprendiz(request, id):
    aprendiz = get_object_or_404(Aprendices, id=id)
    aprendiz.delete()
    messages.success(request, f"El aprendiz {aprendiz.nombres} ha sido eliminado del sistema ")
    return redirect('ConsultarAprendices')

#Programas 
def eliminarProgramas(request, id):
    programas = get_object_or_404(Programas, id=id)
    programas.delete()
    messages.success(request, f"Se elimino el programa" )
    return redirect('vistaProgramas')

#Jornadad 
def ElminiarJornadas(request, id):
    jornadas = get_object_or_404(Jornadas, id=id)
    jornadas.delete()
    messages.success(request, f'Se elimino la jornada')
    return redirect('VistaJornadas')

#Unidad De programacion
def eliminarUnidadProgramacion(request, id):
    unidadpro = get_object_or_404(UnidadProgramacion, id=id)
    unidadpro.delete()
    messages.success(request, f"La unidad de programacion se ha eliminado del sistema" )
    return redirect('consultaUnidadProgramacion')



# Ficha
def eliminar_ficha(request, id):
    ficha = get_object_or_404(Fichas, numero=id)
    ficha.delete()
    messages.success(request, f"La ficha ha sido eliminada exitosamente.")
    return redirect('consultaFichas')  # Cambia esto al nombre de tu vista de listado de fichas

#EstadoAcademico 
def EliminarEstadoAcadmico(request, id):
    estadoAcademico = get_object_or_404(EstadoAcademicoSofia, id=id)
    estadoAcademico.delete()
    messages.success(request, f'Se elimino el estado academico')
    return redirect('ConsultarEstadoSofia')
    
    
# Estado de Asistencias
def eliminar_estado_asistencia(request, id):
    estado_asistencia = get_object_or_404(EstadoAsistencias, id=id)
    estado_asistencia.delete()
    messages.success(request, f"El estado de asistencia {estado_asistencia.estado_asistencia} ha sido eliminado.")
    return redirect('ConsultarEstadoAsistencia')  # Cambia esto al nombre de tu vista de listado de estados

# Asistencias

# Quejas

# Evidencia de Quejas
def eliminar_evidencia_queja(request, id):
    evidencia = get_object_or_404(EvidenciaQueja, id=id)
    evidencia.delete()
    messages.success(request, "La evidencia de la queja ha sido eliminada.")
    return redirect('ConsultarQuejas')  # Cambia esto al nombre de tu vista de listado de evidencias

# Observaciones Extras de Quejas
def eliminar_observacion_extra(request, id):
    observacion = get_object_or_404(ObservacionesExtraQuejas, id=id)
    observacion.delete()
    messages.success(request, "La observación extra ha sido eliminada.")
    return redirect('ConsultarEvidenciaQuejas')  # Cambia esto al nombre de tu vista de listado de observaciones

# Observación de Bienestar

# Novedad del Comité
def eliminar_novedad_comite(request, id):
    novedad = get_object_or_404(NovedadComite, id=id)
    novedad.delete()
    messages.success(request, "La novedad del comité ha sido eliminada.")
    return redirect('ConsultarNovedaComite')  # Cambia esto al nombre de tu vista de listado de novedades
