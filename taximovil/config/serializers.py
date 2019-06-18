from rest_framework import serializers

from config.models import Cliente, Tarjeta, DireccionServicio, Ciudad, TipoPago, TipoVehiculo, Tarifa, Servicio, Chofer, \
    EstatusServicio, TipoServicio, Empresa, Sucursal, Vehiculo


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


class ChoferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chofer
        fields = '__all__'


class CiudadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciudad
        fields = ('id', 'nombre', 'estatus', 'factor_tiempo', 'radio', 'pais', 'centro')


class EstatusServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstatusServicio
        fields = '__all__'


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class TipoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPago
        fields = '__all__'


class TipoVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoVehiculo
        fields = '__all__'


class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = '__all__'


class TarifaSerializer(serializers.ModelSerializer):
    tipo_vehiculo = TipoVehiculoSerializer(read_only=True, many=False)

    class Meta:
        model = Tarifa
        fields = '__all__'


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'


class SucursalSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer(read_only=True, many=False)

    class Meta:
        model = Sucursal
        fields = '__all__'


class ServicioSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True, many=False)
    chofer = ChoferSerializer(read_only=True, many=False)
    vehiculo = VehiculoSerializer(read_only=True, many=False)
    estatus = EstatusServicioSerializer(read_only=True, many=False)
    tipo_servicio = TipoServicioSerializer(read_only=True, many=False)
    sucursal = SucursalSerializer(read_only=True, many=False)
    tarifa = TarifaSerializer(read_only=True, many=False)
    tipo_pago = TipoPagoSerializer(read_only=True, many=False)

    class Meta:
        model = Servicio
        fields = (
            'pk', 'hora_registro', 'hora_servicio', 'origen', 'destino', 'direccion_origen', 'direccion_destino',
            'ref_lugar', 'ref_persona', 'distancia', 'tiempo_aproximado_servicio', 'tiempo_aproximado_taxi', 'duracion',
            'costo', 'estatus', 'cliente', 'chofer', 'tipo_servicio', 'vehiculo', 'sitio', 'sucursal', 'tipo_pago',
            'tarifa')


class AsignarVehiculoSerializer(serializers.Serializer):
    vehiculo = serializers.IntegerField()
    chofer = serializers.IntegerField()