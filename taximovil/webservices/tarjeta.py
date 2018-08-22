import conekta
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from config.models import Tarjeta, Cliente
from config.serializers import TarjetaSerializer, TarjetaEditSerializer
from taximovil.settings import CONEKTA_PRIVATE_KEY, CONEKTA_LOCALE, CONEKTA_VERSION


class TarjetaViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Tarjeta.objects.all()

    def list(self, request):
        try:
            cliente = Cliente.objects.get(pk=self.request.user.pk)
        except Cliente.DoesNotExist:
            return Response({"error": "El cliente no existe"}, status=status.HTTP_400_BAD_REQUEST)
        qs = Tarjeta.objects.filter(usuario=self.request.user)
        serializer = TarjetaSerializer(qs, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        usuario = self.request.user
        serializer = TarjetaEditSerializer(data=self.request.data)
        if serializer.is_valid():
            conekta.api_key = CONEKTA_PRIVATE_KEY
            conekta.locale = CONEKTA_LOCALE
            conekta.api_version = CONEKTA_VERSION
            if usuario.customer_id is None:
                try:
                    custom = conekta.Customer.create({
                        "name": serializer.validated_data.get('nombre_propietario'),
                        "email": usuario.email,
                        "phone": usuario.telefono
                    })
                except conekta.ConektaError as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                usuario.customer_id = custom.id
                usuario.save()
            else:
                custom = conekta.Customer.find(usuario.customer_id)
            source = custom.createPaymentSource({
                "type": "card",
                "token_id": serializer.validated_data.get('token')
            })
            print(source.id)
            serializer.save(usuario=self.request.user, token=source.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.request is None or self.request.method == 'POST':
            return TarjetaEditSerializer
        else:
            return TarjetaSerializer
