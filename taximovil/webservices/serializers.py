from rest_framework import serializers

from config.models import Usuario, Cliente, Chofer, TipoPago, TipoVehiculo


class TelefonoSerializer(serializers.Serializer):
    telefono = serializers.CharField(help_text="telefono a 10 posiciones sin guiones")


class CodigoSerializer(serializers.Serializer):
    codigo = serializers.CharField(help_text="codigo a validar a 5 digitos")
    telefono = serializers.CharField(help_text="telefono a 10 posiciones sin guiones")

class VerChoferSerializer(serializers.Serializer):
    chofer = serializers.IntegerField()

class ActualizarChoferSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

class ResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Check that servicio exists
        """
        if Usuario.objects.filter(email=value).count() == 0:
            raise serializers.ValidationError("El correo no existe")
        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    googleid = serializers.CharField()
    dispositivo = serializers.CharField()


class LoginChoferSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    placas = serializers.CharField()
    googleid = serializers.CharField()
    dispositivo = serializers.CharField()


class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chofer
        fields = '__all__'

class TipoDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'

class ChoferEstatusSerializer(serializers.Serializer):
    activo = serializers.BooleanField()


class TipoPagoSerializer(serializers.Serializer):
    ciudad = serializers.IntegerField()


class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = ('nombre',)
    # ciudad = serializers.IntegerField()


class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField()
    new = serializers.CharField()


class UsuarioEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('email', 'password', 'nombre', 'a_paterno', 'telefono', 'procedencia', 'googleid')


class CoordenadasSerializer(serializers.Serializer):
    latitud = serializers.FloatField()
    longitud = serializers.FloatField()

    def validate_latitud(self, value):
        """
        Check that servicio exists
        """
        if value < -90 or value > 90:
            raise serializers.ValidationError("La latitud no es valida")
        return value

    def validate_longitud(self, value):
        """
        Check that servicio exists
        """
        if value < -180 or value > 180:
            raise serializers.ValidationError("El servicio no existe")
        return value
