from django.contrib import admin
from config.models import Chofer, Empresa, Personal, Sitio, Comisiones, Pais, TipoPago, TipoServicio, Estado, Municipio, \
    Vehiculo, TipoVehiculo, Base, Puerta, Sucursal, Zona, Tarifa, Ciudad, Documentos, Marca, Modelo, Propietario, \
    Tarjeta, Usuario

# Register your models here.
admin.site.register(Usuario)
admin.site.register(Chofer)
admin.site.register(Empresa)
admin.site.register(Personal)
admin.site.register(Sitio)
admin.site.register(Comisiones)
admin.site.register(Pais)
admin.site.register(TipoPago)
admin.site.register(TipoServicio)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Vehiculo)
admin.site.register(TipoVehiculo)
admin.site.register(Base)
admin.site.register(Puerta)
admin.site.register(Sucursal)
admin.site.register(Zona)
admin.site.register(Tarifa)
admin.site.register(Ciudad)
admin.site.register(Documentos)
admin.site.register(Marca)
admin.site.register(Modelo)
admin.site.register(Propietario)
admin.site.register(Tarjeta)