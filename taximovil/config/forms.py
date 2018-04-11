from django.forms import ModelForm, CharField, EmailField, NumberInput, PasswordInput, CheckboxSelectMultiple, forms, Select
from config.models import Empresa, Usuario, Chofer, Sitio, Zona, Base, Direccion


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