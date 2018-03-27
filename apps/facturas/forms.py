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

        }


class FacturaProveedorForm(forms.ModelForm):
    class Meta:
        model = FacturaProveedor
        fields = ['timbrado', 'establecimiento', 'punto_expedicion', 'numero', 'fecha', 'tipo', 'moneda']


