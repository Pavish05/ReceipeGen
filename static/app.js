let foodApi = "https://api.spoonacular.com/recipes/autocomplete";
const apiKey = "4c38af58cbe74ecfac48f137ccfef40b"; // for now i will leave this here but i need to change this!

const searchBar = document.querySelector('#search');
//list should be the api
// Create a search function that takes the input and list of fruits
function search(input, list) {
    input.addEventListener('input', myDebounce(function() {
        let params = {
            number:5,
            apiKey:apiKey,
            query:input.value
        }

        // Close list if it existed before this...
        closeList();

        // If no input then do nothing
        if (!input.value) return;

        // Create a suggestions <div> and add it to the element containing the input field
        makeContainer();

        // Iterate through entire list and find matches
        getData(list, params)
        .then(data => {
            for (let index of data) {
                if (index.title.toLowerCase().includes(input.value.toLowerCase())) {
                    createSuggestion(index.title);
                }
            }
        })
        .catch(err=>console.log(err))
    }, 300));
}

async function getData(url, params) {
    let data = await $.getJSON(`${url}`, params);
    return data;
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
    suggestion.setAttribute('id', 'choices');
    suggestion.style.cursor = 'pointer';

    // add a listener for user mouse click on suggestion to fill in the input with suggestion and close list
    suggestion.addEventListener('click', function(e) {
        searchBar.value = e.target.innerHTML;
        closeList();
    });
    document.querySelector('#suggestions').append(suggestion);
}

//debounce/wait to call function over several inputs
const myDebounce = (func, wait) => {
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