// function takes array data and for each item, appends an li to the ul 
function listCupcakes(cupcakes) {
    for (let c of cupcakes) {
        console.log(c)
        $("ul").append(`<li>${c.flavor}</li>`)
    }
}

// get list of cupcake data via axios, passes array of cupcakes to listCupcakes function
async function getCupcakes() {
    let response = await axios.get('/api/cupcakes')
    console.log(response.data.cupcakes)
    listCupcakes(response.data.cupcakes)
}

$(function(){getCupcakes()})

// post new cupcake to database
async function addCupcake(cupcake) {
    let response = await axios.post('/api/cupcakes', cupcake)
    $('ul').empty()
    getCupcakes()
}

$('.add-cupcake').click(function(event){
    event.preventDefault();
    flavor = $('#flavor').val()
    size = $('#size').val()
    rating = $('#rating').val()
    image = $('#image').val()

    cupcake = {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    }
    console.log(JSON.stringify(cupcake))
    addCupcake(cupcake)
})