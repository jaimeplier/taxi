from fcm_django.models import FCMDevice
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Rol, DireccionServicio, Cliente, Servicio
from config.serializers import DireccionSerializer, DireccionEditSerializer
from webservices.serializers import UsuarioEditSerializer, UltimasDireccionSerializer


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


class DireccionViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = DireccionServicio.objects.all()

    def list(self, request):
        try:
            cliente = Cliente.objects.get(pk=self.request.user.pk)
        except Cliente.DoesNotExist:
            Response({"error": "El cliente no existe"}, status=status.HTTP_400_BAD_REQUEST)
        qs = DireccionServicio.objects.filter(cliente=cliente, estatus=True)
        serializer = DireccionSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        cliente = Cliente.objects.get(pk=self.request.user.pk)
        serializer = DireccionEditSerializer(data=self.request.data)
        if serializer.is_valid():
            d = DireccionServicio(cliente=cliente, nombre=serializer.validated_data.get('nombre'),
                                  direccion=serializer.validated_data.get('direccion'),
                                  estatus=serializer.validated_data.get('estatus'))
            d.set_point(serializer.validated_data.get('latitud'),
                        serializer.validated_data.get('longitud'))
            d.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request is None or self.request.method == 'POST':
            return DireccionEditSerializer
        else:
            return DireccionSerializer


class DireccionesPasadas(ListAPIView):
    serializer_class = UltimasDireccionSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        s = Servicio.objects.filter(cliente__pk=self.request.user.pk).order_by('-id')[:5]
        return s
