import os
import json
import traceback
from django.http import HttpResponse, HttpResponseRedirect
from django.core.management import call_command
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .models import Usuario

@login_required
def backup(request):
    # Verifica que el usuario tenga el rol adecuado
    if not request.user.rol == 'Administrador':
        # Mensaje de error
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('nombre_de_tu_vista')  # Redirige a la vista que desees, por ejemplo, la página principal o el dashboard

    # Crear la carpeta BACKUP si no existe
    if not os.path.exists(settings.BACKUP_DIR):
        os.makedirs(settings.BACKUP_DIR)

    # Nombre del archivo de backup con fecha y hora
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_filename = f"{settings.BACKUP_DIR}/backup_{timestamp}.json"

    # Realiza la copia de seguridad
    call_command('dumpdata', output=backup_filename)

    # Mensaje de éxito
    messages.success(request, f'Backup realizado correctamente. Archivo: {backup_filename}')

    # Redirige a la vista donde deseas mostrar el mensaje
    return redirect('VistaConfiguracion')  # Redirige a la vista que desees


@login_required
def restore(request):
    try:
        # Obtener la lista de archivos de la carpeta BACKUP
        backup_files = [f for f in os.listdir(settings.BACKUP_DIR) if f.endswith('.json')]
        
        # Si no hay archivos de backup, mostrar un mensaje
        if not backup_files:
            return HttpResponse('No se encontraron archivos de backup disponibles.', status=404)

        # Renderizar la plantilla con la lista de archivos de backup
        return render(request, 'Configuracion/select_backup.html', {'backup_files': backup_files})

    except Exception as e:
        error_message = f"Error al restaurar la base de datos: {str(e)}"
        return HttpResponse(error_message, status=500)

    from django.contrib.auth.models import User
import json
import os
from django.contrib import messages
from django.shortcuts import redirect
from django.core.management import call_command
from django.conf import settings

@login_required
def restore_file(request, filename):
    try:
        # Verificar si el archivo existe en el directorio BACKUP
        backup_file_path = os.path.join(settings.BACKUP_DIR, filename)
        
        if not os.path.exists(backup_file_path):
            # Usar mensajes para informar al usuario
            messages.error(request, f"El archivo {filename} no existe en la carpeta de backups.")
            return redirect('restore')  # Redirigir a la vista de selección de backups

        # Cargar el archivo backup con codificación ISO-8859-1
        with open(backup_file_path, 'r', encoding='ISO-8859-1') as f:
            data = json.load(f)  # Cargar los datos del archivo

        # Verificar y filtrar usuarios con correos duplicados
        if 'auth.User' in data:  # Suponiendo que los datos de usuarios están en la clave 'auth.User'
            existing_emails = set(Usuario.objects.values_list('email', flat=True))
            data['auth.User'] = [user for user in data['auth.User'] if user['fields']['email'] not in existing_emails]

        # Guardar los datos en un nuevo archivo 'backup_utf8.json' con codificación UTF-8
        utf8_backup_path = f'{settings.BACKUP_DIR}/backup_utf8.json'
        with open(utf8_backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Guardar el archivo en UTF-8

        # Limpiar contenido relevante antes de cargar los datos
        ContentType.objects.filter(app_label='SMGDP', model='asistencias').delete()

        # Usar el archivo convertido para restaurar la base de datos
        call_command('loaddata', utf8_backup_path)

        # Enviar mensaje de éxito
        messages.success(request, f"Base de datos restaurada correctamente desde el archivo {filename}.")
        return redirect('restore')  # Redirigir a la vista de selección de backups

    except Exception as e:
        # Si ocurre un error, enviar mensaje de error
        messages.error(request, f"Error al restaurar la base de datos: {str(e)}")
        return redirect('restore')  # Redirigir a la vista de selección de backups
