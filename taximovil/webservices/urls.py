from django.urls import path, include
from rest_framework import routers

from webservices import tarjeta, cliente
from webservices.cliente import RegistrarUsuario
from webservices.views import EnviarCodigo, VerificaCodigo, LoginUsuario, ChangePassword, ResetPassword
from webservices.views import EnviarCodigo, VerificaCodigo, LoginChofer

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
    path('modificarPassword', ChangePassword.as_view(), name='modficarPassword'),
    path('resetPassword/', ResetPassword.as_view(), name='reset_password'),
    path('loginChofer/', LoginChofer.as_view(), name='login_chofer'),
]
