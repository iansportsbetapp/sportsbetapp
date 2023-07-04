// Add this script at the end of your HTML body or in a separate JavaScript file

// Function to initialize the date pickers
function initializeDatePickers() {
    // Retrieve the start date and end date input elements
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
  
    // Initialize the date picker widgets using a library like jQuery UI
    // Replace the datepicker initialization code with the one suitable for your date picker library
    $(startDateInput).datepicker();
    $(endDateInput).datepicker();
  }
  
  // Add an event listener to the sport select dropdown
  document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('sport-dropdown').addEventListener('change', function() {
        onSportSelection(this.value);
    });
});
  
  // Call the initializeDatePickers function when the page has finished loading
  window.addEventListener('load', function() {
    initializeDatePickers();
  });

  // Load the sports.json file
var xhr = new XMLHttpRequest();
xhr.open('GET', '/Users/ian/sportsbetapp/config/api/sports.json', true);
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var sportsData = JSON.parse(xhr.responseText);
        populateSportDropdown(sportsData);
    }
};
xhr.send();

function populateSportDropdown(sportsData) {
    var dropdown = document.getElementById('sport-dropdown');

    // Filter the sports data based on the 'active' field
    var activeSports = sportsData.filter(function(sport) {
        return sport.active === true;
    });

    // Generate the HTML options
    activeSports.forEach(function(sport) {
        var option = document.createElement('option');
        option.value = sport.key;
        option.textContent = sport.description;
        dropdown.appendChild(option);
    });
}

function onSportSelection(selectedSport) {
    // URL encode the selectedSport value
    selectedSport = encodeURIComponent(selectedSport);

    // Make an AJAX request to retrieve the upcoming games based on the selected sport
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_upcoming_games/' + selectedSport, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var games = JSON.parse(xhr.responseText);
            var gamesList = document.getElementById('games-list');
            gamesList.innerHTML = '';
            if (games.length === 0) {
                var listItem = document.createElement('li');
                listItem.textContent = 'No upcoming games.';
                gamesList.appendChild(listItem);
            } else {
                for (var i = 0; i < games.length; i++) {
                    var listItem = document.createElement('li');
                    listItem.textContent = games[i].home_team;
                    gamesList.appendChild(listItem);
                }
            }
        }
    };
    xhr.send();
}