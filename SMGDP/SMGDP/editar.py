from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Aprendices, UnidadProgramacion, Programas, Jornadas, Fichas, EstadoAcademicoSofia
from django.contrib import messages
from django.http import HttpResponseRedirect


def PreEditarUsuarios(request, id):
    usuario = get_object_or_404(Usuario, pk=id)
    data = {
        "usuario": usuario,
    }
    return render(request, "usuarios/EditarUsuarios.html", data)

def ActualizarUsuarios(request, id):
    if request.method == "POST":
        usuario = get_object_or_404(Usuario, pk=id)
        usuario.username = request.POST.get('username')
        usuario.documento = request.POST.get('documento')
        usuario.email = request.POST.get('email')
        usuario.rol = request.POST.get('rol')
        usuario.save()
        return redirect('VistaCoordinador')
    else:
        return redirect('PreEditarUsuarios', id=id)  # Redirecciona si no es una petición POST


def PreEditarPerfil(request):
    usuario = request.user  # Obtiene el usuario en sesión
    data = {
        "usuario": usuario,
    }
    return render(request, "usuarios/EditarPerfil.html", data)



def ActualizarPerfil(request):
    if request.method == "POST":
        usuario = request.user  # Obtiene el usuario en sesión
        usuario.username = request.POST.get('username')
        usuario.documento = request.POST.get('documento')
        usuario.email = request.POST.get('email')
        
        # Asegúrate de que el rol no sea modificable por el usuario, si aplica:
        # usuario.rol = request.POST.get('rol')

        usuario.save()

        # Redirigir a la página anterior (si existe, si no a la vista de perfil)
        referer = request.META.get('HTTP_REFERER', 'default-url')  # 'default-url' es la URL a la que se redirige si no hay referrer
        return HttpResponseRedirect(referer)  # Redirige a la URL que estaba antes
    else:
        # Si no es una solicitud POST, redirigir a la vista de edición de perfil
        return redirect('PreEditarPerfil')


# Vista para mostrar el formulario de edición de un aprendiz
def PreEditarAprendiz(request, id):
    # Obtener el aprendiz por el ID
    aprendiz = get_object_or_404(Aprendices, pk=id)
    data = {
        "aprendiz": aprendiz,
        "fichas": Fichas.objects.all(),  # Para mostrar las fichas en el formulario
        "estado_academico": EstadoAcademicoSofia.objects.all(),  # Para mostrar el estado académico
    }
    return render(request, "Aprendices/EditarAprendiz.html", data)



def ActualizarAprendix(request, id):
    # Obtener el aprendiz desde la base de datos por ID
    aprendiz = get_object_or_404(Aprendices, pk=id)
    
    if request.method == "POST":
        try:
            # Obtener los datos del formulario
            aprendiz.nombres = request.POST.get('nombres')
            aprendiz.apellidos = request.POST.get('apellidos')
            aprendiz.tipo_documento = request.POST.get('tipoDocumento')
            aprendiz.no_documento = request.POST.get('no_documento')
            aprendiz.correo = request.POST.get('correo')
            aprendiz.telefono = request.POST.get('telefono')
            
            # Asignar la ficha seleccionada por número
            ficha_numero = request.POST.get('ficha')
            try:
                ficha = Fichas.objects.get(numero=ficha_numero)
                aprendiz.ficha = ficha
            except Fichas.DoesNotExist:
                messages.error(request, "Ficha no encontrada.")
                return redirect('PreEditarAprendiz', id=id)
            
            # Asignar el estado académico seleccionado
            estado_academico_id = request.POST.get('estado_academico')
            try:
                estado_academico = EstadoAcademicoSofia.objects.get(id=estado_academico_id)
                aprendiz.estado_academico_sofia = estado_academico
            except EstadoAcademicoSofia.DoesNotExist:
                messages.error(request, "Estado académico no encontrado.")
                return redirect('PreEditarAprendiz', id=id)
            
            # Guardar los cambios en el aprendiz
            aprendiz.save()
            
            # Mostrar mensaje de éxito
            messages.success(request, "Datos del aprendiz actualizados exitosamente.")
            return redirect('ConsultarAprendices')  # Redirigir a la vista de consulta de aprendices
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return redirect('PreEditarAprendiz', id=id)
    
    else:
        # Si no es un POST, redirigir a la página de edición para mostrar el formulario
        return redirect('PreEditarAprendiz', id=id)




