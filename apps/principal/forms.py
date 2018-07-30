from django import forms

from django.contrib.auth.forms import AuthenticationForm


class PrincipalAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'Usuario'}),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )
