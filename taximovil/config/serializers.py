from rest_framework import serializers

from config.models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'email', 'password', 'nombre', 'a_paterno', 'telefono', 'procedencia', 'googleid')
