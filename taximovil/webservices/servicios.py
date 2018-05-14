import datetime

import googlemaps
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad, Tarifa, Cliente, EstatusServicio, BitacoraEstatusServicio, Servicio, Chofer, Rutas, \
    Usuario, ChoferHasVehiculo, ServicioChofer
from config.serializers import CiudadSerializer, TarifaSerializer, ServicioSerializer, ChoferSerializer
from taximovil import settings
from webservices.permissions import IsOwnerPermission, ChoferPermission
from webservices.serializers import CoordenadasSerializer, CotizarSerializer, SolicitarServicioSerializer, \
    ServicioPkSerializer, ChoferCoordenadasSerializer, RutaSerializer


def buscar_tarifa(fecha, ciudad, tipo_vehiculo, tipo_servicio, sucursal=None, base=None):
    time = fecha.time()
    if sucursal is not None:
        t = Tarifa.objects.filter(sucursal__pk=sucursal, horario__diasemana=fecha.isoweekday(),
                                  horario__horainicio__lte=time, horario__horafin__gte=time)
        return t.first()
    tars = Tarifa.objects.filter(ciudad__pk=ciudad, tipo_vehiculo__pk=tipo_vehiculo, tipo_servicio__pk=tipo_servicio,
                                 horario__diasemana=fecha.isoweekday(), horario__horainicio__lte=time,
                                 horario__horafin__gte=time)
    if base is not None:
        tars = tars.filter(base__pk=tars)
    return tars.first()


def buscar_choferes(servicio):
    cc = Chofer.objects.filter(estatus=True, activo=True, latlgn__distance_lte=(servicio.origen, D(km=5)))
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
    for c in cc:
        print(c)
        check = ServicioChofer.objects.filter(servicio=servicio, chofer=c).first()
        if check is not None:
            if check.estatus == 1:
                return c
            if check.estatus == 2:
                continue
        origen = (c.latitud, c.longitud)
        destino = (servicio.origen.coords[1], servicio.origen.coords[0])
        directions_result = gmaps.distance_matrix(origen, destino, departure_time=datetime.datetime.now(),
                                                  traffic_model='best_guess')
        duracion = directions_result['rows'][0]['elements'][0]['duration_in_traffic']['value']
        print(duracion)
        if duracion <= 900:
            return c
    return None


