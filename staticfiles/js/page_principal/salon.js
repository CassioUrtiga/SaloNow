var redimensionar = null
var imagem_atual = null
var render = true // true renderiza a tela de add salao, false tela de edit salao
var reset = false // true edit salão com reset, false edit salão sem reset

let btnAddSalon = document.getElementById('addsalon')
let form = document.getElementById('form-salao')
let titulo = document.querySelector('#modalsalon .modal-header h1')
let nameSalon = document.getElementById('salon-name')
let descricao = document.getElementById('desc-salon')
let locations = document.querySelectorAll('.location-inputs input')
let servicos = document.getElementById('input-container')
let daysFunc = document.querySelectorAll('#days-selector input')
let btnSubmit = document.querySelector('#modalsalon .modal-footer input')
let tempContent = document.getElementById('temp-content')

// Adicionar novo salão
btnAddSalon.addEventListener('click', ()=>{
    render = true
    titulo.textContent = 'Adicionar salão'
    btnSubmit.value = 'Adicionar salão'
    form.action = '/criar-salao/'
    
    nameSalon.value = ''
    descricao.value = ''
    servicos.innerHTML = ''

    for (let i=0; i<locations.length; i++) {
        locations[i].value = ''
    }

    limpar_croppie()
    create_element_add_salon()

    renderizar_imagem()
    limparDatasHorarios()
})

// Editar salão
function editarSalao(event){
    let elementoPai = event.target.closest('.card-body').parentNode
    let imagem_url = elementoPai.querySelector('input').value
    imagem_atual = imagem_url
   
    limpar_croppie()

    if (imagem_url.includes('default.jpg')){
        render = true
        create_element_add_salon()
        renderizar_imagem()
    }else{
        render = false
        create_element_edit_salon(imagem_url)
    }

    let dias = elementoPai.querySelectorAll('#table-view-days tbody tr td')
    let arrayDatas = []
    let localidade = elementoPai.querySelector('.div1 p small').innerText.trim().replace('(','').replace(')','').replace(' - ',',').split(',')
    let services = elementoPai.querySelectorAll('#table-view-services tbody tr td')

    titulo.textContent = 'Editar salão'
    btnSubmit.value = 'Salvar alterações'
    form.action = '/editar-salao/' + elementoPai.getAttribute('id') + '/'

    nameSalon.value = elementoPai.querySelector('.div2 h3').innerText
    descricao.value = elementoPai.querySelector('.div2 p').innerText
    servicos.innerHTML = ''
    servicos.parentNode.style.display = 'block'

    locations[0].value = localidade[0]
    locations[1].value = localidade[4]
    locations[2].value = localidade[1]
    locations[3].value = localidade[2]
    locations[4].value = localidade[3]
    
    // Preenche os serviços
    for (let i=0; i<services.length; i+=4){
        let newRow = document.createElement('tr')
    
        newRow.innerHTML = `
            <tr>
                <td>
                    <input type="text" class="form-control" name="servicos[]" placeholder="Serviço" value="${services[i].textContent.replace('R$','').trim()}" oninput="event_input_void(event)"" />
                </td>
                <td>
                    <input type="number" class="form-control" step="0.01" min="0.00" name="precos[]" placeholder="Preço" value="${parseFloat(services[i+1].textContent.replace('R$','').replace(',','.').trim())}" oninput="validity.valid||(value='');"/>
                </td>
                <td>
                    <input type="time" class="form-control" name="duracao_homem[]"  value="${services[i+2].textContent}" required />
                </td>
                <td>
                    <input type="time" class="form-control" name="duracao_mulher[]"  value="${services[i+3].textContent}" required />
                </td>
                <td>
                    <button class="btn btn-danger remove-button"><i class="fas fa-times"></i> Remover serviço</button>
                </td>
            </tr>
        `

        let removeButton = newRow.querySelector('.remove-button')
        removeButton.addEventListener('click', () => {
            newRow.remove()
            if (servicos.querySelectorAll('tr').length === 0) {
                servicos.parentNode.style.display = 'none'
            }
        })
        
        servicos.appendChild(newRow)
    }

    let texto = ''
    dias.forEach((td, index) => {
        texto += td.textContent.trim() + ',' 
        if ((index + 1) % 3 === 0 && texto.length > 0) {
            arrayDatas.push(texto.split(','))
            texto = ''
        }
    })

    limparDatasHorarios()
    
    // Marca os dias e insere as horas
    for (let i=0; i<daysFunc.length; i+=3) {
        for (let j=0; j<arrayDatas.length; j++){
            if (daysFunc[i].name.startsWith(arrayDatas[j][0].toLowerCase().slice(0, 3))){
                daysFunc[i].checked = true
                daysFunc[i+1].value = arrayDatas[j][1].trim()
                daysFunc[i+2].value = arrayDatas[j][2].trim()
                daysFunc[i+1].disabled = false
                daysFunc[i+2].disabled = false
            }
        }
    }
}

