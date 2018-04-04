from django.forms import ModelForm, CharField, EmailField, NumberInput, PasswordInput, CheckboxSelectMultiple, forms
from config.models import Empresa, Usuario, Chofer, Sitio


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
                  ]
        labels = {'nombre': 'Nombre',
                  }