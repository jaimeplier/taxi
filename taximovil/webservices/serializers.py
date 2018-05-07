from rest_framework import serializers

from config.models import Usuario, Cliente, Chofer, Ciudad, TipoPago, TipoVehiculo


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


class ChoferEstatusSerializer(serializers.Serializer):
    activo = serializers.BooleanField()


class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = ('nombre',)

class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = ('nombre',)
    #ciudad = serializers.IntegerField()


class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField()
    new = serializers.CharField()


class UsuarioEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('email', 'password', 'nombre', 'a_paterno', 'telefono', 'procedencia', 'googleid')
