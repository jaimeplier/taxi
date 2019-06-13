from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.models import Ciudad, ChoferHasVehiculo
from webservices.serializers import CatalogoSerializer, ChoferHasVehiculoSerializer


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