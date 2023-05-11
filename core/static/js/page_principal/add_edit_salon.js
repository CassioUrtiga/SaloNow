let btnAddSalon = document.getElementById('addsalon')

let form = document.querySelector('#modalsalon .modal-body form')
let titulo = document.querySelector('#modalsalon .modal-header h1')
let imageSalon = document.getElementById('imgs')
let nameSalon = document.getElementById('salon-name')
let descricao = document.getElementById('desc-salon')
let locations = document.querySelectorAll('.location-inputs input')
let servicos = document.getElementById('input-container')
let daysFunc = document.querySelectorAll('#days-selector input')
let btnSubmit = document.querySelector('#modalsalon .modal-footer input')

// Adicionar novo salão
btnAddSalon.addEventListener('click', ()=>{
    titulo.textContent = 'Adicionar salão'
    btnSubmit.value = 'Adicionar salão'
    form.action = '/criar-salao/'

    imageSalon.innerHTML = 'Escolher banner (700x200)'
    nameSalon.value = ''
    descricao.value = ''
    servicos.innerHTML = ''

    for (let i=0; i<locations.length; i++) {
        locations[i].value = ''
    }

    limparDatasHorarios()
})

// Editar salão
function editarSalao(event){
    let elementoPai = event.target.closest('.card-body').parentNode

    let dias = elementoPai.querySelectorAll('#table-view-days tbody tr td')
    let arrayDatas = []
    let localidade = elementoPai.querySelector('.div1 p small').innerText.trim().replace('(','').replace(')','').replace(' - ',',').split(',')
    let services = elementoPai.querySelectorAll('#table-view-services tbody tr td')

    titulo.textContent = 'Editar salão'
    btnSubmit.value = 'Salvar alterações'
    form.action = '/editar-salao/' + elementoPai.getAttribute('id') + '/'

    imageSalon.innerHTML = 'Escolher banner (700x200)'
    nameSalon.value = elementoPai.querySelector('.div2 h3').innerText
    descricao.value = elementoPai.querySelector('.div2 p').innerText
    servicos.innerHTML = ''

    locations[0].value = localidade[0]
    locations[1].value = localidade[4]
    locations[2].value = localidade[1]
    locations[3].value = localidade[2]
    locations[4].value = localidade[3]

    // Preenche os serviços
    for (let i=0; i<services.length; i+=2){
        const newRow = document.createElement('tr')
    
        newRow.innerHTML = `
            <tr>
                <td>
                    <input type="text" class="form-control" name="servicos[]" placeholder="Serviço" value="${services[i].textContent.replace('R$','').trim()}" oninput="event_input_void(event)"" />
                </td>
                <td>
                    <input type="number" class="form-control" step="0.01" name="precos[]" placeholder="Preço" value="${parseFloat(services[i+1].textContent.replace('R$','').replace(',','.').trim())}"/>
                </td>
                <td>
                    <button class="btn btn-danger remove-button"><i class="fas fa-times"></i> Remover serviço</button>
                </td>
            </tr>
        `;

        const removeButton = newRow.querySelector('.remove-button')
        removeButton.addEventListener('click', () => {
            newRow.remove()
        });
        
        servicos.appendChild(newRow)
    }

    let texto = ''
    dias.forEach((td, index) => {
        texto += td.textContent.trim() + ',' 
        if ((index + 1) % 3 === 0 && texto.length > 0) {
            arrayDatas.push(texto.split(','))
            texto = ''
        }
    });

    limparDatasHorarios()
    
    // Marca os dias e insere as horas
    for (let i=0; i<daysFunc.length; i+=3) {
        for (let j=0; j<arrayDatas.length; j++){
            if (daysFunc[i].name.startsWith(arrayDatas[j][0].toLowerCase().slice(0, 3))){
                daysFunc[i].checked = true;
                daysFunc[i+1].value = arrayDatas[j][1].trim()
                daysFunc[i+2].value = arrayDatas[j][2].trim()
                daysFunc[i+1].disabled = false
                daysFunc[i+2].disabled = false
            }
        }
    }

}

function limparDatasHorarios(){
    for (let i=0; i<daysFunc.length; i++) {

        if (daysFunc[i].type === 'time') {
            daysFunc[i].value = '00:00:00'
            daysFunc[i].disabled = true
        }

        if (daysFunc[i].type === 'checkbox') {
            daysFunc[i].checked = false
        }
    }
}

// Adiciona evento de desmarque para zerar as horas
for (let i=0; i<daysFunc.length; i+=3) {
    daysFunc[i].addEventListener('change', function(event) {
        if (event.target.checked) {
            daysFunc[i+1].disabled = false
            daysFunc[i+2].disabled = false
        }else{
            daysFunc[i+1].value = '00:00:00'
            daysFunc[i+1].disabled = true
            daysFunc[i+2].value = '00:00:00'
            daysFunc[i+2].disabled = true
        }
    })
}
  
