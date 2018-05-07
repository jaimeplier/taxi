from rest_framework import serializers

from config.models import Cliente, Tarjeta, DireccionServicio, Ciudad


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


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DireccionServicio
        fields = ('id', 'direccion', 'nombre', 'latitud', 'longitud', 'estatus')


class DireccionEditSerializer(serializers.ModelSerializer):
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()

    class Meta:
        model = DireccionServicio
        fields = ('id', 'direccion', 'nombre', 'latitud', 'longitud', 'estatus')


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = '__all__'
