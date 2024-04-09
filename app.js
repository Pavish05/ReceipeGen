let foodApi = "https://api.spoonacular.com/recipes/autocomplete"
const key = "4c38af58cbe74ecfac48f137ccfef40b" // for now i will leave this here but i need to change this!

// let data = await $.getJSON(`${foodApi}?number5&apiKey=${key}&query=${input}`) //i think i need to somehow include my api key.

const searchBar = document.querySelector('#search')
//list should be the api
// Create a search function that takes the input and list of fruits
async function search(input, list) {
    let data = await $.getJSON(`${list}?number=5&apiKey=${key}&query=${input}`)
    input.addEventListener('input', debounce(function() {
        // Close list if it existed before this...
        closeList();
        console.log("doing something")
        // If no input then do nothing
        if (!input.value) return;

        // Create a suggestions <div> and add it to the element containing the input field
        makeContainer();
        
        // Iterate through entire list and find matches
        for (let index of data) {
            if (index.toLowerCase().inclueds(input.value.toLowerCase())) {
                createSuggestion(index);
            }
        }
    }, 300));
}

//Remove the suggestionsContainer
function closeList() {
    let suggestions = document.getElementById('suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

//creates a container that holds the autosuggestions
function makeContainer() {
    const suggestionContainer = document.createElement('div');
    suggestionContainer.setAttribute('id', 'suggestions');
    document.querySelector('.navbar-form').append(suggestionContainer);
}

//Create the autocomplete suggestions using ul and append them under the searchBar
function createSuggestion(index) {
    //If a match is found create a suggestion <ul> and add it to suggestionContainer
    let suggestion = document.createElement('ul');
    suggestion.innerHTML = index;
    suggestion.style.cursor = 'pointer';

    // add a listener for user mouse click on suggestion to fill in the input with suggestion and close list
    suggestion.addEventListener('click', function(e) {
        searchBar.value = e.target.innerHTML;
        closeList();
    });
    document.querySelector('#suggestions').append(suggestion);
}

//debounce/wait to call function over several inputs
const debounce = (func, wait) => {
    let timer = null;
    return function (...args) {
        if (timer) {
            clearTimeout(timer);
            timer = null;
        }
        timer = setTimeout(() => {
            func.apply(this, args);
            timer = null;
        }, wait);
    }
}

search(searchBar, foodApi)