from __future__ import unicode_literals

from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.contrib.gis.db import models


# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password, rol, nombre, a_paterno, telefono):
        if not email:
            raise ValueError('El usuario necesita un email')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.rol = rol
        user.nombre = nombre
        user.a_paterno = a_paterno
        user.telefono = telefono
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, rol, nombre, a_paterno, telefono):
        user = self.create_user(email=email, password=password, rol=Rol(pk=1), nombre=nombre, a_paterno=a_paterno,
                                telefono=telefono)
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=128)
    password = models.CharField(max_length=512)
    rol = models.ForeignKey('Rol', models.DO_NOTHING)
    nombre = models.CharField(max_length=64)
    a_paterno = models.CharField(max_length=64)
    a_materno = models.CharField(max_length=64, null=True, blank=True)
    telefono = models.CharField(max_length=20, unique=True)
    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'rol', 'nombre', 'a_paterno', 'telefono']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True
        p = perm.split('.')
        if len(p) > 1:
            per = self.rol.permisos.filter(codename=p[1]).count()
        else:
            per = self.rol.permisos.filter(codename=p[0]).count()
        if per > 0:
            return True
        return False

    def has_perms(self, perm, obj=None):
        # Este válida
        if self.is_superuser:
            return True
        for p in perm:
            pr = p.split('.')
            if len(pr) > 1:
                per = self.rol.permisos.filter(codename=pr[1]).count()
            else:
                per = self.rol.permisos.filter(codename=pr[0]).count()
            if per == 0:
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True
        if self.is_staff:
            return True
        if self.rol.permisos.filter(codename=app_label).count() > 0:
            return True
        return False

    @property
    def is_staff(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_superuser(self):
        if self.rol.pk == 1:
            return True
        else:
            return False

    @property
    def is_active(self):
        return self.estatus

    def get_full_name(self):
        return str(self.nombre) + ' ' + str(self.a_paterno) + ' ' + str(self.a_materno)

    def get_personalize_name(self):
        name = self.persona.nombre
        if self.persona.a_paterno is not None:
            name = name + ' ' + self.persona.a_paterno
        return name

    def get_short_name(self):
        return self.email

    class Meta:
        managed = True
        db_table = 'usuario'


class Cliente(Usuario):
    rfc = models.CharField(max_length=45, blank=True, null=True)
    cp = models.IntegerField(blank=True, null=True)
    lada = models.IntegerField(blank=True, null=True)
    procedencia = models.CharField(max_length=45, blank=True, null=True)
    customer_id = models.CharField(max_length=45, blank=True, null=True)
    googleid = models.CharField(max_length=128, blank=True, null=True)

    # customer_token = models.CharField(blank=True, null=True, max_length=512)

    def get_full_name(self):
        return str(self.nombre) + ' ' + str(self.a_paterno) + ' ' + str(self.a_materno)

    class Meta:
        managed = True
        db_table = 'cliente'


class Chofer(Usuario):
    foto = models.FileField(db_column='foto', upload_to='asociados/', null=True)
    numero_licencia = models.CharField(max_length=64)
    turno = models.CharField(max_length=3)
    saldo = models.FloatField()
    direccion = models.ForeignKey('Direccion', models.DO_NOTHING)

    # estatusChofer
    # cuenta (historial)
    # documentos
    # taxi = models.ManyToMany('Taxi', models.DO_NOTHING)

    def get_full_name(self):
        return str(self.nombre) + ' ' + str(self.a_paterno) + ' ' + str(self.a_materno)

    class Meta:
        managed = True
        db_table = 'chofer'


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'empresa'


class Personal(Usuario):
    class Meta:
        managed = True
        db_table = 'persona'


class Sitio(models.Model):
    nombre = models.CharField(max_length=50)
    num_espacio = models.IntegerField()
    pv = models.CharField(max_length=45)
    # estatus_permiso
    estatus_sesion = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'sitio'

    def __str__(self):
        return self.nombre


class BitacoraEstatusServicio(models.Model):
    estatus = models.ForeignKey('EstatusServicio', on_delete=models.DO_NOTHING)
    # servicio = models.ForeignKey('Servicio', on_delete=models.DO_NOTHING)
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'bitacora_estatus_servicio'


class Codigo(models.Model):
    codigo = models.CharField(max_length=5)
    telefono = models.CharField(max_length=10)
    fecha = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'codigo'


class Dia(Enum):
    Domingo = 7
    Lunes = 1
    Martes = 2
    Miercoles = 3
    Jueves = 4
    Viernes = 5
    Sabado = 6


class EstatusPago(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'estatus_pago'


class EstatusServicio(models.Model):
    nombre = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'estatus_servicio'


class Horario(models.Model):
    diasemana = models.IntegerField()
    horainicio = models.TimeField()
    horafin = models.TimeField()
    tarifa = models.ForeignKey('Tarifa', models.DO_NOTHING)

    def get_dia(self):
        return Dia(self.diasemana).name

    class Meta:
        managed = True
        db_table = 'horario'


class Comisiones(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.IntegerField()
    factor = models.FloatField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'comisiones'


class Pais(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'pais'


class Rol(models.Model):
    nombre = models.CharField(max_length=64)
    permisos = models.ManyToManyField(Permission, through='RolHasPermissions')

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'rol'


class RolHasPermissions(models.Model):
    rol = models.ForeignKey(Rol, models.DO_NOTHING)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'rol_has_permissions'


class ServicioChofer(models.Model):
    chofer = models.ForeignKey(Chofer, models.DO_NOTHING, blank=True, null=True)
    # servicio = models.ForeignKey(Servicio, models.DO_NOTHING)
    estatus = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'servicio_asociado'


class TipoMateria(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'tipo_materia'


class TipoPago(models.Model):
    nombre = models.CharField(max_length=45)
    precio = models.FloatField()
    plan = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'tipo_pago'


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'tipo_servicio'


class Direccion(models.Model):
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    numero_interior = models.CharField(max_length=20, null=True, blank=True)
    numero_exterior = models.CharField(max_length=50)
    cp = models.CharField(max_length=10)

    latlgn = models.PointField()
    municipio = models.ForeignKey('Municipio', models.DO_NOTHING)

    def get_address(self):
        return 'Calle: ' + str(self.calle) + ' Num ext: ' + str(self.numero_exterior) + ' Col: ' + str(
            self.colonia) + ' Municipio: ' + str(self.municipio)

    @property
    def latitud(self):
        """I'm the 'x' property."""
        return str(self.latlgn.coords[1])

    @property
    def longitud(self):
        """I'm the 'x' property."""
        return str(self.latlgn.coords[0])

    class Meta:
        managed = True
        db_table = 'direccion'


class Estado(models.Model):
    nombre = models.CharField(max_length=45)
    hora_diferencia = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'estado'


class Municipio(models.Model):
    nombre = models.CharField(max_length=45)
    estado = models.ForeignKey('Estado', models.DO_NOTHING)  # Field name made lowercase.

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'municipio'


class Vehiculo(models.Model):
    placa = models.CharField(max_length=45, unique=True)
    anio = models.IntegerField()
    cromatica = models.CharField(max_length=45)
    # seguro

    estatus = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    modelo = models.ForeignKey('Modelo', models.DO_NOTHING)
    propietario = models.ForeignKey('Propietario', models.DO_NOTHING)
    economico = models.CharField(max_length=15, unique=True)
    ciudad = models.ForeignKey('Ciudad', models.DO_NOTHING)
    activo = models.BooleanField(default=True)

    class Meta:
        managed = True
        db_table = 'vehiculo'


class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=45, unique=True)
    caracteristicas = models.CharField(max_length=200)
    num_max_pasajeros = models.IntegerField()
    num_maletas = models.IntegerField()

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'tipo_vehiculo'


class Base(models.Model):
    identificador = models.CharField(max_length=15)
    numero_espacio = models.IntegerField()
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE, )
    telefono = models.CharField(max_length=25, unique=True)

    # horario = models.ManyToManyField('Horario', models.DO_NOTHING)
    sitio = models.ForeignKey('Sitio', models.DO_NOTHING)

    # puerta = models.ManyToOneRel('Puerta', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'base'

    def __str__(self):
        return self.identificador


class Puerta(models.Model):
    nombre = models.CharField(max_length=45)
    comentarios = models.CharField(max_length=150)

    class Meta:
        managed = True
        db_table = 'puerta'


class Sucursal(models.Model):
    clave = models.CharField(max_length=50)
    nombre = models.CharField(max_length=200)
    coordenadas = models.PointField()
    direccion = models.CharField(max_length=200)
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    empresa = models.ForeignKey('Empresa', models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    @property
    def latitud(self):
        """I'm the 'x' property."""
        if self.coordenadas is None:
            return None
        return str(self.coordenadas.coords[1])

    @property
    def longitud(self):
        """I'm the 'x' property."""
        if self.coordenadas is None:
            return None
        return str(self.coordenadas.coords[0])

    class Meta:
        managed = True
        db_table = 'sucursal'


class Zona(models.Model):
    nombre = models.CharField(max_length=45)
    centro = models.PointField()
    radio = models.FloatField()

    def __str__(self):
        return self.nombre

    @property
    def latitud(self):
        """I'm the 'x' property."""
        if self.centro is None:
            return None
        return str(self.centro.coords[1])

    @property
    def longitud(self):
        """I'm the 'x' property."""
        if self.centro is None:
            return None
        return str(self.centro.coords[0])

    class Meta:
        managed = True
        db_table = 'zona'


class Tarifa(models.Model):
    tarifa_base = models.FloatField()
    costo_minimo = models.FloatField()
    costo_km = models.FloatField()
    distancia_max = models.FloatField()
    incremento_distancia = models.FloatField()
    costo_minuto = models.FloatField()
    comision = models.FloatField()

    ciudad = models.ForeignKey('Ciudad', models.DO_NOTHING)
    pais = models.ForeignKey('Pais', models.DO_NOTHING)
    empresa = models.ForeignKey('Empresa', models.DO_NOTHING)
    sucursal = models.ForeignKey('Sucursal', models.DO_NOTHING)
    zona_origen = models.ForeignKey('Zona', models.DO_NOTHING, related_name='zona_origen')
    zona_destino = models.ForeignKey('Zona', models.DO_NOTHING, related_name='zona_destino')
    sitio = models.ForeignKey('Sitio', models.DO_NOTHING)
    base = models.ForeignKey('Base', models.DO_NOTHING)
    pago = models.ManyToManyField('TipoPago')
    tipo_vehiculo = models.ForeignKey('TipoVehiculo', models.DO_NOTHING)
    tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING)
    comisiones = models.ManyToManyField('Comisiones')

    class Meta:
        managed = True
        db_table = 'tarifa'


class Ciudad(models.Model):
    nombre = models.CharField(max_length=45)
    estatus = models.BooleanField(default=True)
    factor_tiempo = models.FloatField()
    centro = models.PointField()
    radio = models.IntegerField()
    pais = models.ForeignKey('Pais', models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    @property
    def latitud(self):
        """I'm the 'x' property."""
        if self.centro is None:
            return None
        return str(self.centro.coords[1])

    @property
    def longitud(self):
        """I'm the 'x' property."""
        if self.centro is None:
            return None
        return str(self.centro.coords[0])

    class Meta:
        managed = True
        db_table = 'ciudad'


class Cuentas(models.Model):
    cie = models.CharField(max_length=7)
    clabe = models.CharField(max_length=18)

    # chofer = models.ManyToOneRel('Cuentas', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'cuentas'


class Documentos(models.Model):
    licencia_condicir = models.CharField(max_length=200)
    licencia_auto = models.CharField(max_length=200)
    seguro_auto = models.CharField(max_length=200)
    tarjeta_circulacion = models.CharField(max_length=200)
    placas = models.CharField(max_length=200, unique=True)
    verificacion = models.CharField(max_length=200)
    penales = models.CharField(max_length=200)
    toxicologico = models.CharField(max_length=200)
    chofer = models.OneToOneField('Chofer', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'documentos'


class Servicio(models.Model):
    hora_registro = models.DateTimeField(auto_now_add=True)
    ubicacion_usuario = models.PointField()
    destino = models.PointField()
    direccion_servicio = models.CharField(max_length=400)
    direccion_destino = models.CharField(max_length=400)
    tiempo_aproximado = models.CharField(max_length=20)
    ref_lugar = models.CharField(max_length=200)
    ref_persona = models.CharField(max_length=200)
    distancia = models.CharField(max_length=20)
    costo = models.CharField(max_length=20)
    estatus = models.IntegerField()

    cliente = models.ForeignKey('Cliente', models.DO_NOTHING)
    tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING)
    vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING)
    sitio = models.ForeignKey('Sitio', models.DO_NOTHING)

    forma_pago = models.ForeignKey(TipoPago, models.DO_NOTHING)
    tarifa = models.ForeignKey('Tarifa', models.DO_NOTHING)

    @property
    def latitudUsuario(self):
        """I'm the 'x' property."""
        if self.ubicacion_usuario is None:
            return None
        return str(self.ubicacion_usuario.coords[1])

    @property
    def longitudUsuario(self):
        """I'm the 'x' property."""
        if self.ubicacion_usuario is None:
            return None
        return str(self.ubicacion_usuario.coords[0])

    @property
    def latitudDestino(self):
        """I'm the 'x' property."""
        if self.destino is None:
            return None
        return str(self.destino.coords[1])

    @property
    def longitudDestino(self):
        """I'm the 'x' property."""
        if self.destino is None:
            return None
        return str(self.destino.coords[0])

    class Meta:
        managed = True
        db_table = 'servicio'


class Marca(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'marca'


class Modelo(models.Model):
    nombre = models.CharField(max_length=45)
    marca = models.ForeignKey('Marca', models.DO_NOTHING)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'modelo'


class Propietario(Usuario):
    tipo_persona = models.CharField(max_length=45)
    razon_social = models.CharField(max_length=45)
    direccion_fiscal = models.CharField(max_length=45)
    nombre_banco = models.CharField(max_length=45)
    titular_cuenta = models.CharField(max_length=45)
    clabe = models.CharField(max_length=45)
    numero_cuenta = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'propietario'


class Tarjeta(models.Model):
    ultiimos_digitos = models.CharField(max_length=5)
    token = models.CharField(max_length=64)
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING)
    nombre = models.CharField(max_length=128)
    nombre_propietario = models.CharField(max_length=256)

    class Meta:
        managed = True
        db_table = 'trajeta'