def EditarUnidadProgramacion(request, unidad_id):
    # Obtener la unidad de programación que se va a editar
    unidad = get_object_or_404(UnidadProgramacion, id=unidad_id)

    if request.method == 'POST':
        unidad_programacion = request.POST.get('unidad_programacion')
        ficha_id = request.POST.get('ficha')
        usuario_id = request.POST.get('usuario')

        # Validar que la ficha existe
        try:
            ficha = Fichas.objects.get(numero=ficha_id)
        except Fichas.DoesNotExist:
            messages.error(request, 'La ficha seleccionada no existe.')
            return redirect('consultaUnidadProgramacion', unidad_id=unidad_id)

        # Validar que el usuario existe
        try:
            usuario = Usuario.objects.get(username=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, 'El usuario seleccionado no existe.')
            return redirect('consultaUnidadProgramacion', unidad_id=unidad_id)

        # Actualizar los datos de la unidad de programación
        try:
            unidad.unidad_programacion = unidad_programacion
            unidad.ficha = ficha
            unidad.usuario = usuario
            unidad.save()
            messages.success(request, 'La unidad de programación se actualizó correctamente.')
            return redirect('consultaUnidadProgramacion')  # Redirige a una vista de listado o donde necesites
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar los cambios: {e}')
            return redirect('consultaUnidadProgramacion', unidad_id=unidad_id)

    # Si es una petición GET, renderiza el formulario con los datos actuales
    fichas = Fichas.objects.all()
    usuarios = Usuario.objects.all()
    return render(request, 'unidadProgramacion/editarUnidadProgramacion.html', {
        'unidad': unidad,
        'fichas': fichas,
        'usuarios': usuarios
    })



def EditarPrograma(request, programa_id):
    # Obtener el programa que se va a editar
    programa = get_object_or_404(Programas, id=programa_id)

    if request.method == 'POST':
        nombre_programa = request.POST.get('nombre_programa')

        # Validar que el campo no esté vacío
        if not nombre_programa:
            messages.error(request, 'El nombre del programa no puede estar vacío.')
            return redirect('editarPrograma', programa_id=programa_id)

        # Actualizar los datos del programa
        try:
            programa.nombre_programa = nombre_programa
            programa.save()
            messages.success(request, 'El programa se actualizó correctamente.')
            return redirect('vistaProgramas')  # Redirige a una vista de listado de programas
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar los cambios: {e}')
            return redirect('editarPrograma', programa_id=programa_id)

    # Si es una petición GET, renderiza el formulario con los datos actuales
    return render(request, 'programas/EditarProgramas.html', {
        'programa': programa
    })



#Fichas
def EditarFicha(request, ficha_id):
    # Obtener la ficha utilizando `numero` en lugar de `id`
    ficha = get_object_or_404(Fichas, numero=ficha_id)

    if request.method == 'POST':
        numero = request.POST.get('numero')
        jornada_id = request.POST.get('jornadas')
        programa_id = request.POST.get('programas')

        # Validar que la jornada existe
        try:
            jornada = Jornadas.objects.get(id=jornada_id)
        except Jornadas.DoesNotExist:
            messages.error(request, 'La jornada seleccionada no existe.')
            return redirect('EditarFicha', ficha_id=ficha_id)

        # Validar que el programa existe
        try:
            programa = Programas.objects.get(id=programa_id)
        except Programas.DoesNotExist:
            messages.error(request, 'El programa seleccionado no existe.')
            return redirect('EditarFicha', ficha_id=ficha_id)

        # Actualizar los datos de la ficha
        try:
            ficha.numero = numero
            ficha.jornada = jornada
            ficha.programa = programa
            ficha.save()
            messages.success(request, 'La ficha se actualizó correctamente.')
            return redirect('consultaFichas')  # Ajusta esto según tu vista de listado
        except Exception as e:
            messages.error(request, f'Ocurrió un error al guardar los cambios: {e}')
            return redirect('EditarFicha', ficha_id=ficha_id)

    # Si es una petición GET, renderiza el formulario con los datos actuales
    jornadas = Jornadas.objects.all()
    programas = Programas.objects.all()
    return render(request, 'fichas/editarFicha.html', {
        'ficha': ficha,
        'jornadas': jornadas,
        'programas': programas
    })
