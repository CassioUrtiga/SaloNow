let cep = document.getElementById('cep')
let cidade = document.getElementById('cidade')
let uf = document.getElementById('uf')
let valor = ''

// mudar por cep
cep.addEventListener('input', ()=>{
    valor = cep.value
    if (valor.length === 9){
        $.ajax({
            url: `https://viacep.com.br/ws/${valor.replace('-','')}/json/`,
            type: "get",
            success: function(dados,status){
                if (dados.erro === true || status == 'error' || dados.erro === 'true'){
                    $('#msg-error1 p').text('CEP inválido')
                    $('#validation_message1').val('')
                    $('#msg-error1').fadeIn()
                }else{
                    $('#msg-error1 p').text(`${dados.localidade}, ${dados.uf}`)
                    $('#validation_message1').val(`${dados.cep},${dados.localidade},${dados.uf}`)
                    $('#msg-error1').fadeIn()
                }
            },
            error: function(){
                $('#msg-error1 p').text('Aguarde um momento e tente novamente!')
                $('#validation_message1').val('')
                $('#msg-error1').fadeIn()
            },
        })
    }else{
        $('#msg-error1').fadeOut()
    }
})

// mudar por cidade e uf
document.getElementById('pesquisar').addEventListener('click', ()=>{
    $.ajax({
        url: `https://viacep.com.br/ws/${uf.value.trim().toUpperCase()}/${cidade.value.trim().toUpperCase()}/Cidade/json/`,
        type: "get",
        success: function(dados,status){
            if (dados.length !== 0){
                if (dados[0].erro === true || status == 'error' || dados[0].erro === 'true'){
                    $('#msg-error2 p').text('CEP inválido')
                    $('#validation_message2').val('')
                    $('#msg-error2').fadeIn()
                    $('#msg-error2').delay(4000).fadeOut()
                }else{
                    $('#msg-error2 p').text(`${dados[0].cep}, ${dados[0].localidade}, ${dados[0].uf}`)
                    $('#validation_message2').val(`${dados[0].cep},${dados[0].localidade},${dados[0].uf}`)
                    $('#msg-error2').fadeIn()
                }
            }else{
                $('#msg-error2 p').text('Endereço não encontrado')
                $('#validation_message2').val('')
                $('#msg-error2').fadeIn()
                $('#msg-error2').delay(4000).fadeOut()
            }
        },
        error: function(){
            $('#msg-error2 p').text('Aguarde um momento e tente novamente!')
            $('#validation_message2').val('')
            $('#msg-error2').fadeIn()
            $('#msg-error2').delay(4000).fadeOut()
        },
    })
})

// limpar o modal quando sair
$('#exampleModal').on('hidden.bs.modal', ()=> {
    cep.value = ''
    cidade.value = ''
    uf.value = ''
    $('#msg-error1 p').text('')
    $('#validation_message1').val('')
    $('#msg-error2 p').text('')
    $('#validation_message2').val('')
})


// limpa os campos cidade e uf se estiverem vazios
cidade.addEventListener('input', ()=>{
    if (cidade.value === ''){
        uf.value = ''
        $('#msg-error2 p').text('')
        $('#validation_message2').val('')
    }
})

uf.addEventListener('input', ()=>{
    if (uf.value === ''){
        cidade.value = ''
        $('#msg-error2 p').text('')
        $('#validation_message2').val('')
    }
})
  