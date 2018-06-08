from django.urls import path

from webapp.views import UsuarioCrear, UsuarioListarAjaxListView, UsuarioActualizar, EmpresaCrear, \
    EmpresaListarAjaxListView, EmpresaActualizar, ChoferCrear, ChoferListarAjaxListView, ChoferActualizar, SitioCrear, \
    SitioListarAjaxListView, SitioActualizar, ZonaCrear, ZonaListarAjaxListView, ZonaActualizar, BaseCrear, \
    BaseListarAjaxListView, PaisCrear, PaisListarAjaxListView, PaisActualizar, CiudadCrear, CiudadListarAjaxListView, \
    CiudadActualizar, SucursalCrear, SucursalListarAjaxListView, SucursalActualizar, FormaPagoCrear, \
    FormaPagoListarAjaxListView, FormaPagoActualizar, TipoVehiculoCrear, TipoVehiculoListarAjaxListView, \
    TipoVehiculoActualizar, BaseActualizar, ClienteCrear, ClienteListarAjaxListView, ClienteActualizar, \
    TipoServicioCrear, TipoServicioListarAjaxListView, TipoServicioActualizar, MarcaCrear, MarcaListarAjaxListView, \
    MarcaActualizar, ModeloCrear, ModeloListarAjaxListView, ModeloActualizar, PropietarioCrear, \
    PropietarioListarAjaxListView, PropietarioActualizar, VehiculoCrear, VehiculoListarAjaxListView, VehiculoActualizar, \
    TarifaListarAjaxListView, TarifaCrear, TarifaActualizar, ComisionCrear, ComisionListarAjaxListView, \
    ComisionActualizar, RolCrear, RolListarAjaxListView, RolActualizar, ServiciosActivosAjaxList, \
    ServiciosFinalizadosAjaxList, ChoferUbicacion
