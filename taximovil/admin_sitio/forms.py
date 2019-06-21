from django.forms import ModelForm, PasswordInput

from config.models import Tarifa, Callcenter


class TarifaForm(ModelForm):
    class Meta:
        model = Tarifa
        fields = '__all__'
        labels = '__all__'

class CallcenterForm(ModelForm):
    class Meta:
        model = Callcenter
        fields = ['nombre',
                  'a_paterno',
                  'a_materno',
                  'telefono',
                  'email',
                  'password'
                  ]
        labels = {'nombre': 'Nombre',
                  'a_paterno': 'Apellido paterno',
                  'a_materno': 'Apellido materno',
                  'email': 'Correo electrónico',
                  'password': 'Contraseña',
                  'telefono': 'Teléfono',
                  }
        widgets = {'password': PasswordInput()}