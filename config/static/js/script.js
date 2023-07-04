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
xhr.open('GET', '../static/sportsbetapp/sports.json', true);
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
    const encodedSport = encodeURIComponent(selectedSport);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/get_upcoming_games/${encodedSport}/`, true);
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4) {
        if (xhr.status === 200) {
          try {
            var games = JSON.parse(xhr.responseText);
            populateGamesList(games);
          } catch (error) {
            console.error('Error parsing JSON:', error);
          }
        } else {
          console.error(`Error with request: HTTP ${xhr.status}`);
        }
      }
    };
    xhr.send();
}

function populateGamesList(games) {
    var gamesList = document.getElementById('games-list');

    // Clear the list before populating
    gamesList.innerHTML = '';

    // Generate the HTML options
    games.forEach(function(game) {
        var a = document.createElement('a');
        a.href = '/game/' + game.id + '/';
        a.textContent = game.home_team + ' VS ' + game.away_team;
        var li = document.createElement('li');
        li.appendChild(a);
        gamesList.appendChild(li);
    });
}
  
  
  
  

