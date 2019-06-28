from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_ciudad.utils import is_callcenter_owner
from config.models import Ciudad, ChoferHasVehiculo, Chofer, EstatusServicio, Servicio, Callcenter, AdministradorSitio, \
    ConfigUsuariosSitio, AdministradorCiudad, DireccionServicio, Cliente, BitacoraEstatusServicio, Usuario
from config.serializers import ServicioSerializer, CiudadSerializer, DireccionClienteSerializer, DireccionSerializer
from webservices.Pagination import SmallPagesPagination
from webservices.permissions import AdministradorPermission, AdministradorSitioPermission, \
    AdministradorCiudadPermission, CallcenterPermission, ChoferPermission
from webservices.serializers import CatalogoSerializer, ChoferHasVehiculoSerializer, EstatusSerializer, \
    AsignarChoferSerializer, ChoferEstatusActivoSerializer


class ListCiudad(ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = CiudadSerializer

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

class AsignarChofer(APIView):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated, CallcenterPermission)

    def post(self, request):
        serializer = AsignarChoferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        id_chofer = serializer.validated_data.get('chofer')
        id_servicio = serializer.validated_data.get('servicio')
        try:
            chofer = Chofer.objects.get(pk=id_chofer)
            servicio = Servicio.objects.get(pk=id_servicio)
            estatus_servicio = EstatusServicio.objects.get(pk=2)
            if chofer.activo and servicio.estatus.pk==1:
                bs = BitacoraEstatusServicio(servicio=servicio, estatus=estatus_servicio)
                bs.save()
                servicio.estatus = estatus_servicio
                servicio.chofer = chofer
                cv = ChoferHasVehiculo.objects.filter(chofer=chofer, estatus=True)
                cv = cv.first()
                servicio.vehiculo = cv.vehiculo
                servicio.save()
                chofer.estatus = False
                chofer.save()
                u = Usuario.objects.get(pk=chofer.pk)
                dispositivos = FCMDevice.objects.filter(user=u)
                if dispositivos.count() != 0:
                    data_push = {}
                    d = dispositivos.first()
                    serializerServicio = ServicioSerializer(servicio, many=False)
                    data_push['servicio'] = serializerServicio.data
                    try:
                        d.send_message(title='Tienes un nuevo servicio',
                                       body='Se te asignó el servicio' + str(servicio.pk), data=data_push)
                    except Exception as e:
                        pass

            else:
                return Response({'Error': 'No puede asignar el servicio a éste chofer o el servicio ya fue aceptado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return AsignarChoferSerializer()

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

class CambiarEstatusAdminCiudad(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AdministradorPermission)

    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            admin_ciudad = AdministradorCiudad.objects.get(pk=serializer.validated_data.get('pk'))
            if admin_ciudad.estatus:
                admin_ciudad.estatus = False
            else:
                admin_ciudad.estatus = True
            admin_ciudad.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusSerializer()

class AgregarDireccionCliente(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = DireccionClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            cliente = Cliente.objects.get(pk=serializer.validated_data.get('cliente'))
            direccion = DireccionServicio(cliente=cliente, nombre=serializer.validated_data.get('nombre'),
                                  direccion=serializer.validated_data.get('direccion'))
            direccion.set_point(serializer.validated_data.get('latitud'),
                        serializer.validated_data.get('longitud'))
            direccion.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return DireccionClienteSerializer()

class CambiarEstatusCallcenter(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AdministradorSitioPermission)

    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            callcenter = Callcenter.objects.get(pk=serializer.data.get('pk'))
            config_sitio = ConfigUsuariosSitio.objects.get(sitio=callcenter.sitio)
            if self.request.user.is_admin_sitio:
                admin_sitio = AdministradorSitio.objects.get(pk=self.request.user.pk)
                usuarios_callcenter = Callcenter.objects.filter(sitio=admin_sitio.sitio).values_list('pk', flat=True)
                if callcenter.pk in usuarios_callcenter:
                    if callcenter.estatus:
                        callcenter.estatus = False
                    else:
                        num_usuarios_callcenter = Callcenter.objects.filter(sitio=admin_sitio.sitio, estatus=True).count()
                        if num_usuarios_callcenter >= config_sitio.max_callcenter:
                            return Response({'Error': 'Estan registrados ' + str(
                                                       num_usuarios_callcenter) + ' usuarios activos de ' +
                                                            str(
                                                                config_sitio.max_callcenter) + ' permitidos, no puedes activar mas.'},
                                            status=status.HTTP_401_UNAUTHORIZED)
                        callcenter.estatus = True
                    callcenter.save()
                else:
                    return Response({'Error': 'No puedes realizar cambios a éste usuario'}, status=status.HTTP_403_FORBIDDEN)
            elif self.request.user.is_admin_ciudad:
                if is_callcenter_owner(self.request.user, callcenter):
                    if callcenter.estatus:
                        callcenter.estatus = False
                    else:
                        num_usuarios_callcenter = Callcenter.objects.filter(sitio=callcenter.sitio, estatus=True).count()
                        if num_usuarios_callcenter >= config_sitio.max_callcenter:
                            return Response({'Error': 'Estan registrados ' + str(
                                                       num_usuarios_callcenter) + ' usuarios activos de ' +
                                                            str(
                                                                config_sitio.max_callcenter) + ' permitidos, no puedes activar mas.'},
                                            status=status.HTTP_401_UNAUTHORIZED)
                        callcenter.estatus = True
                    callcenter.save()
                else:
                    return Response({'Error': 'No puedes realizar cambios a éste usuario'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if callcenter.estatus:
                    callcenter.estatus = False
                else:
                    num_usuarios_callcenter = Callcenter.objects.filter(sitio=callcenter.sitio, estatus=True).count()
                    if num_usuarios_callcenter >= config_sitio.max_callcenter:
                        return Response({'Error': 'Estan registrados ' + str(
                            num_usuarios_callcenter) + ' usuarios activos de ' +
                                                  str(
                                                      config_sitio.max_callcenter) + ' permitidos, no puedes activar mas.'},
                                        status=status.HTTP_401_UNAUTHORIZED)
                    callcenter.estatus = True
                callcenter.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusSerializer()



class CambiarEstatusAdminSitio(APIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, AdministradorCiudadPermission)

    def post(self, request):
        serializer = EstatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            admin_sitio = AdministradorSitio.objects.get(pk=serializer.data.get('pk'))
            config_sitio = ConfigUsuariosSitio.objects.get(sitio=admin_sitio.sitio)
            if self.request.user.is_admin_ciudad:
                admin_ciudad= AdministradorCiudad.objects.get(pk=self.request.user.pk)
                usuarios_admin_sitio = AdministradorSitio.objects.filter(sitio=admin_sitio.sitio, sitio__admin_ciudad=admin_ciudad).values_list('pk', flat=True)
                if admin_sitio.pk in usuarios_admin_sitio:
                    if admin_sitio.estatus:
                        admin_sitio.estatus = False
                    else:
                        num_usuarios_admin_sitio = AdministradorSitio.objects.filter(sitio=admin_sitio.sitio, estatus=True).count()
                        if num_usuarios_admin_sitio >= config_sitio.max_administradores:
                            return Response({'Error': 'Estan registrados ' + str(
                                                       num_usuarios_admin_sitio) + ' usuarios activos de ' +
                                                            str(
                                                                config_sitio.max_administradores) + ' permitidos, no puedes activar mas.'},
                                            status=status.HTTP_401_UNAUTHORIZED)
                        admin_sitio.estatus = True
                    admin_sitio.save()
                else:
                    return Response({'Error': 'No puedes realizar cambios a éste usuario'}, status=status.HTTP_403_FORBIDDEN)
            else:
                if admin_sitio.estatus:
                    admin_sitio.estatus = False
                else:
                    num_usuarios_admin_sitio = AdministradorSitio.objects.filter(sitio=admin_sitio.sitio,
                                                                                 estatus=True).count()
                    if num_usuarios_admin_sitio >= config_sitio.max_administradores:
                        return Response({'Error': 'Estan registrados ' + str(
                            num_usuarios_admin_sitio) + ' usuarios activos de ' +
                                                  str(
                                                      config_sitio.max_administradores) + ' permitidos, no puedes activar mas.'},
                                        status=status.HTTP_401_UNAUTHORIZED)
                    admin_sitio.estatus = True
                admin_sitio.save()
        except:
            return Response({'Error': 'Objeto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'result': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return EstatusSerializer()

class ChoferActivoEstatus(APIView):
    """
    post:
        Cambiar estatus del chofer
    """
    #authentication_classes = (SessionAuthentication, TokenAuthentication)
    #permission_classes = (IsAuthenticated, ChoferPermission)

    def post(self, request):
        serializer = ChoferEstatusActivoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        c = Chofer.objects.get(pk=serializer.validated_data.get('chofer'))
        c.activo = serializer.validated_data.get('activo')
        c.save()
        return Response({'resultado': 1}, status=status.HTTP_200_OK)

    def get_serializer(self):
        return ChoferEstatusActivoSerializer()