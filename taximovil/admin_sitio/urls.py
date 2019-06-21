from django.urls import path

from admin_sitio import views
from admin_sitio.views import TarifaCrear, TarifaListarAjaxListView, TarifaActualizar, CallcenterCrear, \
    CallcenterListarAjaxListView, CallcenterActualizar

app_name = 'admin_sitio'
urlpatterns = [

    path('callcenter/nuevo/', CallcenterCrear.as_view(), name='nuevo_callcenter'),
    path('callcenter/listar/', views.callcenter_listar, name='list_callcenter'),
    path('tabla_callcenter/', CallcenterListarAjaxListView.as_view(), name='tab_list_callcenter'),
    path('callcenter/editar/<int:pk>', CallcenterActualizar.as_view(), name='edit_callcenter'),
    path('callcenter/listar/delete/<int:pk>', views.callcenter_eliminar, name='delete_callcenter'),

    path('tarifa/nuevo/', TarifaCrear.as_view(), name='nuevo_tarifa'),
    path('tarifa/add/', views.tarifa_add, name='tarifa_add'),
    path('tarifa/listar/', views.tarifa_listar, name='list_tarifa'),
    path('tabla_tarifa/', TarifaListarAjaxListView.as_view(), name='tab_list_tarifa'),
    path('tarifa/editar/<int:pk>', TarifaActualizar.as_view(), name='edit_tarifa'),
]