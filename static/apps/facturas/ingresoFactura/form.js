$(function(){
    $('.modal').removeClass('fade');

    $('#nuevo').click(function(){
        $('#object_detalle_id').val(null);
        $('#cantidad').val(1);
        $('#monto').val(0);
        $('#iva').val(1).trigger('chosen:updated');
        $('#monto_iva').val(0);
        $('#descripcion').val('');

    });

    $('[name="detalleFactura"]').click(function(){
        var id = $(this).attr('id');
        console.log("el id es = ", id);
        $('#object_detalle_id').val(id);
        $.get('/facturas/ingresoFactura/detalle/'+id, {id:id})
        .done(function(data){
            var data = $.parseJSON(data)[0].fields;
//            console.log("data ", $.parseJSON(data));
            console.log("data ", data);
//            console.log("data ", data[0].fields);

            $('#cantidad').val(data.cantidad);
            $('#monto').val(data.monto);
            $('#iva').val(data.iva).trigger("chosen:updated");
            $('#monto_iva').val(data.monto_iva);
            $('#descripcion').val(data.descripcion);

            $('#modalDetalle').modal('show');
        });
    });

    $('#guardarDetalle').click(function(){
        console.log('clic en guardar');
        var data = new Object();
        data.factura = parseInt($('#object_id').val());
        data.cantidad = parseInt($('#cantidad').val());
        data.monto = parseFloat($('#monto').val(), 10);
        data.iva = parseInt($('#iva').val());
        data.monto_iva = parseFloat($('#monto_iva').val(), 10);
        data.descripcion = $('#descripcion').val();
        data.csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

        var url = '';
        if ($('#object_detalle_id').val() == null || $('#object_detalle_id').val() == '') {
            url = '/facturas/ingresoFactura/detalle/crear';
        } else {
            url = '/facturas/ingresoFactura/detalle/editar';
            data.id = $('#object_detalle_id').val();
        }

        console.log('el url es:', url, 'object detalle id: "' + $('#object_detalle_id').val() + '"'); //borrar

        $.post(url, data)
        .done(function(data) {
            console.log("llego al done");
            //$('#modalDetalle').modal('hide');
            location.reload();
        })
        .fail(function(data) {
            alert("ERROR")
        })

    });

    /***************** ON CHANGE *******************/

    $('#cantidad').change(function(){
        var parameters = getParameters();
        console.log('parameters', parameters);
        var montoIva = calcularIVA(parameters);
        $('#monto_iva').val(montoIva);
    });

    $('#monto').change(function(){
        var parameters = getParameters();
        console.log('parameters', parameters);
        var montoIva = calcularIVA(parameters);
        $('#monto_iva').val(montoIva);
    });

    $('#iva').change(function(){
        var parameters = getParameters();
        console.log('parameters', parameters);
        var montoIva = calcularIVA(parameters);
        $('#monto_iva').val(montoIva);
    });


    /***************** ON FOCUS OUT *******************/

    $('#id_timbrado').focusout(function(){

        //console.log("$('#object_id').val()", $('#object_id').val(), $('#object_id').val().length);
        if ($('#object_id').val() != null && $('#object_id').val().length == 0) {
            buscarDatosTimbradoProveedor($('#id_timbrado').val());
        }
    });

})

function getParameters() {
    var parameters = new Object;
    parameters.cantidad = $('#cantidad').val();
    parameters.monto = $('#monto').val();
    parameters.iva = $('#iva').val();
    return parameters;
}

function calcularIVA(param) {
    var montoTotal = param.cantidad * param.monto;
    if (param.iva == 1) //10%
        return redondearNumero((montoTotal / 11), 0);
    else if (param.iva == 2) //5%
        //return montoTotal / 21;
        return redondearNumero((montoTotal / 21), 0);
    else if (param.iva == 3) //exenta
        return 0;
    else alert("Código de IVA no definido")
}

function buscarDatosTimbradoProveedor(timbrado) {
    var data = new Object;
    data.timbrado = timbrado;
    data.csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    var $data = new Object;

    $.post('/facturas/ingresoFactura/timbradoProveedor', data)
    .done(function(data) {
        console.log("llego al done");
        console.log("data", $.parseJSON(data)[0]);

        var data = $.parseJSON(data)[0];
        if(data.pk != null) {
            $data = data.fields;
            setDataTimbradoProveedor($data);
        }
        else
            $data = null;
    })
    .fail(function(data) {
       // alert("Error al traer datos del proveedor.")
    })
}

function setDataTimbradoProveedor(data) {
    console.log("data en set tim pro", data);
    $('#id_establecimiento').val(data.establecimiento);
    $('#id_punto_expedicion').val(data.punto_expedicion);
    $('#id_proveedor').val(data.proveedor).trigger('chosen:updated');
    $('#id_numero').focus();
}

function redondearNumero(numero, decimales){
    return +(Math.round(numero+ "e+" + decimales)  + "e-" + decimales);
}