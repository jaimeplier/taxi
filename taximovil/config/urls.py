from django.urls import path

from config.views import UsuarioCrear, UsuarioListarAjaxListView, UsuarioActualizar, EmpresaCrear, \
    EmpresaListarAjaxListView, EmpresaActualizar, ChoferCrear, ChoferListarAjaxListView, ChoferActualizar, SitioCrear, \
    SitioListarAjaxListView, SitioActualizar, ZonaCrear, ZonaListarAjaxListView, ZonaActualizar, BaseCrear, \
    BaseListarAjaxListView, PaisCrear, PaisListarAjaxListView, PaisActualizar, CiudadCrear, CiudadListarAjaxListView, \
    CiudadActualizar, SucursalCrear, SucursalListarAjaxListView, SucursalActualizar, FormaPagoCrear, \
    FormaPagoListarAjaxListView, FormaPagoActualizar
from . import views

app_name = 'config'

urlpatterns = [
    path('', views.index, name='index'),

    path('empresa/nuevo/', EmpresaCrear.as_view(), name='nuevo_empresa'),
    path('empresa/listar/', views.empresaListar, name='list_empresa'),
    path('tabla_empresa/', EmpresaListarAjaxListView.as_view(), name='tab_list_empresa'),
    path('empresa/editar/<int:pk>', EmpresaActualizar.as_view(), name='edit_empresa'),
    path('empresa/listar/delete/<int:pk>', views.empresa_eliminar, name='delete_empresa'),

    path('usuario/nuevo/', UsuarioCrear.as_view(), name='nuevo_usuario'),
    path('usuario/listar/', views.usuarioListar, name='list_usuario'),
    path('tabla_usuario/', UsuarioListarAjaxListView.as_view(), name='tab_list_usuario'),
    path('usuario/editar/<int:pk>', UsuarioActualizar.as_view(), name='edit_usuario'),
    path('usuario/listar/delete/<int:pk>', views.usuario_eliminar, name='delete_usuario'),

    path('chofer/nuevo/', ChoferCrear.as_view(), name='nuevo_chofer'),
    path('chofer/listar/', views.choferListar, name='list_chofer'),
    path('tabla_chofer/', ChoferListarAjaxListView.as_view(), name='tab_list_chofer'),
    path('chofer/editar/<int:pk>', ChoferActualizar.as_view(), name='edit_chofer'),
    path('chofer/listar/delete/<int:pk>', views.chofer_eliminar, name='delete_chofer'),

    path('sitio/nuevo/', SitioCrear.as_view(), name='nuevo_sitio'),
    path('sitio/listar/', views.sitioListar, name='list_sitio'),
    path('tabla_sitio/', SitioListarAjaxListView.as_view(), name='tab_list_sitio'),
    path('sitio/editar/<int:pk>', SitioActualizar.as_view(), name='edit_sitio'),
    path('sitio/listar/delete/<int:pk>', views.sitio_eliminar, name='delete_sitio'),

    path('zona/nuevo/', ZonaCrear.as_view(), name='nuevo_zona'),
    path('zona/listar/', views.zonaListar, name='list_zona'),
    path('tabla_zona/', ZonaListarAjaxListView.as_view(), name='tab_list_zona'),
    path('zona/editar/<int:pk>', ZonaActualizar.as_view(), name='edit_zona'),
    path('zona/listar/delete/<int:pk>', views.zona_eliminar, name='delete_zona'),

    path('base/nuevo/', BaseCrear.as_view(), name='nuevo_base'),
    path('base/listar/', views.baseListar, name='list_base'),
    path('tabla_base/', BaseListarAjaxListView.as_view(), name='tab_list_base'),

    path('pais/nuevo/', PaisCrear.as_view(), name='nuevo_pais'),
    path('pais/listar/', views.paisListar, name='list_pais'),
    path('tabla_pais/', PaisListarAjaxListView.as_view(), name='tab_list_pais'),
    path('pais/editar/<int:pk>', PaisActualizar.as_view(), name='edit_pais'),
    path('pais/listar/delete/<int:pk>', views.pais_eliminar, name='delete_pais'),

    path('ciudad/nuevo/', CiudadCrear.as_view(), name='nuevo_ciudad'),
    path('ciudad/listar/', views.ciudadListar, name='list_ciudad'),
    path('tabla_ciudad/', CiudadListarAjaxListView.as_view(), name='tab_list_ciudad'),
    path('ciudad/editar/<int:pk>', CiudadActualizar.as_view(), name='edit_ciudad'),
    path('ciudad/listar/delete/<int:pk>', views.ciudad_eliminar, name='delete_ciudad'),

    path('sucursal/nuevo/', SucursalCrear.as_view(), name='nuevo_sucursal'),
    path('sucursal/listar/', views.sucursalListar, name='list_sucursal'),
    path('tabla_sucursal/', SucursalListarAjaxListView.as_view(), name='tab_list_sucursal'),
    path('sucursal/editar/<int:pk>', SucursalActualizar.as_view(), name='edit_sucursal'),
    path('sucursal/listar/delete/<int:pk>', views.sucursal_eliminar, name='delete_sucursal'),

    path('forma_pago/nuevo/', FormaPagoCrear.as_view(), name='nuevo_forma_pago'),
    path('forma_pago/listar/', views.formaPagoListar, name='list_forma_pago'),
    path('tabla_forma_pago/', FormaPagoListarAjaxListView.as_view(), name='tab_list_forma_pago'),
    path('forma_pago/editar/<int:pk>', FormaPagoActualizar.as_view(), name='edit_forma_pago'),
    path('forma_pago/listar/delete/<int:pk>', views.forma_pago_eliminar, name='delete_forma_pago'),

]
