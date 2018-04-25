from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Rol
from webservices.serializers import UsuarioEditSerializer


class RegistrarUsuario(APIView):
    """
        post:
            Registrar usuario
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        response_data = {}
        serializer = UsuarioEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.cliente.save(rol=Rol(pk=2))
            serializer.cliente.instance.set_password(serializer.instance.password)
            serializer.cliente.instance.save()
            token = Token.objects.get_or_create(user=serializer.instance)
            try:
                device = FCMDevice.objects.get(registration_id=serializer.validated_data.get('googleid'))
            except FCMDevice.DoesNotExist:
                device = FCMDevice(registration_id=serializer.validated_data.get('googleid'),
                                   name=serializer.cliente.instance.get_full_name(), user=serializer.cliente.instance)
            device.type = serializer.cliente.instance.procedencia
            device.save()
            return Response({'id': serializer.instance.pk, "token": str(token[0])}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return UsuarioEditSerializer()