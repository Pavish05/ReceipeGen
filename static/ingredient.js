let ingredientApi = "https://api.spoonacular.com/food/ingredients/autocomplete";
//const apiKey = "4c38af58cbe74ecfac48f137ccfef40b"; // for now i will leave this here but i need to change this!

const ingredientBar = document.querySelector('#title');
//list should be the api
// Create a search function that takes the input and list of fruits
function searchIngredient(input, list) {
    input.addEventListener('input', myOtherDebounce(function() {
        let params = {
            number:10,
            apiKey:apiKey,
            query:input.value
        }

        // Close list if it existed before this...
        closeIngredientList();

        // If no input then do nothing
        if (!input.value) return;

        // Create a suggestions <div> and add it to the element containing the input field
        makeIngredientContainer();

        // Iterate through entire list and find matches
        getIngredientData(list, params)
        .then(data => {
            for (let index of data) {
                if (index.name.toLowerCase().includes(input.value.toLowerCase())) {
                    createIngredientSuggestion(index.name);
                }
            }
        })
        .catch(err=>console.log(err))
    }, 300));
}

async function getIngredientData(url, params) {
    let data = await $.getJSON(`${url}`, params);
    return data;
}

//Remove the suggestionsContainer
function closeIngredientList() {
    let suggestions = document.getElementById('ingredientSuggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

//creates a container that holds the autosuggestions
function makeIngredientContainer() {
    const suggestionContainer = document.createElement('div');
    suggestionContainer.setAttribute('id', 'ingredientSuggestions');
    document.querySelector('.ingredient-form').append(suggestionContainer);
}

//Create the autocomplete suggestions using ul and append them under the searchBar
function createIngredientSuggestion(index) {
    //If a match is found create a suggestion <ul> and add it to suggestionContainer
    let suggestion = document.createElement('ul');
    suggestion.innerHTML = index;
    suggestion.setAttribute('id', 'choices');
    suggestion.style.cursor = 'pointer';

    // add a listener for user mouse click on suggestion to fill in the input with suggestion and close list
    suggestion.addEventListener('click', function(e) {
        ingredientBar.value = e.target.innerHTML;
        closeIngredientList();
    });
    document.querySelector('#ingredientSuggestions').append(suggestion);
}

//debounce/wait to call function over several inputs
const myOtherDebounce = (func, wait) => {
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

searchIngredient(ingredientBar, ingredientApi)