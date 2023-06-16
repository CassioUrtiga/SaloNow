function agendamentoEspecifico(id){
    window.location.href = '/detalhes-agendamento-especifico/' + id
}

function gerarRelatorio(event, id){
    let divSuperior = event.currentTarget.parentNode.previousElementSibling
    
    let inputMarcado = divSuperior.querySelector('input[name="btnradio' + id + '"]:checked')
    
    let index = inputMarcado.getAttribute('data-index')
    window.open('/relatorio/' + id + '/' + index, '_blank')
}

function limparTodoCache(){
    window.location.href = '/limpar-cache/0/0'
}

function limparCacheEspecifico(id){
    window.location.href = '/limpar-cache/' + id +'/1'
}