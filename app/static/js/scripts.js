$(document).ready( function () {
    $('#table_id').DataTable();
} );

$(document).ready( function () {
    $('#table_id2').DataTable();
} );

$(document).ready( function () {

    $(".estado").focusout(function(){
        var estado = $(this).val();
        alert(estado);
    });
} );

 $(document).ready(function(){
  $('.cnpj').mask('00.000.000/0000-00');
  $('.cnae_principal').mask('0000-0/00');
  $('.cnae_secundaria').mask('0000-0/00');
  $('.nire').mask('00000000000');
  $('.ccm').mask('0.000.000.0');
  $('.cpf').mask('000-000.000-00');
  $('.cnpj').mask('00.000.000/0000-00');
  $('.rg').mask('00.000.000-0');
  $('.cep').mask('00000-000');
  $('.telefone').mask('(00) 0000-0000');
  $('.celular').mask('(00) 00000-0000');
  $('.capital_social').mask('#.##0,00', {reverse: true});
  $('.dinheiro').mask('#.##0,00', {reverse: true});
  $('.inscricao_estadual').mask('000.000.000.000');

});

$(document).ready(function(){
    $('.valor_faturamento').dblclick(function(){
        if ($('td > input').length > 0){
        return;
        }
        var conteudoOriginal = $(this).text();
        var novoElemento = $('<input/>',{type:'text', value:conteudoOriginal});
        $(this).html(novoElemento.bind('blur keydown',function(e){
            var keyCode = e.which;
            if( keyCode == 13){
                var conteudoNovo = $(this).val();
                if( conteudoNovo != "" ){
                    $(this).parent().html(conteudoNovo);
                }
            }
            if( e.type == "blur" ){
                 $(this).parent().html(conteudoOriginal);
            }
        }));
        $(this).children().select();
    });
});





