from django.forms import ModelForm, CharField, EmailField, NumberInput, PasswordInput, CheckboxSelectMultiple, forms, Select
from config.models import Empresa, Usuario, Chofer, Sitio, Zona, Base, Direccion, Pais, Ciudad, Sucursal, TipoPago, \
    TipoVehiculo


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre',
                  'direccion',
                  ]
        labels = {'nombre': 'Nombre',
                  'direccion': 'Direccion',
                  }


class UsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }


class ChoferForm(ModelForm):
    class Meta:
        model = Chofer
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }


class SitioForm(ModelForm):
    class Meta:
        model = Sitio
        fields = ['nombre',
                  'num_espacio',
                  'pv',
                  ]
        labels = {'nombre': 'Nombre',
                  'num_espacio': 'Cantidad de espacios'
                  }


class ZonaForm(ModelForm):
    class Meta:
        model = Zona
        fields = ['nombre',
                  'radio',
                  ]

class BaseForm(ModelForm):
    class Meta:
        model = Base
        fields = ['identificador',
                  'numero_espacio',
                  'telefono',
                  'sitio',
        ]

class DireccionForm(ModelForm):
    class Meta:
        model = Direccion
        fields = ['colonia',
                  'calle',
                  'numero_interior',
                  'numero_exterior',
                  'cp',
                  'municipio',
                  ]

class PaisForm(ModelForm):
    class Meta:
        model = Pais
        fields = ['nombre',
                  ]

class CiudadForm(ModelForm):
    class Meta:
        model = Ciudad
        fields = ['nombre',
                  'factor_tiempo',
                  'radio',
                  'pais',
                  ]

class SucursalForm(ModelForm):
    class Meta:
        model = Sucursal
        fields = ['nombre',
                  'clave',
                  'direccion',
                  'usuario',
                  'empresa',
                  ]

class TipoPagoForm(ModelForm):
    class Meta:
        model = TipoPago
        fields = ['nombre',
                  'precio',
                  'plan',
                  ]

class TipoVehiculoForm(ModelForm):
    class Meta:
        model = TipoVehiculo
        fields = ['nombre',
                  'caracteristicas',
                  'num_max_pasajeros',
                  'num_maletas',
                  ]