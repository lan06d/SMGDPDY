from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
import random
import string
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect


# Usamos el modelo personalizado de usuario
Usuario = get_user_model()


def recuperacion_contraseña(request):
    if request.method == "POST":
        # Obtener el correo del formulario
        email = request.POST.get('email')

        # Buscar el usuario en base al correo proporcionado
        try:
            persona = Usuario.objects.get(email=email)  # Buscar por email
        except Usuario.DoesNotExist:
            # Manejar el caso en que no se encuentre un usuario con ese email
            messages.error(
                request, "El correo electrónico proporcionado no está registrado.")
            return render(request, 'inicio/recuperacionClave.html')

        # Generar un código aleatorio alfanumérico de 8 caracteres
        caracteres = string.ascii_letters + string.digits  # Letras y números
        codigo = ''.join(random.choice(caracteres)
                         for _ in range(8))  # Generar código de 8 caracteres

        # Encriptamos el código para actualizar la contraseña
        contraseña_encriptada = make_password(codigo)

        # Actualizamos la contraseña del usuario
        persona.password = contraseña_encriptada
        persona.save()

        # Crear el contenido del mensaje HTML
        mensaje_html = f"""
<html>
<head>
    <style>
        /* Estilos para el cuerpo del mensaje */
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fc;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }}
        h1 {{
            color: #2c3e50;
            font-size: 24px;
            margin-bottom: 15px;
            text-align: center;
        }}
        p {{
            color: #34495e;
            font-size: 16px;
            line-height: 1.5;
            margin-bottom: 15px;
            text-align: center;
        }}
        .codigo {{
            font-size: 24px;
            font-weight: bold;
            color: #2980b9;
            background-color: #ecf0f1;
            padding: 10px 15px;
            border-radius: 5px;
            margin: 20px 0;
            display: inline-block;
        }}
        .cta {{
            display: block;
            width: 200px;
            margin: 30px auto;
            background-color: #2980b9;
            color: white;
            text-align: center;
            padding: 12px;
            font-size: 16px;
            border-radius: 5px;
            text-decoration: none;
        }}
        .cta:hover {{
            background-color: #1d6ea5;
        }}
        .footer {{
            text-align: center;
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Recuperación de Contraseña</h1>
        <p>Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Si no solicitaste este cambio, puedes ignorar este correo.</p>
        <p><span class="codigo">{codigo}</span></p>
        <p>Por favor, usa esta nueva contraseña para iniciar sesión en tu cuenta.</p>
        <a href="https://tusitio.com/iniciar-sesion" class="cta">Iniciar sesión</a>
        <div class="footer">
            <p>&copy; 2024 Tu Sitio Web. Todos los derechos reservados.</p>
        </div>
    </div>
</body>
</html>
"""

        subject = "Recuperación de Contraseña"
        from_email = settings.EMAIL_HOST_USER
        to_email = [persona.email]

        # Enviar el correo electrónico
        msg = EmailMultiAlternatives(subject, "", from_email, to_email)
        msg.attach_alternative(mensaje_html, "text/html")
        msg.send()

        # Mensaje de éxito
        messages.success(
            request, "Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.")

    return render(request, 'inicio/recuperacionClave.html')



def enviar_correo(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')  # Ahora se obtiene el asunto
        mensaje = request.POST.get('mensaje')

        subject = asunto  # Usamos el asunto ingresado en el formulario
        message = mensaje  # El mensaje también es el que se envía
        from_email = settings.EMAIL_HOST_USER
        to_email = [email]

        try:
            msg = EmailMultiAlternatives(subject, message, from_email, to_email)
            msg.send()
            messages.success(request, "Correo enviado exitosamente.")
        except Exception as e:
            messages.error(request, f"Hubo un error al enviar el correo: {str(e)}")
        
        return redirect('EnviarCorreosInstru')  # Aquí rediriges a la URL adecuada

    return render(request, "instrutor/EnviarCorreos.html")  # Si no es un POST, simplemente renderizas el formulario
