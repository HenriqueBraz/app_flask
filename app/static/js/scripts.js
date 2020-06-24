$(document).ready( function () {
    $('#table_id').DataTable( {
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese-Brasil.json"
        }
    });
} );


 $(document).ready(function(){

    $(".cep").focusout(function(){
	    //Início do Comando AJAX
	    $.ajax({
		    //O campo URL diz o caminho de onde virá os dados
		    //É importante concatenar o valor digitado no CEP
		    url: 'https://viacep.com.br/ws/'+$(this).val()+'/json/unicode/',
		    //Aqui você deve preencher o tipo de dados que será lido,
		    //no caso, estamos lendo JSON.
		    dataType: 'json',
		    //SUCESS é referente a função que será executada caso
		    //ele consiga ler a fonte de dados com sucesso.
		    //O parâmetro dentro da função se refere ao nome da variável
		    //que você vai dar para ler esse objeto.
		    success: function(resposta){
			    //Agora basta definir os valores que você deseja preencher
			    //automaticamente nos campos acima.
			    $(".endereco").val(resposta.logradouro);
			    //$(".complemento").val(resposta.complemento);
			    $(".bairro").val(resposta.bairro);
			    $(".cidade").val(resposta.localidade);
			    $(".estado").val(resposta.uf);
			    //Vamos incluir para que o Número seja focado automaticamente
			    //melhorando a experiência do usuário
			    $(".numero").focus();
		    }
	    });
	});
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
    $('.numero').mask('0000');

    var conteudoNovo = "";
    var conteudoOriginal = "";
    var input1 = "";
    var input2 = "";
    $('td.valor_faturamento').click(function(){
        if ($('td > input').length > 0){
        return;
        }
        conteudoOriginal = $(this).text();
        var novoElemento = $('<input/>',{type:'text', name:"faturamento", id:"faturamento", value:conteudoOriginal}).mask('#.##0,00', {reverse: true});
        $(this).html(novoElemento.bind('blur keydown',function(e){
            var keyCode = e.which;
            if( keyCode == 13){
                conteudoNovo = $(this).val();
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

    $('#data_financeiro').datepicker({
    monthNames: [ "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julio", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro" ],
    minDate: "0",
    dateFormat: 'dd/mm/yy',
    dayNamesMin: [ "Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb" ],
    locales: 'pt-br',
    });

});

function salva_dados(){
    var nomes = [];
    var faturamentos = "";
    input = document.querySelector('[name="faturamento"]');
    $('#table_id tbody tr').each(function() {
        var temp = $(this).find('td').eq(5).text();
        faturamentos += temp + "@";
    });

    input.value = faturamentos; // Valor da coluna faturamento
};














