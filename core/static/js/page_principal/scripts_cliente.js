function btn_sair(){
    window.location.href="/logout/"
}
                
function realizarAgendamento(id){
    window.location.href = '/agendamento-cliente/'+ id
}

function cancelarAgendamento(id){
    window.location.href = '/cancelar-agendamento/' + id
}

function cancelarTodosAgendamentos(){
    window.location.href = '/cancelar-todos-agendamentos/'
}

function telaPrincipal(){
    window.location.href = '/tela-principal/'
}

function redirectAgendamento(id) {
    $('html, body').animate({
        scrollTop: $('#' + id).offset().top
    }, 100)
}

function sidebarToggle() {
    let sidebar = $('#sb1');
    if (sidebar.hasClass('slide-open')) {
        sidebar.removeClass('slide-open')
        sidebar.addClass('slide-close')
        setTimeout(function() {
            sidebar.css('display', 'none')
        }, 570)
    } else {
        sidebar.removeClass('slide-close')
        sidebar.addClass('slide-open')
        sidebar.css('display','block')
    }
}
