from django.urls import path, include
from rest_framework import routers

from webservices.views import EnviarCodigo

app_name = 'webservices'

router = routers.DefaultRouter()

urlpatterns = [
    # Router urls
    path('', include(router.urls)),
    # Auth urls
    path('enviarCodigo/', EnviarCodigo.as_view(), name='enviar_codigo'),
]
