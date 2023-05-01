let inputFile = document.getElementById('image')
let pictureImage = document.getElementById('imgs')

inputFile.addEventListener('change', function(e){
    let inputTarget = e.target
    let file = inputTarget.files[0]

    if (file){
        let reader = new FileReader()

        reader.addEventListener('load', function(e){
            let read = e.target
            let img = document.createElement('img')
            img.src = read.result
            img.classList.add('img_input')
            pictureImage.innerHTML = ''
            pictureImage.appendChild(img)
        })

        reader.readAsDataURL(file)
    }else{
        console.log('no')
    }
})