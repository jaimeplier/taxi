from random import randint

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from config.models import Codigo, Usuario, Cliente
from config.serializers import ClienteSerializer
from taximovil.settings import TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER
from webservices.serializers import TelefonoSerializer, CodigoSerializer, LoginSerializer, ResetSerializer, \
    ChangePasswordSerializer


class EnviarCodigo(APIView):
    """
    post:
    Envia un codigo sms al telefono
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TelefonoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = {}
        account_sid = TWILIO_SID
        auth_token = TWILIO_TOKEN
        client = Client(account_sid, auth_token)
        cs = Codigo.objects.filter(telefono=serializer.data.get('telefono'))
        cs.delete()
        codigo = randint(1, 99999)
        codigo = "{0:0=5d}".format(codigo)
        c = Codigo(codigo=codigo, telefono=serializer.data.get('telefono'))
        c.save()
        telefono = "+521" + serializer.data.get('telefono')
        try:
            message = client.messages.create(
                to=telefono,
                from_=TWILIO_NUMBER,
                body="Tu número de verificación Taximovil es " + str(codigo))
            response_data['sid'] = message.sid
            response_data['codigo'] = codigo
        except Exception as e:
            response_data['error'] = 'Ocurrio un problema al enviar el código'
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data)

    def get_serializer(self):
        return TelefonoSerializer()


class VerificaCodigo(APIView):
    """
        post:
        Verifica el codigo enviado y regresa el resultado
        0 el cliente no esta registrado
        1 el cliente ya esta rgistrado con ese telefono
        -1 el codigo es inválido
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        response_data = {}
        serializer = CodigoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        telefono = serializer.data.get('telefono')
        codigo = serializer.data.get('codigo')
        cs = Codigo.objects.filter(telefono=telefono, codigo=codigo)
        if cs.count() > 0:
            try:
                p = Usuario.objects.get(telefono=telefono)
                response_data['resultado'] = p.pk
            except Usuario.DoesNotExist:
                response_data['resultado'] = 0
        else:
            response_data['resultado'] = -1
        return Response(response_data)

    def get_serializer(self):
        return CodigoSerializer()


class LoginUsuario(APIView):
    """
    post:
        Login
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        response_data = {}
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        googleid = serializer.data.get('googleid')
        dispositivo = serializer.data.get('dispositivo')
        try:
            Cliente.objects.get(email=email)
        except Cliente.DoesNotExist:
            response_data['resultado'] = 0
            response_data['error'] = "Usuario y/o contraseña incorrectos"
            return Response(response_data)
        user = authenticate(email=email, password=password)
        if user is not None:
            token = Token.objects.get_or_create(user=user)
        else:
            response_data['resultado'] = 0
            response_data['error'] = "Usuario y/o contraseña incorrectos"
            return Response(response_data)
        user.googleid = googleid
        user.dispositivo = dispositivo
        try:
            device = FCMDevice.objects.get(registration_id=googleid)
            device.user = user
            device.name = user.get_full_name()
        except FCMDevice.DoesNotExist:
            device = FCMDevice(registration_id=googleid, name=user.get_full_name(), user=user)
        device.type = dispositivo
        device.save()
        user.save()
        response_data['resultado'] = 1
        response_data['token'] = str(token[0])
        serializer = ClienteSerializer(user, many=False)
        response_data['cliente'] = serializer.data
        return Response(response_data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return LoginSerializer()


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u = authenticate(email=self.request.user.email, password=serializer.validated_data.get('old'))
        if u is not None:
            u.set_password(serializer.validated_data.get('new'))
            u.save()
        else:
            return Response({"error": "La contraseña anterior no coincide"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"result": 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ChangePasswordSerializer()


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        u = Usuario.objects.get(email=serializer.validated_data.get('email'))
        ptoken = PasswordResetTokenGenerator()
        token = ptoken.make_token(u)
        subject = "Recuperar contraseña"
        to = [u.email]

        ctx = {
            'token': token,
            'uid': urlsafe_base64_encode(force_bytes(u.pk)).decode('UTF-8'),
            'request': request,
            'email': u.pk,
            'nombre': u.get_full_name()
        }
        try:
            message = get_template('correos/reset_password.html').render(ctx)
            msg = EmailMessage(subject, message, to=to)
            msg.content_subtype = 'html'
            msg.send()
        except Exception as e:
            pass
        return Response({"result": 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ResetSerializer()