class BuscarCiudad(APIView):
    """
        post:
        Verifica el codigo enviado y regresa el resultado
        0 el cliente no esta registrado
        1 el cliente ya esta rgistrado con ese telefono
        -1 el codigo es inválido
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CoordenadasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.data.get('latitud')
        longitud = serializer.data.get('longitud')
        p = Point(longitud, latitud)
        cc = Ciudad.objects.filter(centro__distance_lt=(p, F('radio'))).first()
        serializer = CiudadSerializer(cc, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return CoordenadasSerializer()


class Cotizar(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CotizarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fecha = serializer.validated_data.get('fecha')
        ciudad = serializer.validated_data.get('ciudad')
        tipo_vehiculo = serializer.validated_data.get('tipo_vehiculo')
        tipo_servicio = serializer.validated_data.get('tipo_servicio')
        sucursal = serializer.validated_data.get('sucursal')
        base = serializer.validated_data.get('base')
        lat_origen = serializer.data.get('lat_origen')
        lon_origen = serializer.data.get('lon_origen')
        origen = (lat_origen, lon_origen)
        lat_destino = serializer.data.get('lat_destino')
        lon_destino = serializer.data.get('lon_destino')
        destino = (lat_destino, lon_destino)
        t = buscar_tarifa(fecha, ciudad, tipo_vehiculo, tipo_servicio, sucursal, base)
        if t is None:
            return Response({"error": "No se encontraron tarifas para la solicitud"}, status=status.HTTP_200_OK)
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
        if tipo_servicio == 1:
            directions_result = gmaps.distance_matrix(origen, destino, departure_time=datetime.datetime.now(),
                                                      traffic_model='best_guess')
        else:
            directions_result = gmaps.distance_matrix(origen, destino, departure_time=fecha,
                                                      traffic_model='best_guess')
        distancia = directions_result['rows'][0]['elements'][0]['distance']['value'] / 1000
        distancia_text = directions_result['rows'][0]['elements'][0]['distance']['text']
        duracion = directions_result['rows'][0]['elements'][0]['duration_in_traffic']['value']
        duracion_text = directions_result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        precio = t.tarifa_base + t.costo_minuto * (duracion / 50)
        if distancia > t.distancia_max:
            dif_distancia = distancia - t.distancia_max
            precio = precio + t.distancia_max * t.costo_km + dif_distancia * t.costo_km * t.incremento_distancia
        else:
            precio = precio + distancia * t.costo_km
        if precio < t.costo_minimo:
            precio = t.costo_minimo
        tarifa = TarifaSerializer(t)
        return Response({"distance": distancia, "distance_text": distancia_text, "duracion": duracion,
                         "duracion_text": duracion_text, "precio": precio, "tarifa": tarifa.data},
                        status=status.HTTP_200_OK)

    def get_serializer(self):
        return CotizarSerializer()


class SolicitarServicio(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        c = Cliente.objects.get(pk=request.user.pk)
        e = EstatusServicio(pk=1)
        serializer = SolicitarServicioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('tipo_pago').pk == 1:
            if serializer.validated_data.get('tarjeta') is None:
                return Response({"error": "La forma de pago necesito una tarjeta"}, status=status.HTTP_201_CREATED)
        serializer.save(cliente=c, estatus=e)
        b = BitacoraEstatusServicio(estatus=e, servicio=serializer.instance)
        b.save()
        ser = ServicioSerializer(serializer.instance, many=False)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def get_serializer(self):
        return SolicitarServicioSerializer()


class BuscarChofer(APIView):
    permission_classes = (IsAuthenticated, IsOwnerPermission,)

    def post(self, request):
        serializer = ServicioPkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
        if s.estatus.pk == 2:
            cserializer = ChoferSerializer(s.chofer, many=False)
            return Response({"chofer": cserializer.data, "estatus": 1}, status=status.HTTP_200_OK)
        c = buscar_choferes(s)
        if c is None:
            return Response({"error", "No se encontro ningun chofer"}, status=status.HTTP_200_OK)
        else:
            cserializer = ChoferSerializer(c, many=False)
            if ServicioChofer.objects.filter(servicio=s, chofer=c).count() > 0:
                sc = ServicioChofer.objects.filter(servicio=s, chofer=c)
                sc.update(estatus=1)
            else:
                sc = ServicioChofer(servicio=s, chofer=c, estatus=1)
                sc.save()
                u = Usuario.objects.get(pk=c.pk)
                dispositivos = FCMDevice.objects.filter(user=u)
                if dispositivos.count() != 0:
                    data_push = {}
                    d = dispositivos.first()
                    sserializer = ServicioSerializer(s, many=False)
                    data_push['servicio'] = sserializer.data
                    try:
                        d.send_message(data=data_push)
                    except Exception as e:
                        pass
            return Response({"chofer": cserializer.data, "estatus": 0}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()


class TaxisCercanos(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CoordenadasSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.data.get('latitud')
        longitud = serializer.data.get('longitud')
        p = Point(longitud, latitud)
        cc = Chofer.objects.filter(estatus=True, activo=True, latlgn__distance_lte=(p, D(km=2))).annotate(
            distance=Distance('latlgn', p))
        cserializer = ChoferCoordenadasSerializer(cc, many=True)
        return Response(cserializer.data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return CoordenadasSerializer()


class GuardarRuta(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = RutaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        latitud = serializer.data.get('latitud')
        longitud = serializer.data.get('longitud')
        p = Point(longitud, latitud)
        try:
            servicio = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
            r = Rutas(servicio=servicio, punto=p)
            r.save()
        except ObjectDoesNotExist:
            Response({'resultado': 0, 'error': 'Servicio no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'resultado': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return RutaSerializer()


class AceptarServicioView(APIView):
    """
            post:Aceptar servicio
    """
    permission_classes = (IsAuthenticated, ChoferPermission,)

    def post(self, request):
        response_data = {}
        serializer = ServicioPkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
        c = Chofer.objects.get(pk=request.user.pk)
        if s.chofer is None or s.chofer == c:
            if s.estatus.pk == (1):
                e = EstatusServicio(pk=2)
                bs = BitacoraEstatusServicio(servicio=s, estatus=e)
                bs.save()
                s.estatus = e
                s.chofer = c
                cv = ChoferHasVehiculo.objects.filter(chofer=c, estatus=True)
                cv = cv.first()
                s.vehiculo = cv.vehiculo
                s.save()
                if s.tipo_servicio.pk == 1:
                    c.activo = 0
                    c.save()
                u = Usuario.objects.get(pk=s.cliente.pk)
                dispositivos = FCMDevice.objects.filter(user=u)
                if dispositivos.count() != 0:
                    data_push = {}
                    d = dispositivos.first()
                    serializerServicio = ServicioSerializer(s, many=False)
                    data_push['servicio'] = serializerServicio.data
                    try:
                        d.send_message(title='El conductor acepto tu servicio',
                                       body='Se acepto el servicio' + str(s.pk), data=data_push)
                    except Exception as e:
                        pass
                # c = s.cliente
                # subject = "Servicio aceptado"
                # to = [c.email]
                # ctx = {
                #     'request': request,
                #     'servicio': s
                # }
                # message = get_template('correos/mail-confirma-asociado.html').render(ctx)
                # sendMail.delay(to, subject, message)
            else:
                response_data['error'] = 'El Servicio no esta en estatus para ser aceptado'
                response_data['result'] = 0
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data['error'] = 'Este conductor no puede aceptar el servicio'
            response_data['result'] = 0
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()


class RechazarServicioView(APIView):
    """
        post:Rechazar servicio chofer
    """
    permission_classes = (IsAuthenticated, ChoferPermission,)

    def post(self, request):
        serializer = ServicioPkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
        c = Chofer.objects.get(pk=request.user.pk)

        try:
            aso = ServicioChofer.objects.get(chofer=c, servicio=s)
            aso.estatus = 2
            aso.save()
        except ServicioChofer.DoesNotExist:
            aso = ServicioChofer(chofer=c, servicio=s, estatus=2)
            aso.save()
        return Response(status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()


class FinalizarServicio(APIView):
    """
        post:Finalizar servicio
    """
    permission_classes = (IsAuthenticated)

    def post(self, request):
        response_data = {}
        serializer = ServicioPkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
        if s.estatus.pk == 5:
            e = EstatusServicio(pk=6)
            bs = BitacoraEstatusServicio(servicio=s, estatus=e)
            bs.save()
            s.estatus = e
            s.save()
            # TODO cobrar
            u = Usuario.objects.get(pk=s.cliente.pk)
            dispositivos = FCMDevice.objects.filter(user=u)
            if dispositivos.count() != 0:
                data_push = {}
                d = dispositivos.first()
                serializerServicio = ServicioSerializer(s, many=False)
                data_push['servicio'] = serializerServicio.data
                try:
                    d.send_message(title='Has finalizado el servicio',
                                   body='El servicio fue finalizado', data=data_push)
                except Exception as e:
                    pass
        else:
            response_data['error'] = 'No se puede finalizar el servicio'
            response_data['result'] = 0
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()
