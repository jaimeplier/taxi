from django.urls import path

from admin_softic import views
from admin_softic.views import AdministradorCiudadCrear, AdministradorCiudadListarAjaxListView, \
    AdministradorCiudadActualizar

app_name = 'admin_softic'
urlpatterns = [

    path('administrador_ciudad/nuevo/', AdministradorCiudadCrear.as_view(), name='nuevo_administrador_ciudad'),
    path('administrador_ciudad/listar/', views.administrador_ciudad_listar, name='list_administrador_ciudad'),
    path('tabla_administrador_ciudad/', AdministradorCiudadListarAjaxListView.as_view(),
         name='tab_list_administrador_ciudad'),
    path('administrador_ciudad/editar/<int:pk>', AdministradorCiudadActualizar.as_view(),
         name='edit_administrador_ciudad'),

]

