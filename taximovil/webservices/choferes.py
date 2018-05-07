from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Chofer
from webservices.permissions import ChoferPermission
from webservices.serializers import ActualizarChoferSerializer, ChoferEstatusSerializer


class ChoferEstatus(APIView):
    """
    post:
        Cambiar estatus del chofer
    """
    permission_classes = (IsAuthenticated, ChoferPermission)

    def post(self,request):
        serializer = ChoferEstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = Chofer.objects.get(pk=request.user.pk)
        c.activo = serializer.validated_data.get('activo')
        c.save()
        return Response({'resultado': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ChoferEstatusSerializer()


class ActualizarChofer(APIView):
    permission_classes = (IsAuthenticated,ChoferPermission)

    def post(self, request):
        serializer = ActualizarChoferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = Chofer.objects.get(id=request.user.pk)
        if c is not None:
            lat = serializer.validated_data.get('lat')
            lon = serializer.validated_data.get('lon')
            p = Point(float(lon), float(lat))
            c.latlgn = p
            c.save()
        else:
            return Response({"error": "Datos incorrectos"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"result": 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ActualizarChoferSerializer()