$(document).on("click", "#botao_modal", function () {

       var id = $(this).attr('data-id');
       console.log(id)
        $(".modal-body #id").val(id);

 });


$(document).ready( function () {
    $('#table_id').DataTable();
} );

$(document).ready( function () {
    $('#table_id2').DataTable();
} );