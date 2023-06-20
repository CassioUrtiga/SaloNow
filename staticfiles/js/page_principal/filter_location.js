window.addEventListener('load', ()=>{

    let cidade = document.querySelector('#localidade').textContent.split(',')[0].trim().toUpperCase()
    let pai = document.querySelector('main');
    let div_saloes = document.querySelectorAll('.div-salao')

    let divsPrimarias = []
    let divsSecundarias = []

    div_saloes.forEach((div)=>{
        if (div.querySelector('.organiza p').textContent.split(',')[0].trim().toUpperCase() === cidade){
            divsPrimarias.push(div)
        }else{
            divsSecundarias.push(div)
        }
    })

    if (divsPrimarias.length !== 0){
        pai.innerHTML = ''
        let fragment = document.createDocumentFragment()

        divsPrimarias.concat(divsSecundarias).forEach((div)=>{
            fragment.appendChild(div)
        })

        pai.appendChild(fragment)
    }
})
