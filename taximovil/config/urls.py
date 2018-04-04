from django.urls import path

from config.views import UsuarioCrear, UsuarioListarAjaxListView, UsuarioActualizar, EmpresaCrear, \
    EmpresaListarAjaxListView, EmpresaActualizar, ChoferCrear, ChoferListarAjaxListView, ChoferActualizar
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


]
