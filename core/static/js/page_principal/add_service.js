const addButton = document.getElementById('add-button');
const inputContainer = document.getElementById('input-container');

let inputCount = 0;

// Adicione um ouvinte de eventos de clique ao botão "mais"
addButton.addEventListener('click', (event) => {
    // Evite que o evento padrão seja executado
    event.preventDefault();
    
    // Crie uma nova div para o novo conjunto de campos de entrada
    const newDiv = document.createElement('div');
    
    newDiv.innerHTML = `
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <input type="text" class="form-control" id="input-${inputCount}" name="servicos[]" placeholder="Serviço" style="width: 15em">
            <button class="btn btn-danger remove-button"><i class="fas fa-times"></i> Remover serviço</button>
        </div>
    `;

    // Adicione um ouvinte de eventos de clique ao botão de remoção
    const removeButton = newDiv.querySelector('.remove-button');
    removeButton.addEventListener('click', () => {
        newDiv.remove();
    });
    
    inputContainer.appendChild(newDiv);
    
    inputCount++;
});