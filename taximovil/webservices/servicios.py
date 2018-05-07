from django.contrib.gis.geos import Point
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad
from config.serializers import CiudadSerializer
from webservices.serializers import CoordenadasSerializer


class BuscarCiudad(APIView):
    """
        post:
        Verifica el codigo enviado y regresa el resultado
        0 el cliente no esta registrado
        1 el cliente ya esta rgistrado con ese telefono
        -1 el codigo es inválido
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CoordenadasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.data.get('latitud')
        longitud = serializer.data.get('longitud')
        p = Point(longitud, latitud)
        cc = Ciudad.objects.filter(centro__distance_lt=(p, F('radio')))
        serializer = CiudadSerializer(cc, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return CoordenadasSerializer()
