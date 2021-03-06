from datetime import datetime

from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Chofer, EstatusServicio, Servicio, BitacoraEstatusServicio, BitacoraCredito, Vehiculo, \
    ChoferHasVehiculo, MonederoChofer, EstatusPago
from config.serializers import AsignarVehiculoSerializer
from webservices.permissions import ChoferPermission, AdministradorPermission
from webservices.serializers import ActualizarChoferSerializer, ChoferEstatusSerializer, ServicioEstatusSerializer, \
    ChoferCreditoSerializer, AgregarSaldoSerializer


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
    authentication_classes = (TokenAuthentication, SessionAuthentication)
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


class LanaChofer(APIView):
    permission_classes = (IsAuthenticated, ChoferPermission)

    def get(self, request):
        c = Chofer.objects.get(pk=self.request.user)
        f = datetime.now().isocalendar()[1]
        actual_efectivo = Servicio.objects.filter(estatus__pk=6, chofer=c, hora_servicio__week=f,
                                                  tipo_pago__pk=2).aggregate(efectivo=Sum('costo'))['efectivo']
        actual_tarjeta = MonederoChofer.objects.filter(chofer=c, servicio__hora_servicio__week=f, estatus_pago__pk=2) \
            .aggregate(tar_total=Sum('ganancia'))['tar_total']
        pasada_efectivo = Servicio.objects.filter(estatus__pk=6, chofer=c, hora_servicio__week=(f - 1),
                                                  tipo_pago__pk=2).aggregate(efectivo=Sum('costo'))['efectivo']
        pasada_tarjeta = MonederoChofer.objects.filter(chofer=c, servicio__hora_servicio__week=(f - 1),
                                                       estatus_pago__pk=2).aggregate(tar_total=Sum('ganancia'))[
            'tar_total']
        return Response(
            {'efectivo_actual': actual_efectivo, 'tarjeta_actual': actual_tarjeta, 'efectivo_pasada': pasada_efectivo,
             'tarjeta_pasada': pasada_tarjeta}, status=status.HTTP_200_OK)


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


class AgregarSaldo(APIView):
    permission_classes = (IsAuthenticated, ChoferPermission)

    def post(self, request):
        serializer = AgregarSaldoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        monto = serializer.validated_data.get('monto')
        tipo_pago = serializer.validated_data.get('tipo_pago')
        chofer = Chofer.objects.get(pk=self.request.user.pk)
        bitacora = BitacoraCredito(usuario=self.request.user, chofer=chofer, monto=monto)
        bitacora.save()
        if tipo_pago == 3:
            mc = MonederoChofer.objects.filter(chofer=chofer, estatus_pago__pk=2).aggregate(tar_total=Sum('ganancia'))[
                'tar_total']
            if mc is not None and monto <= mc:
                chofer.saldo = chofer.saldo + monto
                mc = MonederoChofer.objects.filter(chofer=chofer, estatus_pago__pk=2)
                for m in mc:
                    if m.ganancia <= monto:
                        m.estatus_pago = EstatusPago(pk=1)
                        m.save()
                        monto = monto - m.ganancia
                        if monto == 0:
                            break
                    elif m.ganancia > monto:
                        m.retencion = m.retencion + monto
                        m.ganancia = m.ganancia - monto
                        m.save()
                        break
            else:
                return Response({'result': 0, "error": "No tienenes las ganancias suficientes"},
                                status=status.HTTP_200_OK)
        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return AgregarSaldoSerializer()
