from django import forms
from .models import Usuario
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


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

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            from .validators import validar_seguridad_contrasena
            validar_seguridad_contrasena(password)
        return password

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')

        # 🔐 Solo encripta si escribió nueva contraseña
        if password:
            usuario.password = make_password(password)

        if commit:
            usuario.save()

            # ✅ Sincronizar auth.User
            auth_user = (
                User.objects.filter(email=usuario.email).first() or
                User.objects.filter(username=usuario.username).first()
            )

            if auth_user:
                auth_user.username = usuario.username
                auth_user.email = usuario.email

                if password:
                    auth_user.set_password(password)

                # ✅ Sincronizar rol → permisos Django
                if usuario.rol == 'admin':
                    auth_user.is_superuser = True
                    auth_user.is_staff = True
                elif usuario.rol == 'empleado':
                    auth_user.is_superuser = False
                    auth_user.is_staff = True
                else:
                    auth_user.is_superuser = False
                    auth_user.is_staff = False

                auth_user.save()

        return usuario