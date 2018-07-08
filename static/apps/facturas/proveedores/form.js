$(function(){
    $('.modal').removeClass('fade');

    $('#nuevo').click(function(){
        $('#timbrado_id').val(null);
        $('#timbrado').val(null);
        $('#establecimiento').val(null);
        $('#punto_expedicion').val(null);
        $('#vigencia').val(null);
        $('#vencimiento').val(null);

    });

    $('[name="timbrado"]').click(function(){
        var id = $(this).attr('id');
        $('#timbrado_id').val(id);
        $.get('/facturas/proveedores/timbrado/'+id, {id:id})
        .done(function(data){
            var data = $.parseJSON(data)[0].fields;
            console.log("data ", data);

            $('#timbrado').val(data.timbrado);
            $('#establecimiento').val(data.establecimiento);
            $('#punto_expedicion').val(data.punto_expedicion);
            $('#vigencia').val(data.vigencia);
            $('#vencimiento').val(data.vencimiento);

            $('#modalTimbrado').modal('show');
        });
    });

    $('#guardarDetalle').click(function(){
        console.log('clic en guardar');
        var data = new Object();
        data.proveedor = parseInt($('#object_id').val());
        data.timbrado = $('#timbrado').val();
        data.establecimiento = parseInt($('#establecimiento').val());
        data.punto_expedicion = parseInt($('#punto_expedicion').val());
        data.vigencia = $('#vigencia').val();
        data.vencimiento = $('#vencimiento').val();
        data.csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();

        var url = '';
        if ($('#timbrado_id').val() == null || $('#timbrado_id').val() == '') {
            url = '/facturas/proveedores/timbrado/crear';
        } else {
            url = '/facturas/proveedores/timbrado/editar';
            data.id = $('#timbrado_id').val();
        }

        console.log('el url es:', url, 'object detalle id: "' + $('#timbrado_id').val() + '"'); //borrar

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

})
