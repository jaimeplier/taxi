from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from config.models import Ciudad
from webservices.serializers import CatalogoSerializer


class ListCiudad(ListAPIView):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )
    serializer_class = CatalogoSerializer

    def get_queryset(self):
        queryset = Ciudad.objects.all()
        return queryset