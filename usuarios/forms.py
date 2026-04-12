from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'rol']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)

        password = self.cleaned_data.get("password")

        # 🔐 Solo encripta si el usuario escribió una nueva contraseña
        if password:
            usuario.password = make_password(password)

        if commit:
            usuario.save()

        return usuario