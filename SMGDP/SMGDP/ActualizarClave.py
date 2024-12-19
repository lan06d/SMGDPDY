from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

def CambiarContrasena(request):
    if request.method == 'POST':
        contrasena_actual = request.POST.get('contrasena_actual')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Verifica que todos los campos estén presentes
        if not all([contrasena_actual, nueva_contrasena, confirmar_contrasena]):
            messages.warning(request, 'Completa todos los campos.')
            return redirect('CambiarContrasena')

        # Verifica que la contraseña actual sea correcta
        if not request.user.check_password(contrasena_actual):
            messages.warning(request, 'La contraseña actual no es correcta.')
            return redirect('CambiarContrasena')

        # Verifica que la nueva contraseña y la confirmación coincidan
        if nueva_contrasena != confirmar_contrasena:
            messages.warning(request, 'Las nuevas contraseñas no coinciden.')
            return redirect('CambiarContrasena')

        # Cambia la contraseña del usuario
        request.user.set_password(nueva_contrasena)
        request.user.save()

        # Actualiza la sesión para que el usuario no tenga que iniciar sesión nuevamente
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Contraseña actualizada exitosamente.')
        return redirect('inicio')  # Redirige a la página de inicio o cualquier otra vista

    return render(request, 'usuarios/CambiarContrasena.html')  # Muestra el formulario
