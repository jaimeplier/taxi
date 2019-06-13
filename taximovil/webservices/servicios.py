import datetime

import googlemaps
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Avg
from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad, Tarifa, Cliente, EstatusServicio, BitacoraEstatusServicio, Servicio, Chofer, Rutas, \
    Usuario, ChoferHasVehiculo, ServicioChofer, MonederoChofer, EstatusPago
from config.serializers import CiudadSerializer, TarifaSerializer, ServicioSerializer, ChoferSerializer
from taximovil import settings
from webservices.permissions import ChoferPermission, IsOwnerPermission
from webservices.serializers import CoordenadasSerializer, CotizarSerializer, SolicitarServicioSerializer, \
    ServicioPkSerializer, ChoferCoordenadasSerializer, RutaSerializer, CalificacionSerializer, ClienteTelSerializer
from webservices.tasks import cobra_servicio


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
    if servicio.tipo_pago.pk == 2:
        cc = cc.filter(saldo__gte=5)
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
    for c in cc:
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
        if duracion <= 900:
            return c
    return None


def distancia_ruta(servicio):
    r = Rutas.objects.filter(servicio__pk=servicio).order_by('fecha_registro')
    aux = None
    distancia = D(km=0)
    for rr in r:
        if aux is not None:
            d = Rutas.objects.filter(pk=rr.pk).annotate(distancia=Distance('punto', aux.punto)).first().distancia
            if (d.m / (rr.fecha_registro - aux.fecha_registro).seconds) > 38.88:
                continue
            distancia = distancia + d
        aux = rr
    return distancia.m


def precio_tarifa(t, distancia, duracion):
    precio = t.tarifa_base + t.costo_minuto * (duracion / 50)
    if distancia > t.distancia_max:
        dif_distancia = distancia - t.distancia_max
        precio = precio + t.distancia_max * t.costo_km + dif_distancia * t.costo_km * t.incremento_distancia
    else:
        precio = precio + distancia * t.costo_km
    if precio < t.costo_minimo:
        precio = t.costo_minimo
    return precio


def cobrar(servicio):
    if servicio.tipo_pago.pk == 1:
        c = servicio.tarifa.comision
        mc = MonederoChofer(servicio=servicio, chofer=servicio.chofer, ganancia=(servicio.costo * (1 - c)),
                            retencion=(servicio.costo * c), estatus_pago=EstatusPago(pk=2))
        mc.save()
        cobra_servicio(servicio.pk)
    elif servicio.tipo_pago.pk == 2:
        servicio.estatus_pago = EstatusPago(pk=1)
        c = servicio.chofer
        c.saldo = c.saldo - servicio.costo * servicio.tarifa.comision
        c.save()
        servicio.save()


class BuscarCiudad(APIView):
    """
        post:
        Recibe coordenadas
        -latitud
        -longitud

        Regresa ciudad de las coordenadas dadas
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
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

class BuscarTelefonoCliente(ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = ClienteTelSerializer

    def get_queryset(self):
        telefono = self.request.query_params.get('telefono', None)
        queryset = Cliente.objects.none()
        if telefono is not None:
            queryset = Cliente.objects.filter(telefono__icontains=telefono)
        return queryset


class Cotizar(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
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
        precio = precio_tarifa(t, distancia, duracion)
        tarifa = TarifaSerializer(t)
        return Response({"distance": distancia, "distance_text": distancia_text, "duracion": duracion,
                         "duracion_text": duracion_text, "precio": precio, "tarifa": tarifa.data},
                        status=status.HTTP_200_OK)

    def get_serializer(self):
        return CotizarSerializer()


class SolicitarServicio(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, SessionAuthentication)

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
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, IsOwnerPermission,)

    def post(self, request):
        serializer = ServicioPkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
        if s.estatus.pk == 2: # Servicio aceptado
            cserializer = ServicioSerializer(s, many=False)
            return Response({"servicio": cserializer.data, "estatus": 1}, status=status.HTTP_200_OK)
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
                    d = dispositivos.first()
                    sserializer = ServicioSerializer(s, many=False)
                    data_push = {'servicio': sserializer.data, 'result': '1'}
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
        c.activo = True
        s.save()
        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()


class FinalizarServicio(APIView):
    """
        post:Finalizar servicio
    """
    permission_classes = (IsAuthenticated,)

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
            bi = BitacoraEstatusServicio.objects.filter(servicio=s, estatus__pk=5).first()
            s.duracion = (bs.fecha - bi.fecha).seconds
            s.costo = precio_tarifa(s.tarifa, distancia_ruta(s.pk), (bs.fecha - bi.fecha).seconds)
            s.save()
            c = s.chofer
            c.activo = True
            c.save()
            cobrar(s)
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
        return Response({'result': 1, 'servicio': serializerServicio.data}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ServicioPkSerializer()


class CalificarServicio(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = CalificacionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if self.request.user.rol.pk == 2:  # cliente
            s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
            s.calificacion_cliente = serializer.validated_data.get('calificacion')
            s.save()
            c = s.chofer
            calif = Servicio.objects.filter(
                estatus__pk=6,
                chofer=c,
                calificacion_cliente__isnull=False).aggregate(calificacion=Avg('calificacion_cliente'))
            c.calificacion = calif['calificacion']
            c.save()
            return Response({'result': 1}, status=status.HTTP_200_OK)
        elif self.request.user.rol.pk == 3:  # chofer
            s = Servicio.objects.get(pk=serializer.validated_data.get('servicio'))
            s.calificacion_chofer = serializer.validated_data.get('calificacion')
            s.save()
            c = s.cliente
            calif = Servicio.objects.filter(
                estatus__pk=6,
                cliente=c,
                calificacion_chofer__isnull=False).aggregate(calificacion=Avg('calificacion_chofer'))
            c.calificacion = calif['calificacion']
            c.save()
            return Response({'result': 1}, status=status.HTTP_200_OK)
        else:
            return Response({'result': 0}, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer(self):
        return CalificacionSerializer()


class HistorialServicios(ListAPIView):
    serializer_class = ServicioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.rol.pk == 2:  # cliente
            s = Servicio.objects.filter(cliente__pk=self.request.user.pk, estatus__pk__in=(6, 7))
        elif self.request.user.rol.pk == 3:  # chofer
            s = Servicio.objects.filter(chofer__pk=self.request.user.pk, estatus__pk__in=(6, 7))
        else:
            s = Servicio.objects.none()
        return s
