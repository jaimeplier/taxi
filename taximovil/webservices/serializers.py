from rest_framework import serializers

from config.models import Usuario, Cliente, TipoPago, Servicio, Chofer


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


class TipoDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'


class ChoferEstatusSerializer(serializers.Serializer):
    activo = serializers.BooleanField()


class ServicioEstatusSerializer(serializers.Serializer):
    servicio = serializers.IntegerField()
    estatus = serializers.IntegerField()


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


class RutaSerializer(serializers.Serializer):
    servicio = serializers.IntegerField()
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


class CotizarSerializer(serializers.Serializer):
    fecha = serializers.DateTimeField()
    ciudad = serializers.IntegerField()
    tipo_vehiculo = serializers.IntegerField()
    tipo_servicio = serializers.IntegerField()
    sucursal = serializers.IntegerField(allow_null=True, required=False)
    base = serializers.IntegerField(allow_null=True, required=False)
    lat_origen = serializers.FloatField()
    lon_origen = serializers.FloatField()
    lat_destino = serializers.FloatField()
    lon_destino = serializers.FloatField()

    def validate_lat_origen(self, value):
        """
        Check that servicio exists
        """
        if value < -90 or value > 90:
            raise serializers.ValidationError("La latitud no es valida")
        return value

    def validate_lon_origen(self, value):
        """
        Check that servicio exists
        """
        if value < -180 or value > 180:
            raise serializers.ValidationError("El servicio no existe")
        return value

    def validate_lat_destino(self, value):
        """
        Check that servicio exists
        """
        if value < -90 or value > 90:
            raise serializers.ValidationError("La latitud no es valida")
        return value

    def validate_lon_destino(self, value):
        """
        Check that servicio exists
        """
        if value < -180 or value > 180:
            raise serializers.ValidationError("El servicio no existe")
        return value


class SolicitarServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = (
            'hora_servicio', 'origen', 'destino', 'direccion_origen', 'direccion_destino', 'ref_lugar', 'ref_persona',
            'distancia', 'tiempo_aproximado_servicio', 'costo', 'tipo_servicio', 'sitio', 'tipo_pago', 'tarifa',
            'tarjeta')


class ServicioPkSerializer(serializers.Serializer):
    servicio = serializers.IntegerField()

    def validate_servicio(self, value):
        """
        Check that servicio exists
        """
        if Servicio.objects.filter(pk=value).count() == 0:
            raise serializers.ValidationError("El servicio no existe")
        return value


class ChoferCoordenadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chofer
        fields = ('latlgn',)


class ChoferCreditoSerializer(serializers.Serializer):
    chofer = serializers.IntegerField()
    monto = serializers.FloatField()

    def validate_chofer(self, value):
        """
        Check that chofer exists
        """
        try:
            Chofer.objects.get(pk=value)
            return value
        except:
            raise serializers.ValidationError("El chofer no existe")


class CalificacionSerializer(serializers.Serializer):
    calificacion = serializers.IntegerField()
    servicio = serializers.IntegerField()

    def validate_servicio(self, value):
        """
        Check that servicio exists
        """
        if Servicio.objects.filter(pk=value).count() == 0:
            raise serializers.ValidationError("El servicio no existe")
        return value


class UltimasDireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicio
        fields = ('latitudDestino', 'longitudDestino', 'direccion_destino')


class EditNombreSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=64)
    a_paterno = serializers.CharField(max_length=64)
    a_materno = serializers.CharField(max_length=64)


class AgregarSaldoSerializer(serializers.Serializer):
    monto = serializers.FloatField()
    tipo_pago = serializers.IntegerField()
