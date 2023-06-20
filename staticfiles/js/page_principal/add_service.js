let addButton = document.getElementById('add-button')
let inputContainer = document.getElementById('input-container')

addButton.addEventListener('click', (event) => {
    event.preventDefault()

    var prox = addButton.nextElementSibling
    prox.style.display = 'block'
    
    let newRow = document.createElement('tr')
    
    newRow.innerHTML = `
        <tr>
            <td>
                <input type="text" class="form-control" name="servicos[]" placeholder="Serviço" oninput="event_input_void(event)" />
            </td>
            <td>
                <input type="number" class="form-control" step="0.01" min="0.00" name="precos[]" placeholder="Preço" required disabled oninput="validity.valid||(value='');" />
            </td>
            <td>
                <input type="time" class="form-control" name="duracao_homem[]"  value="00:00:00" required disabled />
            </td>
            <td>
                <input type="time" class="form-control" name="duracao_mulher[]"  value="00:00:00" required disabled />
            </td>
            <td>
                <button class="btn btn-danger remove-button"><i class="fas fa-times"></i> Remover serviço</button>
            </td>
        </tr>
    `

    let removeButton = newRow.querySelector('.remove-button')
    removeButton.addEventListener('click', () => {
        newRow.remove()
        if (inputContainer.querySelectorAll('tr').length === 0) {
            prox.style.display = 'none'
        }
    })
    
    inputContainer.appendChild(newRow)
})

function event_input_void(event){
    let inputPreco = event.target.parentElement.nextElementSibling.querySelector('input[type=number]')
    let inputDuracaoHomem = event.target.parentElement.nextElementSibling.nextElementSibling.querySelector('input[type=time]')
    let inputDuracaoMulher = event.target.parentElement.nextElementSibling.nextElementSibling.nextElementSibling.querySelector('input[type=time]')

    if (event.target.value.trim() === '') {
        inputPreco.disabled = true
        inputPreco.value = ''
        inputDuracaoHomem.disabled = true
        inputDuracaoMulher.disabled = true
        inputDuracaoHomem.value = '00:00:00'
        inputDuracaoMulher.value = '00:00:00'
    } else {
        inputPreco.disabled = false
        inputDuracaoHomem.disabled = false
        inputDuracaoMulher.disabled = false
    }
}
