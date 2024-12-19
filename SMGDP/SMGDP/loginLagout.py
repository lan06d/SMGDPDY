from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login, logout   # Para iniciar sesión
from .models import Usuario


from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Usuario  # Asegúrate de tener la importación correcta de tu modelo de Usuario

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Por favor, completa ambos campos.')
            return redirect('iniciar_sesion')

        try:
            # Busca el usuario usando su correo electrónico (en lugar de username)
            user = Usuario.objects.get(email=username)
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('iniciar_sesion')

        # Verifica la contraseña manualmente usando check_password
        if check_password(password, user.password):
            # Si las credenciales son correctas, inicia la sesión
            login(request, user)  # Esto maneja la creación de sesión y cookies

            # Depuración: Verificar el rol del usuario
            print(f"Rol del usuario {user.username}: {user.rol}")

            # Redirige según el rol del usuario
            if user.rol == 'Administrador':
                return redirect('VistaCoordinador')
            elif user.rol == 'Instructor' or user.rol == 'instructor':
                return redirect('vistaFichasInstUnidadProgramacion')
            elif user.rol == 'AyudanteCoordinacion':
                return redirect('Ajustar')
            else:
                messages.error(request, f'Rol de usuario "{user.rol}" no reconocido.')
                return redirect('iniciar_sesion')
        else:
            # Si la contraseña es incorrecta
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('iniciar_sesion')

    return render(request, 'inicio/index.html')


def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    messages.success(request, 'Has cerrado sesión con éxito.')  
    return redirect('inicio')  # Redirige a la página de inicio
