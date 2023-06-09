var horarios_disponiveis = document.getElementById('horarios-disponiveis')
var dias_disponiveis = document.getElementById('dias-disponiveis')
var total_pagar = document.getElementById('total')
var soma = '00:00'
var total = 0.0
var servicos_selecionados = []


$(document).ready(function(){
	let multipleCancelButton = new Choices('#choices-multiple-remove-button', {
	   	removeItemButton: true,
	   	placeholderValue: 'Escolher serviços',
		noResultsText: 'Nenhum serviço encontrado',
   	   	noChoicesText: 'Não há mais serviços disponíveis',
		itemSelectText: 'Selecionar',
	})

    let selectElement = document.getElementById('choices-multiple-remove-button')

    selectElement.addEventListener('addItem', function(event) {
        soma = somarHorarios(soma, event.detail.value.split('-')[1])

        desmarcar_dias_selecionados()
        limparCampos()

        servicos_selecionados.push(event.detail.value.split('-')[0])
        
        total += convert_string_for_preco(event.detail.label)
        total = parseFloat(total.toFixed(2))

        total_pagar.innerHTML = `<p style="font-size: 1.2em;">Total a pagar: R$${total}</p>`
    })
      
    selectElement.addEventListener('removeItem', function(event) {
        soma = subtrairHorarios(soma, event.detail.value.split('-')[1])

        desmarcar_dias_selecionados()
        limparCampos()

        servicos_selecionados.splice(servicos_selecionados.indexOf(event.detail.value.split('-')[0]), 1)
        
        total -= convert_string_for_preco(event.detail.label)
        total = parseFloat(total.toFixed(2))

        total_pagar.innerHTML = `<p style="font-size: 1.2em;">Total a pagar: R$${total}</p>`
    })
})

function selecionarDia(event){
    if (soma !== '00:00'){
        let hora_abertura = event.target.getAttribute('data-hora-abertura')
        let hora_fechamento = event.target.getAttribute('data-hora-fechamento')
        let dia = event.target.value
        let divHorariosOcupados = document.getElementById('horarios-ocupados')
        let inputs = divHorariosOcupados.getElementsByTagName('input')
        let faixa_horarios = []

        horarios_disponiveis.innerHTML = ''
        
        if ((hora_abertura >= hora_fechamento) || (soma > hora_fechamento)){
            horarios_disponiveis.innerHTML = '<option selected>Nenhum horário disponível</option>'
        }else{
            let comparar = []
            let remover_horarios = []
            let horarios_finais = []

            // preenche o array com a faixa de horários já ocupados
            for (let i=0; i<inputs.length; i++) {
                let input = inputs[i]
                if (input.name == dia){
                    let partes = input.value.split('/')
                    comparar.push([partes[0], partes[1]])
                }
            }
            
            // gera a faixa de horários
            let horario_atual = hora_abertura
            while (horario_atual < hora_fechamento){
                faixa_horarios.push(horario_atual)
                horario_atual = somarHorarios(horario_atual, soma) 
            }

            // verifica o limite de horários iniciais da faixa de horários ocupados
            for (let i=0; i<faixa_horarios.length; i++){
                for (let j=0; j<comparar.length; j++){
                    if (faixa_horarios[i] >= comparar[j][0] && faixa_horarios[i] <= comparar[j][1]){
                        remover_horarios.push(faixa_horarios[i])
                    }
                }
            }
            
            // remove os horários de inicio da faixa de horários ocupados
            for (let i=0; i<remover_horarios.length; i++){
                let indi = faixa_horarios.indexOf(remover_horarios[i])
                if (indi !== -1) {
                    faixa_horarios.splice(indi, 1)
                }
            }

            // gera a faixa de horários finais com a faixa já cortada dos horários iniciais
            for (let i=0; i<faixa_horarios.length; i++){
                horarios_finais.push(somarHorarios(faixa_horarios[i], soma))
            }

            // verifica os horários finais com os horários ocupados
            remover_horarios.length = 0
            for (let i=0; i<horarios_finais.length; i++){
                for (let j=0; j<comparar.length; j++){
                    if (horarios_finais[i] >= comparar[j][0] && horarios_finais[i] <= comparar[j][1]){
                        remover_horarios.push(subtrairHorarios(horarios_finais[i], soma))
                    }
                }
            }

            for (let i=0; i<remover_horarios.length; i++){
                let indi = faixa_horarios.indexOf(remover_horarios[i])
                if (indi !== -1) {
                    faixa_horarios.splice(indi, 1)
                }
            }
        }

        faixa_horarios.forEach((obj, index)=>{
            let newInput = document.createElement('option')

            newInput.value = obj
            newInput.textContent = obj

            horarios_disponiveis.appendChild(newInput)
        })
    }
}

