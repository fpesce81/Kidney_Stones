// State
let currentLanguage = 'en';
let translations = {};
let foodOxalateData = [];

// DOM elements
const foodSearchInput = document.getElementById('foodSearchInput');
const searchButton = document.getElementById('searchButton');
const resultsDiv = document.getElementById('results');
const langEnButton = document.getElementById('lang-en');
const langItButton = document.getElementById('lang-it');
const sortInputs = document.querySelectorAll('input[name="sort"]');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    setLanguage(currentLanguage);
});

searchButton.addEventListener('click', performSearch);
foodSearchInput.addEventListener('keypress', function (event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // prevent form submission
        performSearch();
    }
});
foodSearchInput.addEventListener('input', handleAutocomplete);

langEnButton.addEventListener('click', () => setLanguage('en'));
langItButton.addEventListener('click', () => setLanguage('it'));

sortInputs.forEach(input => {
    input.addEventListener('change', () => performSearch(true));
});

/**
 * Fetches the language JSON file and initializes the application.
 * @param {string} lang - The language to set (e.g., 'en', 'it').
 */
async function setLanguage(lang) {
    currentLanguage = lang;
    try {
        const response = await fetch(`locales/${lang}.json`);
        translations = await response.json();
        foodOxalateData = translations.food_data;
        updateUI();
        updateFlagSelection();
        performSearch(true); // Re-run search with current input, if any
    } catch (error) {
        console.error('Could not load language file:', error);
    }
}

/**
 * Updates the UI with the loaded translations.
 */
function updateUI() {
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[key]) {
            element.textContent = translations[key];
        }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[key]) {
            element.placeholder = translations[key];
        }
    });
}

/**
 * Updates the visual selection of the language flags.
 */
function updateFlagSelection() {
    if (currentLanguage === 'en') {
        langEnButton.classList.add('active');
        langItButton.classList.remove('active');
    } else {
        langItButton.classList.add('active');
        langEnButton.classList.remove('active');
    }
}

/**
 * Performs the search for food oxalate content based on user input.
 * @param {boolean} isLanguageChange - Flag to indicate if the search is triggered by a language change.
 */
function performSearch(isLanguageChange = false) {
    const searchTerm = foodSearchInput.value.toLowerCase().trim();
    closeAutocomplete();
    resultsDiv.innerHTML = ''; // Clear previous results

    if (searchTerm === '') {
        resultsDiv.innerHTML = `<h3 data-i18n="results_heading">${translations.results_heading}</h3><p data-i18n="results_prompt">${translations.results_prompt}</p>`;
        return;
    }

    let filteredFoods = foodOxalateData.filter(food =>
        food.food.toLowerCase().includes(searchTerm) ||
        food.type.toLowerCase().includes(searchTerm)
    );

    // Fuzzy search if no results
    if (filteredFoods.length === 0) {
        filteredFoods = foodOxalateData.filter(food =>
            levenshtein(food.food.toLowerCase(), searchTerm) <= 2 ||
            levenshtein(food.type.toLowerCase(), searchTerm) <= 2
        );
    }

    displayResults(filteredFoods);
}

/**
 * Displays the search results in the resultsDiv.
 * @param {Array<Object>} foods - An array of food objects to display.
 */
function displayResults(foods) {
    const sortValue = document.querySelector('input[name="sort"]:checked').value;

    if (sortValue === 'asc') {
        foods.sort((a, b) => a.oxalate_mg - b.oxalate_mg);
    } else if (sortValue === 'desc') {
        foods.sort((a, b) => b.oxalate_mg - a.oxalate_mg);
    }
    // No action for 'default' to keep original order

    if (foods.length === 0) {
        resultsDiv.innerHTML = `<h3 data-i18n="results_heading">${translations.results_heading}</h3><p>${translations.no_results} "${foodSearchInput.value}".</p>`;
        return;
    }

    let resultsHtml = `<h3 data-i18n="results_for">${translations.results_for} "${foodSearchInput.value}"</h3>`;
    foods.forEach(food => {
        const oxalateCategory = getOxalateCategory(food.oxalate_mg);
        resultsHtml += `
            <div class="food-item">
                <strong>${food.food}</strong> (${food.type}): ${food.oxalate_mg} mg
                <span class="oxalate-category category-${oxalateCategory.key.replace('_', '-')}">${translations[oxalateCategory.key]}</span>
            </div>
        `;
    });
    resultsDiv.innerHTML = resultsHtml;
}

/**
 * Calculates the Levenshtein distance between two strings.
 * @param {string} a - The first string.
 * @param {string} b - The second string.
 * @returns {number} The Levenshtein distance.
 */
function levenshtein(a, b) {
    const an = a ? a.length : 0;
    const bn = b ? b.length : 0;
    if (an === 0) {
        return bn;
    }
    if (bn === 0) {
        return an;
    }
    const matrix = new Array(bn + 1);
    for (let i = 0; i <= bn; ++i) {
        matrix[i] = new Array(an + 1);
    }
    for (let i = 0; i <= bn; ++i) {
        matrix[i][0] = i;
    }
    for (let j = 0; j <= an; ++j) {
        matrix[0][j] = j;
    }
    for (let i = 1; i <= bn; ++i) {
        for (let j = 1; j <= an; ++j) {
            const cost = a[j - 1] === b[i - 1] ? 0 : 1;
            matrix[i][j] = Math.min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            );
        }
    }
    return matrix[bn][an];
}

/**
 * Handles the autocomplete suggestions.
 */
function handleAutocomplete() {
    const val = foodSearchInput.value;
    closeAutocomplete();
    if (!val) { return false; }

    const suggestions = document.createElement('div');
    suggestions.setAttribute('id', 'autocomplete-list');
    suggestions.setAttribute('class', 'autocomplete-items');
    foodSearchInput.parentNode.appendChild(suggestions);

    const matchingFoods = foodOxalateData.filter(food =>
        food.food.toLowerCase().includes(val.toLowerCase()) ||
        food.type.toLowerCase().includes(val.toLowerCase())
    ).slice(0, 5);

    matchingFoods.forEach(food => {
        const suggestionItem = document.createElement('div');
        suggestionItem.innerHTML = `<strong>${food.food.substr(0, val.length)}</strong>`;
        suggestionItem.innerHTML += food.food.substr(val.length);
        suggestionItem.innerHTML += ` <span style="color: grey; font-size: 0.8em;">(${food.type})</span>`;
        suggestionItem.addEventListener('click', function () {
            foodSearchInput.value = food.food;
            closeAutocomplete();
            performSearch();
        });
        suggestions.appendChild(suggestionItem);
    });
}

/**
 * Closes the autocomplete list.
 */
function closeAutocomplete() {
    const x = document.getElementById('autocomplete-list');
    if (x) {
        x.parentNode.removeChild(x);
    }
}

/**
 * Determines the oxalate category based on the oxalate content.
 * @param {number} oxalateMg - The oxalate content in milligrams.
 * @returns {Object} An object containing the category key and display name.
 */
function getOxalateCategory(oxalateMg) {
    if (oxalateMg > 100) {
        return { key: "very_high" };
    } else if (oxalateMg >= 50) {
        return { key: "high" };
    } else if (oxalateMg >= 20) {
        return { key: "moderate" };
    } else if (oxalateMg >= 10) {
        return { key: "low" };
    } else {
        return { key: "very_low" };
    }
}

// Initial display or instructions
resultsDiv.innerHTML = '<h3>Search Results</h3><p>Enter a food name above to see its oxalate content.</p>';
