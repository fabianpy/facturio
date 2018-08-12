from django import forms

from apps.facturas.models import FacturaProveedor, Proveedor, GrupoProveedor


class GrupoProveedorForm(forms.ModelForm):
    class Meta:
        model = GrupoProveedor
        fields = ['nombre', 'habilitado']
        labels = {'nombre': 'Nombre',
                  'habilitado': 'Habilitado'
                  }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['tipo_doc', 'nro_doc', 'nombre', 'grupo', 'direccion', 'telefono', 'email', 'habilitado']
        labels = {'tipo_doc': 'Tipo de Documento',
                  'nro_doc': 'Nro. Documento',
                  'nombre': 'Nombre',
                  'grupo': 'Grupo',
                  'direccion': 'Dirección',
                  'telefono': 'Teléfono',
                  'email': 'E-Mail',
                  'habilitado': 'Habilitado'
                  }
        widgets = {
            'tipo_doc': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'nro_doc': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'grupo': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'habilitado': forms.CheckboxInput(attrs={'class': 'big-checkbox', 'type': 'checkbox'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo'].queryset = GrupoProveedor.user_objects.filter(habilitado=True)


class FacturaProveedorForm(forms.ModelForm):
    class Meta:
        model = FacturaProveedor
        fields = ['timbrado', 'establecimiento', 'punto_expedicion', 'numero', 'proveedor', 'fecha', 'tipo']
        labels = {'timbrado': 'Timbrado',
                  'fecha': 'Fecha',
                  'proveedor': 'Proveedor',
                  'tipo': 'Tipo Factura',
                  # 'moneda': 'Moneda'
                  }
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            'timbrado': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'establecimiento': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'punto_expedicion': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'required': 'required'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control datepicker', 'required': 'required'}),
            'tipo': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),
            # 'moneda': forms.Select(attrs={'class': 'form-control-chosen', 'style': 'width: 100%'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['proveedor'].queryset = Proveedor.user_objects.filter(habilitado=True)
