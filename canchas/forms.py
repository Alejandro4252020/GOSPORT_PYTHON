from django import forms
from .models import Cancha

class CanchaForm(forms.ModelForm):
    class Meta:
        model = Cancha
        fields = '__all__'
        widgets = {
            'latitud': forms.HiddenInput(),
            'longitud': forms.HiddenInput(),
        }

    def clean_capacidad(self):
        capacidad = self.cleaned_data.get('capacidad')
        if capacidad is not None:
            if capacidad < 1:
                raise forms.ValidationError("La capacidad mínima debe ser al menos 1 persona.")
            if capacidad > 100:
                raise forms.ValidationError("La capacidad máxima de la cancha no puede superar las 100 personas.")
        return capacidad

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio < 0:
                raise forms.ValidationError("El precio no puede ser negativo.")
            if precio > 500000:
                raise forms.ValidationError("El precio de la cancha no puede superar 500.000 de pesos colombianos.")
        return precio