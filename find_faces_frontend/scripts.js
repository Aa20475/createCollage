
const url = 'http://127.0.0.1:5000/createCollage'
const form = document.querySelector('form')
const app = document.getElementById('root')
const inp_loc = document.getElementById('imgs')

form.addEventListener('submit', e => {
  e.preventDefault()


  const files = document.querySelector('[type=file]').files
  const formData = new FormData()
  for(let i=0;i<files.length;i++){
	formData.append("files",files[i])
  }
  console.log(formData.getAll("files"))
  
  if(document.getElementById("Rcd")){
					app.removeChild(document.getElementById("Rcd"))
					app.removeChild(document.getElementById("rcd_img"))
  }
  if(document.getElementById("snd")){
	  app.removeChild(document.getElementById("snd"))
	  app.removeChild(document.getElementById("snd_img"))
  }  
  const g = document.createElement("h1")
  g.textContent = "Sent:"
  g.id = "snd"
  //app.appendChild(g)

  const image1 = document.createElement("img")
  image1.src = files[0]
  image1.id = "snd_img"
  //app.appendChild(image1)

  fetch(url, {

    method: 'POST',
    headers:{
      "Access-Control-Allow-Origin" :"http://127.0.0.1:5000"
    }, 
    body: formData,
	//mode: "no-cors"
  }).then(response => response.blob())
            .then(blob => {
                const h = document.createElement("h1")
				h.textContent = "Received:"
				h.id = "Rcd"
				app.appendChild(h)

				const image = document.createElement("img")
				image.src = URL.createObjectURL(blob)
				image.id = "rcd_img"
				app.appendChild(image)}
            )
})


function readURL(input) {
	const br = document.createElement('br')
	var paras = document.getElementsByClassName('pre');

	while(paras[0]){
		paras[0].parentNode.removeChild(paras[0]);}



    if (input.files && input.files[0]) {
        for(let i=0;i<input.files.length;i++){
			
			var reader = new FileReader();
			const im = document.createElement('img')
			reader.onload = function (e) {
				im.src =  e.target.result;
				im.className = 'pre'
			};

			reader.readAsDataURL(input.files[i]);
			
			inp_loc.appendChild(im)
			inp_loc.appendChild(br)

		}
    }
}