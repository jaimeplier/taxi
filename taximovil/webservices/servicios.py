import googlemaps
from django.contrib.gis.geos import Point
from django.db.models import F
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad, Tarifa
from config.serializers import CiudadSerializer
from taximovil import settings
from webservices.serializers import CoordenadasSerializer, CotizarSerializer


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
        cc = Ciudad.objects.filter(centro__distance_lt=(p, F('radio'))).first()
        serializer = CiudadSerializer(cc, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer(self):
        return CoordenadasSerializer()


class Cotizar(APIView):
    permission_classes = (AllowAny,)

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
        directions_result = gmaps.distance_matrix(origen, destino, departure_time=fecha, traffic_model='pessimistic')
        distancia = directions_result['rows'][0]['elements'][0]['distance']['value'] / 1000
        distancia_text = directions_result['rows'][0]['elements'][0]['distance']['text']
        duracion = directions_result['rows'][0]['elements'][0]['duration_in_traffic']['value'] / 50
        duracion_text = directions_result['rows'][0]['elements'][0]['duration_in_traffic']['text']
        precio = t.tarifa_base + t.costo_minuto * duracion
        if distancia > t.distancia_max:
            dif_distancia = distancia - t.distancia_max
            precio = precio + t.distancia_max * t.costo_km + dif_distancia * t.costo_km * t.incremento_distancia
        else:
            precio = precio + distancia * t.costo_km
        if precio < t.costo_minimo:
            precio = t.costo_minimo
        return Response({"distance": distancia, "dsitance_text": distancia_text, "duracion": duracion,
                         "duracion_text": duracion_text, "precio": precio}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return CotizarSerializer()
