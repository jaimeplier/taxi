from django.urls import path, include
from rest_framework import routers

from webservices import tarjeta, cliente
from webservices.catalogos import TipoPagoList, TipoVehiculoList
from webservices.choferes import ActualizarChofer, ChoferEstatus, CambiarEstatusServicio, CreditoChofer
from webservices.cliente import RegistrarUsuario
from webservices.servicios import BuscarCiudad, Cotizar, SolicitarServicio, TaxisCercanos, GuardarRuta, \
    AceptarServicioView, RechazarServicioView, BuscarChofer, FinalizarServicio
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
    path('creditoChofer/', CreditoChofer.as_view(), name='credito_chofer'),
    # Servicios
    path('buscarCiudad/', BuscarCiudad.as_view(), name='buscar_ciudad'),
    path('cotizar/', Cotizar.as_view(), name='cotizar'),
    path('solicitar/', SolicitarServicio.as_view(), name='solicitar'),
    path('buscarChofer/', BuscarChofer.as_view(), name='buscar_chofer'),
    path('taxis_cercanos/', TaxisCercanos.as_view(), name='taxis_cercanos'),
    path('cambiarEstatusServicio/', CambiarEstatusServicio.as_view(), name='cambiar_estatus_servicio'),
    path('guardarRuta/', GuardarRuta.as_view(), name='guardar_ruta'),
    path('aceptarServicio/', AceptarServicioView.as_view(), name='aceptar_servicio'),
    path('rechazarServicio/', RechazarServicioView.as_view(), name='rechzar_servicio'),
    path('finalizarServicio/', FinalizarServicio.as_view(), name='finalizar_servicio'),
]
