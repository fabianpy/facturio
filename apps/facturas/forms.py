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
            'tipo_doc': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
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
        fields = ['timbrado', 'establecimiento', 'punto_expedicion', 'numero', 'proveedor', 'fecha', 'tipo', 'moneda']
        labels = {'timbrado': 'Timbrado',
                  # 'establecimiento': 'Nro. Documento',
                  # 'punto_expedicion': 'Nombre',
                  # 'numero': 'Número',
                  'fecha': 'Fecha',
                  'proveedor': 'Proveedor',
                  'tipo': 'Tipo Factura',
                  'moneda': 'Moneda'
                  }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'timbrado': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'establecimiento': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'punto_expedicion': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'required': 'required'}),
            'tipo': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'moneda': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),

        }
