from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Chofer, EstatusServicio, Servicio, BitacoraEstatusServicio, BitacoraCredito, Vehiculo, \
    ChoferHasVehiculo
from config.serializers import AsignarVehiculoSerializer
from webservices.permissions import ChoferPermission, AdministradorPermission
from webservices.serializers import ActualizarChoferSerializer, ChoferEstatusSerializer, ServicioEstatusSerializer, \
    ChoferCreditoSerializer


class ChoferEstatus(APIView):
    """
    post:
        Cambiar estatus del chofer
    """
    permission_classes = (IsAuthenticated, ChoferPermission)

    def post(self, request):
        serializer = ChoferEstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = Chofer.objects.get(pk=request.user.pk)
        c.activo = serializer.validated_data.get('activo')
        c.save()
        return Response({'resultado': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ChoferEstatusSerializer()


class CambiarEstatusServicio(APIView):
    """
    post:
        Cambiar estatus del servicio
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = ServicioEstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            e = EstatusServicio.objects.get(pk=serializer.validated_data.get('estatus'))
            s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
            bs = BitacoraEstatusServicio(servicio=s, estatus=e)
            bs.save()
            Servicio.objects.filter(pk=serializer.validated_data.get('servicio')).update(estatus=e)
            return Response({'resultado': 1}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'resultado': 0, 'error': 'Estatus o servicio no encontrado'},
                            status=status.HTTP_404_NOT_FOUND)

    def get_serializer(self):
        return ServicioEstatusSerializer()


class ActualizarChofer(APIView):
    permission_classes = (IsAuthenticated, ChoferPermission)

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


class CreditoChofer(APIView):
    permission_classes = (IsAuthenticated, AdministradorPermission)

    def post(self, request):
        serializer = ChoferCreditoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = Chofer.objects.get(id=serializer.validated_data.get('chofer'))
        monto = serializer.validated_data.get('monto')
        if monto <= 0:
            return Response({"error": "El monto debe ser mayor a 0"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            c.saldo = c.saldo + monto
            c.save()
            bc = BitacoraCredito(chofer=c, usuario=request.user, monto=monto)
            bc.save()
        return Response({"result": 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ChoferCreditoSerializer()

class DesAsignarVehiculo(APIView):
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = AsignarVehiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_vehiculo = serializer.data.get('vehiculo')
        id_chofer = serializer.data.get('chofer')
        try:
            chofer = Chofer.objects.get(pk=id_chofer)
            vehiculo = Vehiculo.objects.get(pk=id_vehiculo)
            chofer_vehiculos = chofer.taxis.all().values_list('id', flat=True)
            if id_vehiculo in chofer_vehiculos:
                ChoferHasVehiculo.objects.filter(vehiculo=vehiculo, chofer=chofer).delete()
            else:
                ChoferHasVehiculo.objects.create(vehiculo=vehiculo, chofer=chofer)
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return AsignarVehiculoSerializer()