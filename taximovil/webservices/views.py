from random import randint

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client

from config.models import Codigo
from taximovil.settings import TWILIO_SID, TWILIO_TOKEN, TWILIO_NUMBER
from webservices.serializers import TelefonoSerializer


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
                body="Tu número de verificación THT es " + str(codigo))
            response_data['sid'] = message.sid
            response_data['codigo'] = codigo
        except Exception as e:
            response_data['error'] = 'Ocurrio un problema al enviar el código'
            return Response(response_data,status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data)

    def get_serializer(self):
        return TelefonoSerializer()

