document.getElementById("submit-file").addEventListener("submit", async (e) => {
    e.preventDefault()
    try{

    }
    catch(err){
        console.log(err.message)
    }
})

// fetch("https://pokeapi.co/api/v2/pokemon/ditto")
//     .then(Response => Response.json())
//     .then(data => console.log(data.abilities))
//     .catch(error => console.error(error))