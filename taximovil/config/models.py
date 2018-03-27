from __future__ import unicode_literals

from enum import Enum

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Permission
from django.contrib.gis.db import models


# Create your models here.
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password, rol, nombre, a_paterno):
        if not email:
            raise ValueError('El usuario necesita un email')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.rol = rol
        user.nombre = nombre
        user.a_paterno = a_paterno
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, rol, nombre, a_paterno):
        user = self.create_user(email=email, password=password, rol=Rol(pk=1), nombre=nombre, a_paterno=a_paterno)
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
    customer_token = models.CharField(blank=True, null=True)

    def get_full_name(self):
        return str(self.nombre) + ' ' + str(self.a_paterno) + ' ' + str(self.a_materno)

    class Meta:
        managed = True
        db_table = 'cliente'


class Chofer(Usuario):

    def get_full_name(self):
        return str(self.nombre) + ' ' + str(self.a_paterno) + ' ' + str(self.a_materno)

    class Meta:
        managed = True
        db_table = 'chofer'


class Empresa(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'empresa'


class Personal(Usuario):

    class Meta:
        managed = True
        db_table = 'persona'


class Sitio(models.Model):
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'sitio'


class BitacoraEstatusServicio(models.Model):
    estatus = models.ForeignKey('EstatusServicio', on_delete=models.DO_NOTHING)
    servicio = models.ForeignKey('Servicio', on_delete=models.DO_NOTHING)
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
    tarifa = models.ForeignKey

    def get_dia(self):
        return Dia(self.diasemana).name

    class Meta:
        managed = True
        db_table = 'horario'


class Idioma(models.Model):
    nombre = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'idioma'


class Estado(models.Model):
    nombre = models.CharField(max_length=45)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = True
        db_table = 'estado'


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
    #servicio = models.ForeignKey(Servicio, models.DO_NOTHING)
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
