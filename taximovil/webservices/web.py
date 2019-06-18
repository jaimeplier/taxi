from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.models import Ciudad, ChoferHasVehiculo, Chofer, EstatusServicio, Servicio
from config.serializers import ServicioSerializer
from webservices.Pagination import SmallPagesPagination
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

class ListServicios(ListAPIView):
    """
        Parámetros:

            tipo_servicio:

                - 1 Para servicios notificados
                - 2 para servicios asignados
                - 3 Para servicios iniciados
                - 4 Para servicios concluidos
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = ServicioSerializer
    pagination_class = SmallPagesPagination


    def get_queryset(self):
        estatus_servicio = self.request.query_params.get('tipo_servicio', None)
        queryset = Servicio.objects.none()
        if estatus_servicio is not None:
            if estatus_servicio=='1':
                estatus_servicio = EstatusServicio.objects.get(pk=1)
            elif estatus_servicio=='2':
                queryset = Servicio.objects.filter(estatus__pk__in=[2,3,4]).order_by('hora_registro')
                return queryset
            elif estatus_servicio=='3':
                estatus_servicio = EstatusServicio.objects.get(pk=5)
            elif estatus_servicio=='4':
                estatus_servicio = EstatusServicio.objects.get(pk=6)
            else:
                return queryset
            queryset = Servicio.objects.filter(estatus=estatus_servicio).order_by('hora_registro')
        return queryset