from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('rol/nuevo/', RolCrear.as_view(), name='nuevo_rol'),
    path('rol/listar/', views.rol_listar, name='list_rol'),
    path('tabla_rol/', RolListarAjaxListView.as_view(), name='tab_list_rol'),
    path('rol/editar/<int:pk>', RolActualizar.as_view(), name='edit_rol'),
    path('rol/listar/delete/<int:pk>', views.rol_eliminar, name='delete_rol'),

    path('empresa/nuevo/', EmpresaCrear.as_view(), name='nuevo_empresa'),
    path('empresa/listar/', views.empresa_listar, name='list_empresa'),
    path('tabla_empresa/', EmpresaListarAjaxListView.as_view(), name='tab_list_empresa'),
    path('empresa/editar/<int:pk>', EmpresaActualizar.as_view(), name='edit_empresa'),
    path('empresa/listar/delete/<int:pk>', views.empresa_eliminar, name='delete_empresa'),

    path('usuario/nuevo/', UsuarioCrear.as_view(), name='nuevo_usuario'),
    path('usuario/listar/', views.usuario_listar, name='list_usuario'),
    path('tabla_usuario/', UsuarioListarAjaxListView.as_view(), name='tab_list_usuario'),
    path('usuario/editar/<int:pk>', UsuarioActualizar.as_view(), name='edit_usuario'),
    path('usuario/listar/delete/<int:pk>', views.usuario_eliminar, name='delete_usuario'),

    path('chofer/nuevo/', ChoferCrear.as_view(), name='nuevo_chofer'),
    path('chofer/listar/', views.chofer_listar, name='list_chofer'),
    path('tabla_chofer/', ChoferListarAjaxListView.as_view(), name='tab_list_chofer'),
    path('chofer/editar/<int:pk>', ChoferActualizar.as_view(), name='edit_chofer'),
    path('chofer/listar/delete/<int:pk>', views.chofer_eliminar, name='delete_chofer'),
    path('chofer/ubicacion/<int:pk>', ChoferUbicacion.as_view(), name='ubicacion_chofer'),

    path('sitio/nuevo/', SitioCrear.as_view(), name='nuevo_sitio'),
    path('sitio/listar/', views.sitio_listar, name='list_sitio'),
    path('tabla_sitio/', SitioListarAjaxListView.as_view(), name='tab_list_sitio'),
    path('sitio/editar/<int:pk>', SitioActualizar.as_view(), name='edit_sitio'),
    path('sitio/listar/delete/<int:pk>', views.sitio_eliminar, name='delete_sitio'),

    path('zona/nuevo/', ZonaCrear.as_view(), name='nuevo_zona'),
    path('zona/listar/', views.zona_listar, name='list_zona'),
    path('tabla_zona/', ZonaListarAjaxListView.as_view(), name='tab_list_zona'),
    path('zona/editar/<int:pk>', ZonaActualizar.as_view(), name='edit_zona'),
    path('zona/listar/delete/<int:pk>', views.zona_eliminar, name='delete_zona'),

    path('base/nuevo/', BaseCrear.as_view(), name='nuevo_base'),
    path('base/listar/', views.base_listar, name='list_base'),
    path('tabla_base/', BaseListarAjaxListView.as_view(), name='tab_list_base'),
    path('base/editar/<int:pk>', BaseActualizar.as_view(), name='edit_base'),
    path('base/listar/delete/<int:pk>', views.base_eliminar, name='delete_base'),

    path('pais/nuevo/', PaisCrear.as_view(), name='nuevo_pais'),
    path('pais/listar/', views.pais_listar, name='list_pais'),
    path('tabla_pais/', PaisListarAjaxListView.as_view(), name='tab_list_pais'),
    path('pais/editar/<int:pk>', PaisActualizar.as_view(), name='edit_pais'),
    path('pais/listar/delete/<int:pk>', views.pais_eliminar, name='delete_pais'),

    path('ciudad/nuevo/', CiudadCrear.as_view(), name='nuevo_ciudad'),
    path('ciudad/listar/', views.ciudad_listar, name='list_ciudad'),
    path('tabla_ciudad/', CiudadListarAjaxListView.as_view(), name='tab_list_ciudad'),
    path('ciudad/editar/<int:pk>', CiudadActualizar.as_view(), name='edit_ciudad'),
    path('ciudad/listar/delete/<int:pk>', views.ciudad_eliminar, name='delete_ciudad'),

    path('sucursal/nuevo/', SucursalCrear.as_view(), name='nuevo_sucursal'),
    path('sucursal/listar/', views.sucursal_listar, name='list_sucursal'),
    path('tabla_sucursal/', SucursalListarAjaxListView.as_view(), name='tab_list_sucursal'),
    path('sucursal/editar/<int:pk>', SucursalActualizar.as_view(), name='edit_sucursal'),
    path('sucursal/listar/delete/<int:pk>', views.sucursal_eliminar, name='delete_sucursal'),

    path('forma_pago/nuevo/', FormaPagoCrear.as_view(), name='nuevo_forma_pago'),
    path('forma_pago/listar/', views.forma_pago_listar, name='list_forma_pago'),
    path('tabla_forma_pago/', FormaPagoListarAjaxListView.as_view(), name='tab_list_forma_pago'),
    path('forma_pago/editar/<int:pk>', FormaPagoActualizar.as_view(), name='edit_forma_pago'),
    path('forma_pago/listar/delete/<int:pk>', views.forma_pago_eliminar, name='delete_forma_pago'),

    path('tipo_vehiculo/nuevo/', TipoVehiculoCrear.as_view(), name='nuevo_tipo_vehiculo'),
    path('tipo_vehiculo/listar/', views.tipo_vehiculo_listar, name='list_tipo_vehiculo'),
    path('tabla_tipo_vehiculo/', TipoVehiculoListarAjaxListView.as_view(), name='tab_list_tipo_vehiculo'),
    path('tipo_vehiculo/editar/<int:pk>', TipoVehiculoActualizar.as_view(), name='edit_tipo_vehiculo'),
    path('tipo_vehiculo/listar/delete/<int:pk>', views.tipoVehiculoEliminar, name='delete_tipo_vehiculo'),

    path('cliente/nuevo/', ClienteCrear.as_view(), name='nuevo_cliente'),
    path('cliente/listar/', views.cliente_listar, name='list_cliente'),
    path('tabla_cliente/', ClienteListarAjaxListView.as_view(), name='tab_list_cliente'),
    path('cliente/editar/<int:pk>', ClienteActualizar.as_view(), name='edit_cliente'),
    path('cliente/listar/delete/<int:pk>', views.cliente_eliminar, name='delete_cliente'),

    path('tipo_servicio/nuevo/', TipoServicioCrear.as_view(), name='nuevo_tipoServicio'),
    path('tipo_servicio/listar/', views.tipo_servicio_listar, name='list_tipoServicio'),
    path('tabla_tipo_servicio/', TipoServicioListarAjaxListView.as_view(), name='tab_list_tipoServicio'),
    path('tipo_servicio/editar/<int:pk>', TipoServicioActualizar.as_view(), name='edit_tipoServicio'),
    path('tipo_servicio/listar/delete/<int:pk>', views.tipoServicio_eliminar, name='delete_tipoServicio'),

    path('marca/nuevo/', MarcaCrear.as_view(), name='nuevo_marca'),
    path('marca/listar/', views.marca_listar, name='list_marca'),
    path('tabla_marca/', MarcaListarAjaxListView.as_view(), name='tab_list_marca'),
    path('marca/editar/<int:pk>', MarcaActualizar.as_view(), name='edit_marca'),
    path('marca/listar/delete/<int:pk>', views.marca_eliminar, name='delete_marca'),

    path('modelo/nuevo/', ModeloCrear.as_view(), name='nuevo_modelo'),
    path('modelo/listar/', views.modelo_listar, name='list_modelo'),
    path('tabla_modelo/', ModeloListarAjaxListView.as_view(), name='tab_list_modelo'),
    path('modelo/editar/<int:pk>', ModeloActualizar.as_view(), name='edit_modelo'),
    path('modelo/listar/delete/<int:pk>', views.modelo_eliminar, name='delete_modelo'),

    path('propietario/nuevo/', PropietarioCrear.as_view(), name='nuevo_propietario'),
    path('propietario/listar/', views.propietario_listar, name='list_propietario'),
    path('tabla_propietario/', PropietarioListarAjaxListView.as_view(), name='tab_list_propietario'),
    path('propietario/editar/<int:pk>', PropietarioActualizar.as_view(), name='edit_propietario'),
    path('propietario/listar/delete/<int:pk>', views.propietario_eliminar, name='delete_propietario'),

    path('vehiculo/nuevo/', VehiculoCrear.as_view(), name='nuevo_vehiculo'),
    path('vehiculo/listar/', views.vehiculo_listar, name='list_vehiculo'),
    path('tabla_vehiculo/', VehiculoListarAjaxListView.as_view(), name='tab_list_vehiculo'),
    path('vehiculo/editar/<int:pk>', VehiculoActualizar.as_view(), name='edit_vehiculo'),
    path('vehiculo/listar/delete/<int:pk>', views.vehiculo_eliminar, name='delete_vehiculo'),

    path('tarifa/nuevo/', TarifaCrear.as_view(), name='nuevo_tarifa'),
    #path('tarifa/nuevo/', views.tarifa_crear, name='nuevo_tarifa'),
    path('tarifa/add/', views.tarifa_add, name='tarifa_add'),
    path('tarifa/listar/', views.tarifa_listar, name='list_tarifa'),
    path('tabla_tarifa/', TarifaListarAjaxListView.as_view(), name='tab_list_tarifa'),
    path('tarifa/editar/<int:pk>', TarifaActualizar.as_view(), name='edit_tarifa'),

    path('horario/<int:pk>/', views.horarios_tarifa, name='horario_tarifa'),
    path('horario/add/', views.agregar_horario, name='agregar_horario'),
    path('horario/edit/<int:pk>', views.editar_horario, name='edit_horario'),
    path('horario/delete/<int:pk>', views.eliminar_horario, name='delete_horario'),

    path('vehiculo_chofer/<int:pk>/', views.vehiculos_chofer, name='vehiculo_chofer'),
    #path('vehiculo_chofer/add/', views.agregar_vehiculo_chofer, name='agregar_vehiculo_chofer'),
    #path('vehiculo_chofer/edit/<int:pk>', views.editar_vehiculo_chofer, name='edit_vehiculo_chofer'),
    #path('vehiculo_chofer/delete/<int:pk>', views.eliminar_vehiculo_chofer, name='delete_vehiculo_chofer'),

    path('comision/nuevo/', ComisionCrear.as_view(), name='nuevo_comision'),
    path('comision/listar/', views.comision_listar, name='list_comision'),
    path('tabla_comision/', ComisionListarAjaxListView.as_view(), name='tab_list_comision'),
    path('comision/editar/<int:pk>', ComisionActualizar.as_view(), name='edit_comision'),
    path('comision/listar/delete/<int:pk>', views.comision_eliminar, name='delete_comision'),

    path('reset/<uidb64>/<token>/', views.reset_confirm, name='reset_confirm'),

    path('vehiculos_activos/', views.vehiculos_activos, name='vehiculos_activos'),
    path('todos_vehiculos/', views.todos_vehiculos, name='todos_vehiculos'),
    path('llamada/', views.llamada, name='llamada'),
    path('mensajes/', views.mensajes, name='mensajes'),
    path('reportes/', views.reportes, name='reportes'),
    path('creditos/', views.creditos, name='creditos'),
    path('menu_configuraciones/', views.configuraciones, name='configuraciones'),
    path('registrar_conductor/', views.registro_conductor, name='registro_conductor'),

    path('servicios_activos/list/', views.list_servicios_activos, name='list_servicios_activos'),
    path('servicios_activos/ajax/list/', ServiciosActivosAjaxList.as_view(), name='list_ajax_servicios_activos'),
    path('servicios_finalizados/list/', views.list_servicios_finalizados, name='list_servicios_finalizados'),
    path('servicios_finalizados/ajax/list/', ServiciosFinalizadosAjaxList.as_view(), name='list_ajax_servicios_finalizados'),

]

