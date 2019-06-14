from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad, ChoferHasVehiculo, Chofer
from webservices.permissions import AdministradorPermission
from webservices.serializers import CatalogoSerializer, ChoferHasVehiculoSerializer, EstatusSerializer


class ListCiudad(ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Ciudad.objects.all()
        return queryset

class ListVehiculoActivo(ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = ChoferHasVehiculoSerializer

    def get_queryset(self):
        queryset = ChoferHasVehiculo.objects.filter(estatus=True)
        return queryset

class CambiarEstatusChofer(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AdministradorPermission)

    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_usuario = serializer.data.get('pk')
        try:
            usuario = Chofer.objects.get(pk=id_usuario)
            if usuario.estatus:
                usuario.estatus = False
            else:
                usuario.estatus = True
            usuario.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusSerializer()