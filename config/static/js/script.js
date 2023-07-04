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
            
            // Get the games list element
            var gamesList = document.getElementById('games-list');
            gamesList.innerHTML = ''; // Clear the current games list
            
            if (games.length === 0) {
              var listItem = document.createElement('li');
              listItem.textContent = 'No upcoming games.';
              gamesList.appendChild(listItem);
            } else {
                for (var i = 0; i < games.length; i++) {
                    var listItem = document.createElement('li');
                    listItem.textContent = games[i].home_team + ' vs. ' + games[i].away_team + ' at ' + games[i].commence_time;
                    console.log('Adding game:', listItem.textContent);
                    gamesList.appendChild(listItem);
                }
            }
            
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
  
  
  
  

