from django.forms import ModelForm, PasswordInput

from config.models import AdministradorSitio, Sitio


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

class AdministradorSitioForm(ModelForm):
    class Meta:
        model = AdministradorSitio
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
                  'email': 'Correo electrónico',
                  'password': 'Contraseña',
                  'telefono': 'Teléfono',
                  }
        widgets = {'password': PasswordInput()}