from django.forms import ModelForm, PasswordInput, Select

from config.models import Empresa, Usuario, Chofer, Sitio, Zona, Base, Direccion, Pais, Ciudad, Sucursal, TipoPago, \
    TipoVehiculo, Cliente, TipoServicio, Marca, Modelo, Propietario, Vehiculo, Tarifa, Comisiones, Rol


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre',
                  'direccion',
                  ]
        labels = {'nombre': 'Nombre',
                  'direccion': 'Dirección',
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
        widgets = {'password': PasswordInput()}


class ChoferForm(ModelForm):
    class Meta:
        model = Chofer
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  'numero_licencia',
                  'turno',
                  'saldo',
                  'estatus'
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }
        widgets = {'password': PasswordInput(),
                   'estatus': Select(choices=[[True, 'Activo'], [False, 'Inactivo']])}


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
        fields = ['nombre']


class TipoVehiculoForm(ModelForm):
    class Meta:
        model = TipoVehiculo
        fields = ['nombre',
                  'caracteristicas',
                  'num_max_pasajeros',
                  'num_maletas',
                  ]


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  'rfc',
                  'cp',
                  'lada'
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }
        widgets = {'password': PasswordInput()}


class TipoServicioForm(ModelForm):
    class Meta:
        model = TipoServicio
        fields = ['nombre',
                  ]
        labels = {'nombre': 'Nombre',
                  }


class MarcaForm(ModelForm):
    class Meta:
        model = Marca
        fields = ['nombre',
                  ]
        labels = {'nombre': 'Nombre',
                  }


class ModeloForm(ModelForm):
    class Meta:
        model = Modelo
        fields = ['nombre',
                  'marca',
                  ]
        labels = {'nombre': 'Modelo',
                  'marca': 'Marca'
                  }


class PropietarioForm(ModelForm):
    class Meta:
        model = Propietario
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  'tipo_persona',
                  'razon_social',
                  'direccion_fiscal',
                  'nombre_banco',
                  'titular_cuenta',
                  'clabe',
                  'numero_cuenta',
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }
        widgets = {'password': PasswordInput()}


class VehiculoForm(ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['placa',
                  'anio',
                  'cromatica',
                  'modelo',
                  'propietario',
                  'economico',
                  'ciudad',
                  ]


class TarifaForm(ModelForm):
    class Meta:
        model = Tarifa
        fields = '__all__'
        labels = '__all__'


class ComisionForm(ModelForm):
    class Meta:
        model = Comisiones
        fields = '__all__'


class PermisosForm(ModelForm):
    class Meta:
        model = Rol
        fields = '__all__'
