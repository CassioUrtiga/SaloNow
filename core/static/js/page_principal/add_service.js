let addButton = document.getElementById('add-button')
let inputContainer = document.getElementById('input-container')

addButton.addEventListener('click', (event) => {
    event.preventDefault()
    
    let newRow = document.createElement('tr')
    
    newRow.innerHTML = `
        <tr>
            <td>
                <input type="text" class="form-control" name="servicos[]" placeholder="Serviço" oninput="event_input_void(event)" />
            </td>
            <td>
                <input type="number" class="form-control" step="0.01" name="precos[]" placeholder="Preço" required disabled />
            </td>
            <td>
                <button class="btn btn-danger remove-button"><i class="fas fa-times"></i> Remover serviço</button>
            </td>
        </tr>
    `

    let removeButton = newRow.querySelector('.remove-button')
    removeButton.addEventListener('click', () => {
        newRow.remove()
    })
    
    inputContainer.appendChild(newRow)
})

function event_input_void(event){
    let inputPreco = event.target.parentElement.nextElementSibling.querySelector('input[type=number]')

    if (event.target.value.trim() === '') {
        inputPreco.disabled = true
        inputPreco.value = ''
    } else {
        inputPreco.disabled = false
    }
}
