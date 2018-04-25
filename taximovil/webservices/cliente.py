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
            serializer.save(rol=Rol(pk=2))
            serializer.instance.set_password(serializer.instance.password)
            serializer.instance.save()
            token = Token.objects.get_or_create(user=serializer.instance)
            try:
                device = FCMDevice.objects.get(registration_id=serializer.instance.googleid)
            except FCMDevice.DoesNotExist:
                device = FCMDevice(registration_id=serializer.instance.googleid,
                                   name=serializer.instance.get_full_name(), user=serializer.instance)
            device.type = serializer.instance.procedencia
            device.save()
            return Response({'id': serializer.instance.pk, "token": str(token[0])}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return UsuarioEditSerializer()