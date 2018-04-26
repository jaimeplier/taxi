from django.urls import path, include
from rest_framework import routers

from webservices.cliente import RegistrarUsuario
from webservices.views import EnviarCodigo, VerificaCodigo, LoginChofer

app_name = 'webservices'

router = routers.DefaultRouter()

urlpatterns = [
    # Router urls
    path('', include(router.urls)),
    # Auth urls
    path('enviarCodigo/', EnviarCodigo.as_view(), name='enviar_codigo'),
    path('verificarCodigo/', VerificaCodigo.as_view(), name='verifica_codigo'),
    path('registrar/', RegistrarUsuario.as_view(), name='registrar'),
    path('loginChofer/', LoginChofer.as_view(), name='login_chofer'),
]
