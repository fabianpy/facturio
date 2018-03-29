"""
Módulo útil para funciones varias
"""


def formatear_documento_nombre(tipo_doc, nro_doc, nombres, apellidos=None):
    formateado = "{}-{} {}".format(tipo_doc, nro_doc, nombres)
    if apellidos:
        formateado += " " + apellidos
    return formateado


def formatear_documento(tipo_doc, nro_doc):
    return "{} - {}".format(tipo_doc, nro_doc)
