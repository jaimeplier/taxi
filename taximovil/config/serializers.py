from rest_framework import serializers

from config.models import Cliente, Tarjeta


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'email', 'password', 'nombre', 'a_paterno', 'telefono', 'procedencia', 'googleid')


class TarjetaEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = ('id', 'nombre', 'ultiimos_digitos', 'token', 'nombre_propietario')


class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = ('id', 'nombre', 'ultiimos_digitos', 'nombre_propietario')
