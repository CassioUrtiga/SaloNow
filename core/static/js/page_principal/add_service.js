const addButton = document.getElementById('add-button');
const inputContainer = document.getElementById('input-container');

addButton.addEventListener('click', (event) => {
    // Evite que o evento padrão seja executado
    event.preventDefault()
    
    // Crie uma nova linha para o novo conjunto de campos de entrada
    const newRow = document.createElement('tr')
    
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
    `;

    const removeButton = newRow.querySelector('.remove-button')
    removeButton.addEventListener('click', () => {
        newRow.remove()
    });
    
    inputContainer.appendChild(newRow)
});

function event_input_void(event){
    let inputPreco = event.target.parentElement.nextElementSibling.querySelector('input[type=number]');

    if (event.target.value.trim() === '') {
        inputPreco.disabled = true
        inputPreco.value = ''
    } else {
        inputPreco.disabled = false
    }
}