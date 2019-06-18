from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.models import TipoPago, TipoVehiculo
from config.serializers import TipoPagoSerializer, TipoVehiculoSerializer


class TipoPagoList(ListAPIView):
    serializer_class = TipoPagoSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TipoPago.objects.all()
        ciudad = self.request.query_params.get('ciudad', None)
        tipo_vehiculo = self.request.query_params.get('tipo_vehiculo', None)
        if ciudad is None or tipo_vehiculo is None:
            queryset = TipoPago.objects.none()
        else:
            queryset = queryset.filter(tarifa__tipo_vehiculo__pk=tipo_vehiculo, tarifa__ciudad__pk=ciudad)
        return queryset


class TipoVehiculoList(ListAPIView):
    serializer_class = TipoVehiculoSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = TipoVehiculo.objects.all()
        ciudad = self.request.query_params.get('ciudad', None)
        if ciudad is None:
            queryset = TipoPago.objects.none()
        else:
            queryset = queryset.filter(tarifa__ciudad__pk=ciudad)
        return queryset
