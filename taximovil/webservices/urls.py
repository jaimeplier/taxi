from django.urls import path, include
from rest_framework import routers

from webservices import tarjeta, cliente
from webservices.catalogos import TipoPagoList, TipoVehiculoList
from webservices.choferes import ActualizarChofer, ChoferEstatus, CambiarEstatusServicio
from webservices.cliente import RegistrarUsuario
from webservices.servicios import BuscarCiudad, Cotizar, SolicitarServicio, TaxisCercanos
from webservices.views import EnviarCodigo, VerificaCodigo, LoginUsuario, ChangePassword, ResetPassword, \
    LoginChofer, LogoutCliente, LogoutChofer, VerChofer

app_name = 'webservices'

router = routers.DefaultRouter()
router.register(r'tarjeta', tarjeta.TarjetaViewSet)
router.register(r'direccion', cliente.DireccionViewSet)

urlpatterns = [
    # Router urls
    path('', include(router.urls)),
    # Auth urls
    path('enviarCodigo/', EnviarCodigo.as_view(), name='enviar_codigo'),
    path('verificarCodigo/', VerificaCodigo.as_view(), name='verifica_codigo'),
    path('registrar/', RegistrarUsuario.as_view(), name='registrar'),
    path('login/', LoginUsuario.as_view(), name='login'),
    path('logoutCliente', LogoutCliente.as_view(), name='logoutCliente'),
    path('logoutChofer', LogoutChofer.as_view(), name='logoutChofer'),
    path('modificarPassword', ChangePassword.as_view(), name='modficarPassword'),
    path('resetPassword/', ResetPassword.as_view(), name='reset_password'),
    path('loginChofer/', LoginChofer.as_view(), name='login_chofer'),
    path('estatusChofer/', ChoferEstatus.as_view(), name='estatus_chofer'),
    path('tipoPago/', TipoPagoList.as_view(), name='tipo_pago'),
    path('tipoVehiculo/', TipoVehiculoList.as_view(), name='tipo_vehiculo'),
    path('verChofer/', VerChofer.as_view(), name='ver_chofer'),
    path('actualizarChofer/', ActualizarChofer.as_view(), name='actualizar_chofer'),
    path('cambiarEstatusServicio/', CambiarEstatusServicio.as_view(), name='cambiar_estatus_servicio'),
    # Servicios
    path('buscarCiudad/', BuscarCiudad.as_view(), name='buscar_ciudad'),
    path('cotizar/', Cotizar.as_view(), name='cotizar'),
    path('solicitar/', SolicitarServicio.as_view(), name='solicitar'),
    path('taxis_cercanos/', TaxisCercanos.as_view(), name='taxis_cercanos')
]
