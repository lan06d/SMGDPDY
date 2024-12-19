from django.shortcuts import render, redirect
from django.http import HttpResponse
import csv
import io
from .models import Usuario, Fichas, Programas, Jornadas, UnidadProgramacion,EstadoAcademicoSofia, Aprendices
import chardet
from django.contrib import messages



def importacioProgramas(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            # Detectar la codificación
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            decoded_file = raw_data.decode(encoding)
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            
            # Saltar el encabezado si existe
            next(reader)

            for row in reader:
                if len(row) < 1:  # Asegúrate de que haya al menos una columna
                    continue
                
                # Asegúrate de que la columna sea [nombre_programa]
                Programas.objects.create(
                    nombre_programa=row[0],  # Suponiendo que el nombre del programa está en la primera columna
                )

            messages.success(request, "Importación de programas realizada con éxito.")
            return redirect('vistaProgramas')
        except Exception as e:
            messages.error(request, f"Error en la importación: {str(e)}")
            return redirect('vistaProgramas')

    return render(request, 'programas/ConsultarProgramas.html') 



import csv
import io
import chardet
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.hashers import make_password  # Importar make_password
from .models import Usuario

def import_csv(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            # Detectar la codificación
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            decoded_file = raw_data.decode(encoding)
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            
            # Saltar el encabezado si existe
            next(reader, None)

            for row in reader:
                if len(row) < 5:  # Verificar que haya al menos 5 columnas
                    continue
                
                # Verificar si el documento ya existe para evitar duplicados
                if not Usuario.objects.filter(documento=row[1]).exists():
                    # Asegúrate de que las columnas sean [nombre_apellido, documento, correo, clave, rol]
                    Usuario.objects.create(
                        username=row[0],
                        documento=int(row[1]),  # Convertir a entero para BigIntegerField
                        email=row[2],
                        password=make_password(row[3]),  # Cifrar la clave con make_password
                        rol=row[4],
                    )

            # Mensaje de éxito
            messages.success(request, "Importación realizada con éxito.")
            return redirect('VistaCoordinador')  # Reemplaza con el nombre de la URL correspondiente
        except Exception as e:
            messages.error(request, f"Error en la importación: {str(e)}")
            return redirect('VistaCoordinador')  # Reemplaza con el nombre de la URL correspondiente

    return render(request, 'coordinador/inicioCoordinador.html')


"""def ImportacionFicha(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            
            # Saltar el encabezado si existe
            next(reader)

            # Obtener los objetos de programa y jornada con id 1
            programa = Programas.objects.get(id=1)
            jornada = Jornadas.objects.get(id=1)

            for row in reader:
                if len(row) < 1:  # Asegúrate de que haya al menos una columna (número de ficha)
                    continue
                
                # Crear la ficha con el número de ficha, programa y jornada predeterminados
                Fichas.objects.create(
                    numero=row[0],
                    programa=programa,
                    jornada=jornada,
                )

            return HttpResponse("Importación de fichas realizada con éxito.")
        except Exception as e:
            return HttpResponse(f"Error en la importación: {str(e)}")

    return render(request, 'tu_template.html')  # Cambia a tu template
""" 

def ImportacionFicha(request):
    
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            # Cambiar la codificación a 'latin-1' para leer caracteres especiales
            decoded_file = file.read().decode('latin-1')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            
            # Saltar el encabezado si existe
            next(reader)

            for row in reader:
                if len(row) < 3:  
                    continue
                
                # Extraer los datos del CSV
                ficha_numero = row[0]  # Número de ficha
                nombre_programa = row[1]  # Nombre del programa
                nombre_jornada = row[2]  # Nombre de la jornada

                # Obtener o crear el programa y jornada
                programa, _ = Programas.objects.get_or_create(nombre_programa=nombre_programa)
                jornada, _ = Jornadas.objects.get_or_create(nombre_jornada=nombre_jornada)

                # Crear la ficha
                Fichas.objects.create(
                    numero=ficha_numero,
                    programa=programa,
                    jornada=jornada
                )

            
            messages.success(request, "Importación realizada con éxito.")
            return redirect('consultaFichas')
        except Exception as e:
            messages.error(request, f"Error en la importación: {str(e)}")
            return redirect('consultaFichas')

    return render(request, 'fichas/consultaFichas.html')

def importar_unidad_programacion(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        errores = []  # Lista para registrar las filas que no se pudieron importar

        try:
            # Detectar la codificación
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            decoded_file = raw_data.decode(encoding)
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            
            # Saltar el encabezado
            next(reader)

            for index, row in enumerate(reader, start=2):  # Comenzar en 2 para considerar el encabezado
                if len(row) != 3:  # Verificar que la fila tenga exactamente 3 columnas
                    errores.append(f"Fila {index}: Número incorrecto de columnas. Se esperaban 3.")
                    continue

                # Extraer los datos
                ficha_id = row[0]  # Primera columna
                unidad_programacion = row[1]  # Segunda columna
                usuario_nombre_apellido = row[2]  # Tercera columna

                # Obtener la ficha por ID
                ficha = Fichas.objects.filter(numero=ficha_id).first()
                if not ficha:
                    errores.append(f"Fila {index}: Ficha con ID {ficha_id} no encontrada.")
                    continue

                # Obtener el usuario por nombre y apellido
                usuario = Usuario.objects.filter(username=usuario_nombre_apellido).first()
                if not usuario:
                    errores.append(f"Fila {index}: Usuario {usuario_nombre_apellido} no encontrado.")
                    continue

                # Verificar si ya existe la unidad de programación
                if UnidadProgramacion.objects.filter(
                    ficha=ficha,
                    unidad_programacion=unidad_programacion,
                    usuario=usuario
                ).exists():
                    errores.append(f"Fila {index}: Unidad de programación duplicada.")
                    continue

                # Crear la unidad de programación
                UnidadProgramacion.objects.create(
                    ficha=ficha,
                    unidad_programacion=unidad_programacion,
                    usuario=usuario
                )

            # Mostrar mensajes de éxito o errores
            if errores:
                messages.warning(request, "Algunas unidades no se importaron correctamente:")
                for error in errores:
                    messages.warning(request, error)
            else:
                messages.success(request, "Importación de unidades de programación realizada con éxito.")

            return redirect('consultaUnidadProgramacion')

        except Exception as e:
            print(f"Error en la importación: {str(e)}")
            messages.error(request, f"Error en la importación: {str(e)}")
            return redirect('consultaUnidadProgramacion')

    return render(request, 'unidadProgramacion/cosultarUnidadProgramacion.html')





def importarAprendices(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        try:
            # Detectar la codificación
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            decoded_file = raw_data.decode(encoding)
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')

            # Saltar el encabezado
            next(reader)

            for row in reader:
                if len(row) < 8:  # Asegurarse de que haya al menos 8 columnas
                    print("Fila incompleta:", row)
                    continue

                # Extraer los datos
                nombres = row[0]
                apellidos = row[1]
                tipo_documento = row[2]
                no_documento = row[3]
                correo = row[4]
                telefono = row[5]
                ficha_id = row[6]
                estado_academico_nombre = row[7]

                # Validar Ficha
                ficha = Fichas.objects.filter(numero=ficha_id).first()
                if not ficha:
                    print("Ficha no encontrada:", ficha_id)
                    messages.error(request, f"Ficha no encontrada: {ficha_id}")
                    continue

                # Validar Estado Académico
                estado_academico = EstadoAcademicoSofia.objects.filter(estado=estado_academico_nombre).first()
                if not estado_academico:
                    print("Estado académico no encontrado:", estado_academico_nombre)
                    messages.error(request, f"Estado académico no encontrado: {estado_academico_nombre}")
                    continue

                # Crear o actualizar el aprendiz
                aprendiz, created = Aprendices.objects.update_or_create(
                    no_documento=no_documento,
                    defaults={
                        'nombres': nombres,
                        'apellidos': apellidos,
                        'tipo_documento': tipo_documento,
                        'correo': correo,
                        'telefono': telefono,
                        'ficha': ficha,
                        'estado_academico_sofia': estado_academico
                    }
                )
                print("Aprendiz creado o actualizado:", aprendiz.nombres, aprendiz.apellidos, " - Creado:", created)

            messages.success(request, "Importación de aprendices realizada con éxito.")
            return redirect('ConsultarAprendices')
        except Exception as e:
            print(f"Error en la importación: {str(e)}")
            messages.error(request, f"Error en la importación: {str(e)}")
            return redirect('ConsultarAprendices')

    return render(request, 'Aprendices/ConsultaAprendices.html')

