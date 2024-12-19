from django.urls import path
from . import views, imporExpor, registros, loginLagout, editar, eliminar, asistencias, enviarcorreos,  backupRestore, ActualizarClave

urlpatterns = [
    
    path('', views.inicio, name='inicio'),
    path('vistaRecuperacionClave', views.vistaRecuperacionClave, name='vistaRecuperacionClave'),
    path('vistaRegistroUsuarios', views.vistaRegistroUsuarios, name='vistaRegistroUsuarios'),
    path('vistaFichasIns', views.vistaFichasIns, name='vistaFichasIns'),
    #sesiones
    #path('iniciar_sesion', loginLagout.iniciar_sesion, name='iniciar_sesion'),
    path('accounts/login/', loginLagout.iniciar_sesion, name='iniciar_sesion'),
    path('VistaCoordinador', views.VistaCoordinador, name='VistaCoordinador'),
    #Recuperacion de contraseña 
    path('recuperacion_contraseña', enviarcorreos.recuperacion_contraseña, name='recuperacion_contraseña'),
    #Enviar Correos 
    path('EnviarCorreosInstru', views.EnviarCorreosInstru, name='EnviarCorreosInstru'),
    path('enviar_correo', enviarcorreos.enviar_correo, name='enviar_correo'),
    #cerrar sesiones
    path('cerrar_sesion', loginLagout.cerrar_sesion, name='cerrar_sesion'),
    # Vistas Importacion 
    path('VistaImportacion', views.VistaImportacion, name='VistaImportacion'),
    path('import_csv', imporExpor.import_csv, name='import_csv'),
    path('vistaImportacioFichas', views.vistaImportacioFichas ,name='vistaImportacioFichas'),
    path('vistaImportacionProgramas', views.vistaImportacionProgramas, name='vistaImportacionProgramas'),
    path('importar_unidad_programacion', imporExpor.importar_unidad_programacion, name='importar_unidad_programacion'),
    path('importarAprendices', imporExpor.importarAprendices, name='importarAprendices'),
    #
    path('vista_backup_restore', views.vista_backup_restore, name='vista_backup_restore'),
    path('backup/', backupRestore.backup, name='backup'),
    path('restore/', backupRestore.restore, name='restore'),
    path('restore/<str:filename>/', backupRestore.restore_file, name='restore_file'),
    #Configuracion
    path('VistaConfiguracion', views.VistaConfiguracion, name='VistaConfiguracion'),
    #usuarios
    path('perfil/cambiar-contrasena/', ActualizarClave.CambiarContrasena, name='CambiarContrasena'),
    path('PreEditarPerfil',editar.PreEditarPerfil, name='PreEditarPerfil'),
    path('ActualizarPerfil',editar.ActualizarPerfil, name='ActualizarPerfil'),
    path('RegistroUsuarios', registros.RegistroUsuarios, name='RegistroUsuarios'),
    path('PreEditarUsuarios/<int:id>/', editar.PreEditarUsuarios, name='PreEditarUsuarios'),
    path('ActualizarUsuarios/<int:id>/', editar.ActualizarUsuarios, name='ActualizarUsuarios'),
    path('eliminar_usuario/<int:id>/', eliminar.eliminar_usuario, name='eliminar_usuario'),
    # Metodos importacion 
    path('ImportacionFicha', imporExpor.ImportacionFicha, name='ImportacionFicha'),
    path('importacioProgramas', imporExpor.importacioProgramas, name='importacioProgramas'),
    # Programas 
    path('vistaProgramas', views.vistaProgramas, name='vistaProgramas'),
    path('vistaRegistroProgramas', views.vistaRegistroProgramas, name='vistaRegistroProgramas'),
    path('RegistroPrograma', registros.RegistroPrograma, name='RegistroPrograma'),
    path('eliminarProgramas/<int:id>/', eliminar.eliminarProgramas, name='eliminarProgramas'),
    path('EditarPrograma<int:programa_id>', editar.EditarPrograma,name='EditarPrograma'),
    # jornadas
    path('VistaJornadas', views.VistaJornadas, name='VistaJornadas'),
    path('vistaRegistroJornadas', views.vistaRegistroJornadas, name='vistaRegistroJornadas'),
    path('RegistroJornada', registros.RegistroJornada, name='RegistroJornada'),
    path('ElminiarJornadas/<int:id>/', eliminar.ElminiarJornadas, name='ElminiarJornadas'),
    # Fichas 
    path('vistaRegistroFichas', views.vistaRegistroFichas, name='vistaRegistroFichas'),
    path('consultaFichas', views.consultaFichas, name='consultaFichas'),
    path('RegistroFichas', registros.RegistroFichas, name='RegistroFichas'),
    path('vistaFichasInstUnidadProgramacion', views.vistaFichasInstUnidadProgramacion, name='vistaFichasInstUnidadProgramacion'),
    path('EditarFicha/<int:ficha_id>/', editar.EditarFicha, name='EditarFicha'),
    path('eliminar_ficha/<int:id>/', eliminar.eliminar_ficha, name='eliminar_ficha'),
    # Unidad de Programacion
    path('consultaUnidadProgramacion', views.consultaUnidadProgramacion, name='consultaUnidadProgramacion'),
    path('VistaRegistoUnidadProgramacion', views.VistaRegistoUnidadProgramacion, name='VistaRegistoUnidadProgramacion'),
    path('RegistroUnidadProgramacion', registros.RegistroUnidadProgramacion, name='RegistroUnidadProgramacion'),
    path('EditarUnidadProgramacion/<int:unidad_id>/', editar.EditarUnidadProgramacion, name='EditarUnidadProgramacion'),
    path('eliminarUnidadProgramacion/<int:id>/', eliminar.eliminarUnidadProgramacion, name='eliminarUnidadProgramacion'),
    # Trimestre
    path('VistaConsultarTrimestres', views.VistaConsultarTrimestres, name='VistaConsultarTrimestres'),
    path('VistaRegistroTrimestres', views.VistaRegistroTrimestres, name='VistaRegistroTrimestres'),
    path('RegistroTrimestres', registros.RegistroTrimestres, name='RegistroTrimestres'),
    #Estado Academico Sofia 
    path('ConsultarEstadoSofia', views.ConsultarEstadoSofia, name='ConsultarEstadoSofia'),
    path('RegistroEstadoAcademicoSofia', views.RegistroEstadoAcademicoSofia, name='RegistroEstadoAcademicoSofia'),
    path('RegistroEstadosAcademicos', registros.RegistroEstadosAcademicos, name='RegistroEstadosAcademicos'),
    path('EliminarEstadoAcadmico/<int:id>/', eliminar.EliminarEstadoAcadmico, name='EliminarEstadoAcadmico'),
    #Aprendices
    path('ConsultarAprendices', views.ConsultarAprendices, name='ConsultarAprendices'),
    path('RegistroAprendices', views.RegistroAprendices, name='RegistroAprendices'),
    path('RegistroRegistroAprendices', registros.RegistroRegistroAprendices, name='RegistroRegistroAprendices'),
    path('consultar_asistencias_Aprendiz/<str:documento>/asistencias/', views.consultar_asistencias_Aprendiz, name='consultar_asistencias_Aprendiz'),
    path('listar-aprendices/<int:ficha_numero>/<int:unidad_id>/', views.listar_aprendices_ficha, name='listar_aprendices'),
    path('PreEditarAprendiz/<int:id>/', editar.PreEditarAprendiz, name='PreEditarAprendiz'),
    path('ActualizarAprendix/<int:id>/', editar.ActualizarAprendix, name='ActualizarAprendix'),
    path('eliminarAprendiz/<int:id>/', eliminar.eliminarAprendiz, name='eliminarAprendiz'),
    #Estado de Asistencia
    path('ConsultarEstadoAsistencia', views.ConsultarEstadoAsistencia, name='ConsultarEstadoAsistencia'),
    path('VistaRegistroEstadoAsistencia', views.VistaRegistroEstadoAsistencia, name='VistaRegistroEstadoAsistencia'),
    path('RegistroEstadoAsistencia', registros.RegistroEstadoAsistencia, name='RegistroEstadoAsistencia'),
    path('eliminar_estado_asistencia/<int:id>/', eliminar.eliminar_estado_asistencia, name='eliminar_estado_asistencia'),
    #Asistencia
    path('ConsultarAsistencias', views.ConsultarAsistencias, name='ConsultarAsistencias'),
    path('VistaRegistroAsistencias', views.VistaRegistroAsistencias, name='VistaRegistroAsistencias'),
    path('preregistrar_asistencia/<str:ficha_id>/<int:unidad_id>/', asistencias.preregistrar_asistencia, name='preregistrar_asistencia'),
    path('listar_asistencias_ficha/<str:ficha_numero>/<int:unidad_id>/', asistencias.listar_asistencias_ficha, name='listar_asistencias_ficha'),
    path('registrar-asistencia/<str:ficha_id>/<int:unidad_id>/', asistencias.registrar_asistencia, name='registrar_asistencia'),
    path('pre_editar_asistencia/editar/<int:asistencia_id>/', asistencias.pre_editar_asistencia, name='PreEditarAsistencia'),
    path('actualizar_asistencia/editar/<int:asistencia_id>/', asistencias.actualizar_asistencia, name='actualizar_asistencia'),
    #Quejas
    path('ConsultarQuejas', views.ConsultarQuejas, name='ConsultarQuejas'),
    path('vistaRegistroQuejas', views.vistaRegistroQuejas, name='vistaRegistroQuejas'),
    path('detalle_queja/<int:queja_id>/', views.detalle_queja, name='detalle_queja'),
     path('pre-registrar-queja/<int:aprendiz_id>/', registros.pre_registrar_queja, name='pre_registrar_queja'),
    path('registrar-queja/', registros.registro_queja, name='registro_queja'),
    path('vistaInstruRegistroquejas', views.vistaInstruRegistroquejas, name='vistaInstruRegistroquejas'),

    #Evidencias de las Queja
    path('ConsultarEvidenciaQuejas', views.ConsultarEvidenciaQuejas, name='ConsultarEvidenciaQuejas'),
    path('VistaRegistrarEvidenciasQuejas', views.VistaRegistrarEvidenciasQuejas, name='VistaRegistrarEvidenciasQuejas'),
    #Observaciones extra de las queja 
    path('ConsultarObservacionesEstrasQuejas', views.ConsultarObservacionesEstrasQuejas, name='ConsultarObservacionesEstrasQuejas'),
    path('VistaRegistroObservacionExtraQueja', views.VistaRegistroObservacionExtraQueja, name='VistaRegistroObservacionExtraQueja'),
    #Novedad Comite 
    path('ConsultarNovedaComite', views.ConsultarNovedaComite, name='ConsultarNovedaComite'),
    path('VistaRegistroNovedadComite', views.VistaRegistroNovedadComite, name='VistaRegistroNovedadComite'),
    #
    path('marcar-leido/<int:notificacion_id>/', views.marcar_leido, name='marcar_leido'),

    
]

