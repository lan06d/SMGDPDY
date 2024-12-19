from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Usuario, Jornadas, Programas, Fichas, UnidadProgramacion, Trimestre, EstadoAsistencias, EstadoAcademicoSofia, Aprendices, Quejas
from django.contrib.auth.hashers import make_password  #  codificar la contraseña
import re


def RegistroUsuarios(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_apellido = request.POST.get('nombre_apellido')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conpassword = request.POST.get('Conpassword')
        documento = request.POST.get('documento')
        rol_id = request.POST.get('rol_id')

        # Verifica que todos los campos requeridos estén presentes
        if not all([nombre_apellido, email, password, conpassword, documento, rol_id]):
            messages.warning(request, 'Completa todos los campos.')
            return redirect('vistaRegistroUsuarios')

        # Verifica que las contraseñas coincidan
        if password != conpassword:
            messages.warning(request, 'Las contraseñas no coinciden.')
            return redirect('vistaRegistroUsuarios')

        # Verifica que el email no esté ya registrado en el modelo Usuario
        if Usuario.objects.filter(email=email).exists():  # Cambiar 'correo' por 'email'
            messages.warning(request, 'El correo del usuario ya está registrado.')
            return redirect('vistaRegistroUsuarios')

        # Verifica que el documento no esté ya registrado
        if Usuario.objects.filter(documento=documento).exists():
            messages.warning(request, 'El documento ya está registrado.')
            return redirect('vistaRegistroUsuarios')

        # Codifica la contraseña utilizando make_password para cumplir con las normas de seguridad
        password_encriptado = make_password(password)

        # Crear el nuevo usuario con la contraseña encriptada
        usuario = Usuario(
            username=nombre_apellido,
            documento=documento,
            email=email,  # Cambiar 'correo' por 'email'
            password=password_encriptado,  # Contraseña encriptada
            rol=rol_id  
        )
        usuario.save()

        # Mensaje de éxito y redirección a la página de inicio
        messages.success(request, 'Registro exitoso.')
        return redirect('inicio')

    # Si no es un método POST, redirigir a la vista de registro
    return redirect('vistaRegistroUsuarios')


def RegistroPrograma(request):
    
    if request.method == 'POST':
        programa_nombre = request.POST.get('programa')
        
        # Validar que el nombre del programa solo contenga letras y espacios
        if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', programa_nombre):
            messages.error(request, 'El nombre del programa solo puede contener letras y espacios.')
            return render(request, 'programas/RegistroPrograma.html')
        
        # Change 'programas' to 'nombre_programa'
        programa = Programas(nombre_programa=programa_nombre)
        
        if Programas.objects.filter(nombre_programa=programa_nombre).exists():
            messages.warning(request, 'El Programa ya está registrado en el sistema')
            return render(request, 'programas/RegistroPrograma.html')
        
        programa.save()
        messages.success(request, 'El Programa se ha registrado con éxito')
        return render(request, 'programas/RegistroPrograma.html')

def RegistroJornada(request):
    if request.method == 'POST':
        jornada_nombre = request.POST.get('jornada')
        
        # Verifica si el nombre de la jornada ya existe
        if Jornadas.objects.filter(nombre_jornada=jornada_nombre).exists():
            messages.error(request, "La jornada ya existe.")
            return redirect('vistaRegistroJornadas')  
        # Crea y guarda la nueva jornada
        nueva_jornada = Jornadas(nombre_jornada=jornada_nombre)
        nueva_jornada.save()
        messages.success(request, "Jornada registrada exitosamente.")
        return redirect('vistaRegistroJornadas') 

    return render(request, 'jornadas/registroJornadas.html')  


def RegistroFichas(request):
    if request.method == 'POST':
        numero_ficha = request.POST.get('numero')
        programa_id = request.POST.get('programas')
        jornada_id = request.POST.get('jornadas')
        
        # Verificar si la ficha ya existe
        if Fichas.objects.filter(numero=numero_ficha).exists():
            messages.error(request, 'La ficha ya está registrada.')
            return redirect('vistaRegistroFichas')
        
        try:
            nuevaFicha = Fichas(
                numero=numero_ficha,
                programa=Programas.objects.get(id=programa_id),
                jornada=Jornadas.objects.get(id=jornada_id)
            )
            nuevaFicha.save()
            messages.success(request, 'La ficha se registró correctamente.')
            return redirect('vistaRegistroFichas')
        except Programas.DoesNotExist:
            messages.error(request, 'Programa no encontrado.')
        except Jornadas.DoesNotExist:
            messages.error(request, 'Jornada no encontrada.')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')
    
    return render(request, 'fichas/RegistrarFichas.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UnidadProgramacion, Fichas, Usuario

def RegistroUnidadProgramacion(request):
    if request.method == 'POST':
        unidad_programacion = request.POST.get('unidad_programacion')
        ficha_id = request.POST.get('ficha')
        usuario_id = request.POST.get('usuario')

        # Validar que se envían todos los datos necesarios
        if not unidad_programacion or not ficha_id or not usuario_id:
            messages.error(request, 'Todos los campos son obligatorios.')
            return redirect('VistaRegistoUnidadProgramacion')

        # Validar que la ficha existe
        try:
            ficha = Fichas.objects.get(numero=ficha_id)
        except Fichas.DoesNotExist:
            messages.error(request, 'La ficha seleccionada no existe.')
            return redirect('VistaRegistoUnidadProgramacion')

        # Validar que el usuario existe
        try:
            usuario = Usuario.objects.get(username=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario seleccionado no existe.')
            return redirect('VistaRegistoUnidadProgramacion')

        # Validar si ya existe una unidad con la misma ficha y usuario
        if UnidadProgramacion.objects.filter(ficha=ficha, usuario=usuario, unidad_programacion=unidad_programacion).exists():
            messages.error(request, 'Ya existe una unidad de programación con estos datos.')
            return redirect('VistaRegistoUnidadProgramacion')

        # Crear y guardar la unidad de programación
        try:
            nueva_unidad = UnidadProgramacion(
                ficha=ficha,
                unidad_programacion=unidad_programacion,
                usuario=usuario
            )
            nueva_unidad.save()
            messages.success(request, 'La unidad de programación se registró correctamente.')
            return redirect('VistaRegistoUnidadProgramacion')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar la unidad: {e}')
    
    return redirect('VistaRegistoUnidadProgramacion')


def RegistroTrimestres(request):
    
    
    if request.method == 'POST':
        nombre_trimestre = request.POST.get('nombre_trimestre')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        ficha_id = request.POST.get('ficha')

        # Validar que la ficha existe
        try:
            ficha = Fichas.objects.get(numero=ficha_id)
        except Fichas.DoesNotExist:
            messages.error(request, 'La ficha no existe.')
            return redirect('vistaRegistroTrimestres')

        # Verificar que la fecha de inicio sea anterior a la fecha de fin
        if fecha_inicio > fecha_fin:
            messages.error(request, 'La fecha de inicio debe ser anterior a la fecha de fin.')
            return redirect('vistaRegistroTrimestres')

        # Crear y guardar el trimestre
        try:
            nuevoTrimestre = Trimestre(
                nombre_trimestre=nombre_trimestre,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                ficha=ficha
            )
            nuevoTrimestre.save()
            messages.success(request, 'El trimestre se registró correctamente.')
            return redirect('vistaRegistroTrimestres')
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {e}')

    # Renderizar la plantilla con las fichas disponibles
    fichas = Fichas.objects.all()  # Obtener todas las fichas
    return render(request, 'trimestre/registroTrimestres.html', {'fichas': fichas})




def RegistroEstadoAsistencia(request):
    if request.method == 'POST':
        estado_asistencia = request.POST.get('estado_asistencia')
        
        # Verifica si el campo está vacío
        if not estado_asistencia:
            messages.error(request, 'Por favor, ingresa un estado de asistencia válido.')
            return redirect('ConsultarEstadoAsistencia')
        
        # Crear y guardar el nuevo estado de asistencia
        try:
            nuevo_estado = EstadoAsistencias(estado_asistencia=estado_asistencia)
            nuevo_estado.save()
            messages.success(request, 'Estado de asistencia registrado correctamente.')
            return redirect('ConsultarEstadoAsistencia')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar el estado: {e}')
    
    return render(request, 'EstadoAsistencia/ConsultarEstado.html')


def RegistroRegistroAprendices(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombres = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        tipo_documento = request.POST.get('tipoDocumento')
        no_documento = request.POST.get('no_documento')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        ficha_id = request.POST.get('fichas')
        estado_academico_id = request.POST.get('estadoAcadenico')

        # Verificar que todos los campos estén presentes
        if not all([nombres, apellidos, tipo_documento, no_documento, correo, telefono, ficha_id, estado_academico_id]):
            messages.warning(request, 'Completa todos los campos.')
            return redirect('RegistroAprendices')

        # Verificar que el correo no esté ya registrado en el modelo Aprendices
        if Aprendices.objects.filter(correo=correo).exists():
            messages.warning(request, 'El correo ya está registrado para otro aprendiz.')
            return redirect('RegistroAprendices')

        # Verificar que el número de documento no esté ya registrado
        if Aprendices.objects.filter(no_documento=no_documento).exists():
            messages.warning(request, 'El número de documento ya está registrado para otro aprendiz.')
            return redirect('RegistroAprendices')

        # Crear un nuevo aprendiz
        aprendiz = Aprendices(
            nombres=nombres,
            apellidos=apellidos,
            tipo_documento=tipo_documento,
            no_documento=no_documento,
            correo=correo,
            telefono=telefono,
            ficha_id=ficha_id,
            estado_academico_sofia_id=estado_academico_id
        )
        aprendiz.save()

        messages.success(request, 'Se registro al aprendiz')
        return redirect('RegistroAprendices')

    # Obtener las fichas y estados académicos para mostrarlos en el formulario
    fichas = Fichas.objects.all()
    estados_academicos = EstadoAcademicoSofia.objects.all()

    return render(request, 'Aprendices/RegistroAprendices.html', {
        'fichas': fichas,
        'estadoAcadenico': estados_academicos
    })


from datetime import date


def RegistroEstadosAcademicos(request):
    if request.method == 'POST':
        estado_academico = request.POST.get('Academico')
        
        # Verifica si el campo está vacío
        if not estado_academico:
            messages.error(request, 'Por favor, ingresa un estado de Academico  válido.')
            return redirect('RegistroEstadoAcademicoSofia')
        if EstadoAcademicoSofia.objects.filter(estado=estado_academico).exists():
            
            messages.error(request, 'Estado academico ya esta registrado')
            return redirect('RegistroEstadoAcademicoSofia')
        
        # Crear y guardar el nuevo estado de asistencia
        try:
            nuevo_estado = EstadoAcademicoSofia(estado=estado_academico)
            nuevo_estado.save()
            messages.success(request, 'Estado academico registrado correctamente.')
            return redirect('RegistroEstadoAcademicoSofia')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar el estado: {e}')
    
    return render(request, 'EstadoSofia/RegistrarEstado.html')

from django.shortcuts import redirect
from .models import Quejas, Notificacion

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse


from django.shortcuts import render, get_object_or_404, redirect

def pre_registrar_queja(request, aprendiz_id):
    # Obtener el aprendiz con el ID proporcionado
    aprendiz = get_object_or_404(Aprendices, id=aprendiz_id)
    programas = Programas.objects.all()

    # Redirigir al formulario de quejas, pasando los datos del aprendiz al contexto
    return render(request, 'Quejas/RegistroQuejas.html', {'aprendiz': aprendiz, 'programas': programas})



from django.utils.timezone import now  # Asegúrate de agregar esta línea

def registro_queja(request):
    if request.method == 'POST':
        # Proceso de registro de la queja
        nueva_queja = Quejas(
            regional=request.POST['regional'],
            motivo=request.POST['motivo'],
            programa_id=request.POST['programa_id'],
            centro_formacion=request.POST['centro_formacion'],
            nivel_formacion=request.POST['nivel_formacion'],
            usuario=request.user,
            fecha_registro=now(),  # Se utiliza el método now importado
            aprendiz_id=request.POST['aprendiz_id'],
            observacion_instructor=request.POST['observacion_instructor'],
            situacion_riesgo=request.POST['situacion_riesgo'],
            causas_origen_riesgo=request.POST['causas_origen_riesgo'],
            escalo_riesgo=request.POST['escalo_riesgo'],
            a_quien_escalo=request.POST['a_quien_escalo'],
            acciones_ruta_apren=request.POST['acciones_ruta_apren'],
            estado_contrato_aprendizaje=request.POST.get('estado_contrato_aprendizaje', False),
            correo_vocero=request.POST['correo_vocero']
        )
        nueva_queja.save()

        # Crear una notificación para el usuario
        mensaje = f"Se ha registrado una nueva queja con ID {nueva_queja.id}"
        Notificacion.objects.create(usuario=request.user, mensaje=mensaje)

        return redirect('vistaFichasInstUnidadProgramacion')

