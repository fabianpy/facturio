from django import forms

from apps.personas.models import Persona


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombres', 'apellidos', 'tipo_doc', 'nro_doc', 'tipo_persona']
        labels = {'nombres': 'Nombres',
                  'apellidos': 'Apellidos',
                  'tipo_persona': 'Tipo'
                  }
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_doc': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'tipo_persona': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
        }
