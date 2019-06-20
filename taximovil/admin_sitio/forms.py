from django.forms import ModelForm

from config.models import Tarifa


class TarifaForm(ModelForm):
    class Meta:
        model = Tarifa
        fields = '__all__'
        labels = '__all__'
