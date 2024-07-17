from django import forms
from .models import Entidad


class ProductoForm(forms.Form):
    opciones = forms.ModelChoiceField(queryset=Entidad.objects.all())
