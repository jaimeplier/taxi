from django.urls import path

from admin_ciudad.views import SitioCrear, SitioListarAjaxListView, SitioActualizar, AdministradorSitioCrear, AdministradorSitioListarAjaxListView, AdministradorSitioActualizar
from admin_ciudad import views

app_name = 'admin_ciudad'

urlpatterns = [

    path('sitio/nuevo/', SitioCrear.as_view(), name='nuevo_sitio'),
    path('sitio/listar/', views.sitio_listar, name='list_sitio'),
    path('tabla_sitio/', SitioListarAjaxListView.as_view(), name='tab_list_sitio'),
    path('sitio/editar/<int:pk>', SitioActualizar.as_view(), name='edit_sitio'),
    path('sitio/listar/delete/<int:pk>', views.sitio_eliminar, name='delete_sitio'),

    path('admin_sitio/nuevo/<int:sitio>', AdministradorSitioCrear.as_view(), name='nuevo_admin_sitio'),
    path('admin_sitio/listar/<int:sitio>', views.admin_sitio_listar, name='list_admin_sitio'),
    path('tabla_admin_sitio/<int:sitio>', AdministradorSitioListarAjaxListView.as_view(), name='tab_list_admin_sitio'),
    path('admin_sitio/editar/<int:pk>/<int:sitio>', AdministradorSitioActualizar.as_view(), name='edit_admin_sitio')
]