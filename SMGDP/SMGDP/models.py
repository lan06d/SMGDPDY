from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class Usuario(AbstractUser):
    documento = models.BigIntegerField(unique=True)  # Campo adicional
    rol = models.CharField(max_length=80)  # Campo adicional
    # Aquí puedes agregar más campos si lo necesitas



class Programas(models.Model):
    nombre_programa = models.CharField(max_length=100)

class Jornadas(models.Model):
    nombre_jornada = models.CharField(max_length=50)


class Fichas(models.Model):
    numero = models.CharField(max_length=300, primary_key=True)
    programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    jornada = models.ForeignKey(Jornadas, on_delete=models.CASCADE)

class UnidadProgramacion(models.Model):
    ficha = models.ForeignKey(Fichas, on_delete=models.CASCADE)  
    unidad_programacion = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

class Trimestre(models.Model):
    nombre_trimestre = models.CharField(max_length=80)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    ficha = models.ForeignKey(Fichas, on_delete=models.CASCADE)

class EstadoAcademicoSofia(models.Model):
    estado = models.CharField(max_length=50)

class Aprendices(models.Model):
    nombres = models.CharField(max_length=90)
    apellidos = models.CharField(max_length=90)
    tipo_documento = models.CharField(max_length=20)
    no_documento = models.CharField(max_length=20)
    correo = models.EmailField(max_length=50)
    telefono = models.CharField(max_length=15)
    ficha = models.ForeignKey(Fichas, on_delete=models.CASCADE)
    estado_academico_sofia = models.ForeignKey(EstadoAcademicoSofia, on_delete=models.CASCADE)

class EstadoAsistencias(models.Model):
    estado_asistencia = models.CharField(max_length=50)

class Asistencias(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    unidad_programacion = models.ForeignKey(UnidadProgramacion, on_delete=models.CASCADE)
    observaciones = models.TextField()
    aprendiz = models.ForeignKey(Aprendices, on_delete=models.CASCADE)
    estado_asistencia = models.ForeignKey(EstadoAsistencias, on_delete=models.CASCADE)

class Quejas(models.Model):
    regional = models.CharField(max_length=80)
    motivo = models.CharField(max_length=80)
    programa = models.ForeignKey(Programas, on_delete=models.CASCADE)
    centro_formacion = models.CharField(max_length=80)
    nivel_formacion = models.CharField(max_length=80)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    aprendiz = models.ForeignKey(Aprendices, on_delete=models.CASCADE)
    observacion_instructor = models.TextField()
    situacion_riesgo = models.CharField(max_length=100)
    causas_origen_riesgo = models.CharField(max_length=100)
    escalo_riesgo = models.CharField(max_length=80)
    a_quien_escalo = models.CharField(max_length=80)
    acciones_ruta_apren = models.CharField(max_length=100)
    estado_contrato_aprendizaje = models.BooleanField()
    correo_vocero = models.EmailField(max_length=100)

class EvidenciaQueja(models.Model):
    imagen = models.BinaryField()
    queja = models.ForeignKey(Quejas, on_delete=models.CASCADE)

class ObservacionesExtraQuejas(models.Model):
    queja = models.ForeignKey(Quejas, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    observacion = models.TextField()
    imagen = models.BinaryField()

class ObservacionBienestar(models.Model):
    queja = models.ForeignKey(Quejas, on_delete=models.CASCADE)
    observacion = models.TextField()

class NovedadComite(models.Model):
    queja = models.ForeignKey(Quejas, on_delete=models.CASCADE)
    acta = models.CharField(max_length=80)
    novedad = models.CharField(max_length=80)



class Notificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="notificaciones")
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(default=now)
    leido = models.BooleanField(default=False)

    def __str__(self):
        return self.mensaje