// Evento de desmarque do checkbox para zerar as horas
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

// Envia o formulário de adicionar ou editar salão
$('#submit-form').on('click', function() {
    let form = document.getElementById('form-salao')
    let input_img = document.createElement("input")
    let imagemCrop = $('#imagem-crop')

    input_img.type = "hidden"
    input_img.name = "img_salao"
    
    if (imagemCrop.length > 0 && imagemCrop[0].files.length === 0){ // imagem é vazia
        input_img.value = ''
        form.appendChild(input_img)
        form.submit()
    }else{
        if (redimensionar === null || imagemCrop[0].files.length === 0){ // não houve alteração na imagem
            input_img.value = 'null'
            form.appendChild(input_img)
            form.submit()
        }else{
            redimensionar.croppie('result', {
                type: 'canvas',
                size: 'viewport',
                format: 'jpeg',
            }).then(function(imgRecortada) { // enviar a imagem recortada
                input_img.value = imgRecortada
                form.appendChild(input_img)
                form.submit()
            })
        }
    }
})

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

// Renderiza um novo croppie e a imagem
function renderizar_imagem(){
    redimensionar = $('#preview').croppie({
        enableExif: true,
    
        enableOrientation: true,
    
        viewport: {
            width: 1100,
            height: 300,
            type: 'square'
        },
    
        boundary: {
            width: 1100, 
            height: 300
        },
    })
    $('#imagem-crop').on('change', (event)=>{
        let reader = new FileReader()

        reader.onload = function(e){
            
            redimensionar.croppie('bind', {
                url: e.target.result
            })
        }
        
        reader.readAsDataURL(event.target.files[0])
    })
}

function remover_imagem(){
    limpar_croppie()

    if (render){
        create_element_add_salon()
    }else{
        if (reset){
            create_element_salon_with_reset()
        }else{
            create_element_edit_salon(imagem_atual)
        }   
    }

    renderizar_imagem()
}

function create_element_salon_with_reset(){
    let elemento = document.createElement('div')

    elemento.innerHTML = `
        <div class="mb-3">
            <h3>Trocar Imagem</h3>
            <p class="form-label">
                Lembre-se de que, caso não haja uma imagem disponível, utilizaremos uma imagem padrão.
            </p>
            <input class="form-control" type="file" accept="image/jpeg" name="image" id="imagem-crop">
        </div>
        <div id="preview"></div>
        <div class="d-grid gap-2 d-md-block text-center">
            <button type="button" class="btn btn-danger btn-lg" onclick="remover_imagem()">Remover imagem selecionada</button>

            <button type="button" class="btn btn-secondary btn-lg" onclick="redefinir_imagem()">Redefinir imagem</button>
        </div>
    `

    tempContent.appendChild(elemento)
}

function create_element_add_salon(){
    let elemento = document.createElement('div')

    elemento.innerHTML = `
        <div class="mb-3">
            <h3>Imagem</h3>
            <p class="form-label">
                Lembre-se de que, caso não haja uma imagem disponível, utilizaremos uma imagem padrão.
            </p>
            <input class="form-control" type="file" accept="image/jpeg" name="image" id="imagem-crop">
        </div>
        <div id="preview"></div>
        <div class="text-center">
            <button type="button" class="btn btn-danger btn-lg" onclick="remover_imagem()">Remover imagem selecionada</button>
        </div> 
    `

    tempContent.appendChild(elemento)
}

function create_element_edit_salon(imagem){
    let elemento = document.createElement('div')
    
    elemento.innerHTML = `
        <img src="${imagem}" alt="Imagem salão" id="view-image">
        <div class="text-center mt-3">
            <button type="button" class="btn btn-dark btn-lg" onclick="trocar_imagem()">Trocar imagem</button>
        </div>
    `

    tempContent.appendChild(elemento)
}

function trocar_imagem(){
    limpar_croppie()

    let elemento = document.createElement('div')

    elemento.innerHTML = `
        <div class="mb-3">
            <h3>Trocar Imagem</h3>
            <p class="form-label">
                Lembre-se de que, caso não haja uma imagem disponível, utilizaremos uma imagem padrão.
            </p>
            <input class="form-control" type="file" accept="image/jpeg" name="image" id="imagem-crop">
        </div>
        <div id="preview"></div>
        <div class="d-grid gap-2 d-md-block text-center">
            <button type="button" class="btn btn-danger btn-lg" onclick="remover_imagem()">Remover imagem selecionada</button>

            <button type="button" class="btn btn-secondary btn-lg" onclick="redefinir_imagem()">Redefinir imagem</button>
        </div>
    `

    reset = true
    tempContent.appendChild(elemento)

    renderizar_imagem()
}

function redefinir_imagem(){
    limpar_croppie()
    create_element_edit_salon(imagem_atual)
}

function limpar_croppie(){
    $('#imagem-crop').val('')
    
    if (redimensionar !== null){
        redimensionar.croppie('destroy')
    }

    redimensionar = null
    tempContent.innerHTML = ''
}
