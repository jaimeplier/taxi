from django.forms import ModelForm, CharField, EmailField, NumberInput, PasswordInput, CheckboxSelectMultiple, forms
from config.models import Empresa


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
        model = Empresa
        fields = ['email',
                  'password',
                  'nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electronico',
                  'password': 'Contraseña',
                  'telefono': 'Telefono',
                  }
