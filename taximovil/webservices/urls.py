from django.urls import path, include
from rest_framework import routers

from webservices import tarjeta, cliente
from webservices.catalogos import TipoPagoList, TipoVehiculoList
from webservices.choferes import ActualizarChofer, ChoferEstatus, CambiarEstatusServicio, CreditoChofer, LanaChofer, \
    DesAsignarVehiculo, AgregarSaldo
from webservices.cliente import RegistrarUsuario, DireccionesPasadas
from webservices.servicios import BuscarCiudad, Cotizar, SolicitarServicio, TaxisCercanos, GuardarRuta, \
    AceptarServicioView, RechazarServicioView, BuscarChofer, FinalizarServicio, CalificarServicio, HistorialServicios, \
    BuscarTelefonoCliente, SolicitarServicioWeb
from webservices.views import EnviarCodigo, VerificaCodigo, LoginUsuario, ChangePassword, ResetPassword, \
    LoginChofer, LogoutCliente, LogoutChofer, VerChofer, InicioApp, CambiarNombre
from webservices.web import ListCiudad, ListVehiculoActivo, CambiarEstatusChofer, ListServicios, \
    CambiarEstatusCallcenter, CambiarEstatusAdminSitio, CambiarEstatusAdminCiudad, AgregarDireccionCliente, \
    AsignarChofer, ChoferActivoEstatus

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
    path('modificarPassword/', ChangePassword.as_view(), name='modficarPassword'),
    path('resetPassword/', ResetPassword.as_view(), name='reset_password'),
    path('loginChofer/', LoginChofer.as_view(), name='login_chofer'),
    path('estatusChofer/', ChoferEstatus.as_view(), name='estatus_chofer'),
    path('tipoPago/', TipoPagoList.as_view(), name='tipo_pago'),
    path('tipoVehiculo/', TipoVehiculoList.as_view(), name='tipo_vehiculo'),
    path('verChofer/', VerChofer.as_view(), name='ver_chofer'),
    path('actualizarChofer/', ActualizarChofer.as_view(), name='actualizar_chofer'),
    path('creditoChofer/', CreditoChofer.as_view(), name='credito_chofer'),
    path('inicioApp/', InicioApp.as_view(), name='inicio_app'),
    # Cliente
    path('direccionesPasadas/', DireccionesPasadas.as_view(), name='direcciones_pasadas'),
    path('cambiaNombre/', CambiarNombre.as_view(), name='cambiar_nombre'),
    # Servicios
    path('buscarCiudad/', BuscarCiudad.as_view(), name='buscar_ciudad'),
    path('buscarTelefonoCliente/', BuscarTelefonoCliente.as_view(), name='buscar_telefono_cliente'),
    path('cotizar/', Cotizar.as_view(), name='cotizar'),
    path('solicitar/', SolicitarServicio.as_view(), name='solicitar'),
    path('solicitar_servicio_web/', SolicitarServicioWeb.as_view(), name='solicitar_servicio_web'),
    path('buscarChofer/', BuscarChofer.as_view(), name='buscar_chofer'),
    path('taxis_cercanos/', TaxisCercanos.as_view(), name='taxis_cercanos'),
    path('cambiarEstatusServicio/', CambiarEstatusServicio.as_view(), name='cambiar_estatus_servicio'),
    path('guardarRuta/', GuardarRuta.as_view(), name='guardar_ruta'),
    path('aceptarServicio/', AceptarServicioView.as_view(), name='aceptar_servicio'),
    path('rechazarServicio/', RechazarServicioView.as_view(), name='rechzar_servicio'),
    path('finalizarServicio/', FinalizarServicio.as_view(), name='finalizar_servicio'),
    path('calificarServicio/', CalificarServicio.as_view(), name='calificar_servicio'),
    path('listaServicios/', HistorialServicios.as_view(), name='lista_servicios'),
    path('lana_choferas/', LanaChofer.as_view(), name='lana_choferes'),
    path('agrega_sado/', AgregarSaldo.as_view(), name='agrega_saldo'),
    path('asignar_vehiculo_toogle/', DesAsignarVehiculo.as_view(), name='asignar_vehiculo_toogle'),
    # Web
    path('cambiar_estatus_chofer/', CambiarEstatusChofer.as_view(), name='cambiar_estatus_chofer'),
    path('cambiar_estatus_activo_chofer/', ChoferActivoEstatus.as_view(), name='cambiar_estatus_activo_chofer'),
    path('asignar_chofer/', AsignarChofer.as_view(), name='asignar_chofer'),
    path('list_ciudades/', ListCiudad.as_view(), name='list_ciudades'),
    path('list_vehiculos_activos/', ListVehiculoActivo.as_view(), name='list_vehiculos_activos'),
    path('list_servicios/', ListServicios.as_view(), name='list_servicios'),
    path('add_direccion_cliente/', AgregarDireccionCliente.as_view(), name='add_direccion_cliente'),
    # Administrador softic
    path('cambiar_estatus_admin_ciudad/', CambiarEstatusAdminCiudad.as_view(), name='cambiar_estatus_admin_ciudad'),
    # Administrador de sitio
    path('cambiar_estatus_callcenter/', CambiarEstatusCallcenter.as_view(), name='cambiar_estatus_callcenter'),
    # Administrador de ciudad
    path('cambiar_estatus_admin_sitio/', CambiarEstatusAdminSitio.as_view(), name='cambiar_estatus_admin_sitio'),

]
