from django.forms import ModelForm, PasswordInput

from config.models import AdministradorCiudad


class AdministradorCiudadForm(ModelForm):
    class Meta:
        model = AdministradorCiudad
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password',
                  'ciudad'
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electrónico',
                  'password': 'Contraseña',
                  'telefono': 'Teléfono',
                  }
        widgets = {'password': PasswordInput()}