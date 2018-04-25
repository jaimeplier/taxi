from rest_framework import serializers

from config.models import Usuario


class TelefonoSerializer(serializers.Serializer):
    telefono = serializers.CharField(help_text="telefono a 10 posiciones sin guiones")


class CodigoSerializer(serializers.Serializer):
    codigo = serializers.CharField(help_text="codigo a validar a 5 digitos")
    telefono = serializers.CharField(help_text="telefono a 10 posiciones sin guiones")


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


class ChoferEstatusSerializer(serializers.Serializer):
    activo = serializers.BooleanField()


class ChangePasswordSerializer(serializers.Serializer):
    old = serializers.CharField()
    new = serializers.CharField()