function somarHorarios(horario1, horario2) {
    let [horas1, minutos1] = horario1.split(':').map(Number)
    let [horas2, minutos2] = horario2.split(':').map(Number)
  
    let totalMinutos = minutos1 + minutos2
    let totalHoras = horas1 + horas2
  
    if (totalMinutos >= 60) {
        totalHoras += Math.floor(totalMinutos / 60)
        totalMinutos = totalMinutos % 60
    }

    let horaFormatada = totalHoras.toString().padStart(2, '0') + ':' + totalMinutos.toString().padStart(2, '0')
    return horaFormatada
}

function subtrairHorarios(horario1, horario2) {
    let [horas1, minutos1] = horario1.split(':').map(Number)
    let [horas2, minutos2] = horario2.split(':').map(Number)
  
    let totalMinutos = minutos1 - minutos2
    let totalHoras = horas1 - horas2
  
    if (totalMinutos < 0) {
        totalHoras -= 1
        totalMinutos += 60
    }
  
    if (totalHoras < 0) {
        totalHoras += 24
    }
  
    let horaFormatada = totalHoras.toString().padStart(2, '0') + ':' + totalMinutos.toString().padStart(2, '0')
    return horaFormatada
}

function desmarcar_dias_selecionados(){
    dias_disponiveis.querySelectorAll('input').forEach((radio) => {
        radio.checked = false
    })
}

function convert_string_for_preco(valor_string){
    let valor = valor_string.match(/R\$ ([\d,.]+)/)[1]
    return parseFloat(valor.replace(',', '.'))
}
  
function limparCampos(){
    total_pagar.innerHTML = '' 
    horarios_disponiveis.innerHTML = ''
    horarios_disponiveis.innerHTML = '<option selected>Escolher horário</option>'
}

function enviarFormularioAgendamento(){
    let mensagem = $('#msg')

    try {
        let form = document.getElementById('msform')

        let idade = document.getElementById('idade')
        let opcaoSelecionada = idade.options[idade.selectedIndex]
        let conteudoSelecionado = opcaoSelecionada.textContent

        let horario = horarios_disponiveis.options[horarios_disponiveis.selectedIndex]
        let horario_selecionado = horario.textContent

        let regexHorario = /^\d{2}:\d{2}$/
        
        if (
            (servicos_selecionados.length == 0) ||
            !(regexHorario.test(horario_selecionado)) ||
            (idade == 'Selecione a sua faixa etária')
            ){
            throw new Error()
        }else{
            // enviar o id do salao
            let url = window.location.pathname
            
            let input_id_salao = document.createElement("input")
            input_id_salao.type = "hidden"
            input_id_salao.name = "id_salao"
            input_id_salao.value = url.split('/').filter(Boolean).pop()

            // enviar a faixa etária
            let input_idade = document.createElement("input")
            input_idade.type = "hidden"
            input_idade.name = "idade"
            input_idade.value = conteudoSelecionado

            // enviar o total a pagar
            let input_total = document.createElement("input")
            input_total.type = "hidden"
            input_total.name = "total"
            input_total.value = total

            // enviar o dia selecionado
            let input_dia = document.createElement('input')
            input_dia.type = 'hidden'
            input_dia.name = 'dia_selecionado'
            input_dia.value = document.querySelector('input[name="dia"]:checked').value
            
            // enviar o horario selecionado 
            let input_horario = document.createElement('input')
            input_horario.type = 'hidden'
            input_horario.name = 'horario'
            input_horario.value = horario_selecionado

            // enviar os serviços selecionados
            servicos_selecionados.forEach(function(obj) {
                let input_servico = document.createElement('input')
                input_servico.type = 'hidden'
                input_servico.name = 'servicos_selecionados[]'
                input_servico.value = obj
                form.appendChild(input_servico)
            })

            form.appendChild(input_id_salao)
            form.appendChild(input_idade)
            form.appendChild(input_total)
            form.appendChild(input_dia)
            form.appendChild(input_horario)

            form.submit()
        }
    } catch (error) {
        mensagemTemporaria(mensagem, 'Informações inválidas/incompletas')
    }
}

function mensagemTemporaria(elemento, msg){
    elemento.text(msg)
    elemento.fadeIn()
    setTimeout(function() {
        elemento.fadeOut()
        elemento.text('')
    }, 3000)
}
