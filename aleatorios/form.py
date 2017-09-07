from django.forms import ModelForm

from aleatorios.models import Calculator, Lineal_metodo


class formcalculator(ModelForm):
    class Meta:
        model = Calculator
        fields = "__all__"


class formLineal(ModelForm):
    class Meta:
        model = Lineal_metodo
        fields = "__all__"
