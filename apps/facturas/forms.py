from django import forms

from apps.facturas.models import FacturaProveedor, Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['tipo_doc', 'nro_doc', 'nombre', 'direccion', 'telefono', 'email', 'habilitado']
        labels = {'tipo_doc': 'Tipo de Documento',
                  'nro_doc': 'Nro. Documento',
                  'nombre': 'Nombre',
                  'direccion': 'Dirección',
                  'telefono': 'Teléfono',
                  'email': 'E-Mail',
                  'habilitado': 'Habilitado'
                  }
        widgets = {
            'tipo_doc': forms.Select(attrs={'style': 'width: 100%'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }


class FacturaProveedorForm(forms.ModelForm):
    class Meta:
        model = FacturaProveedor
        fields = ['timbrado', 'establecimiento', 'punto_expedicion', 'numero', 'fecha', 'tipo', 'moneda']


