function initializeDatePickers() {
    // Retrieve the start date and end date input elements
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
}

// Event listener for the 'sport' dropdown menu on home.html
document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('sport-dropdown').addEventListener('change', function() {
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        onSportSelection(this.value, startDate, endDate);
    });

document.getElementById('start-date').addEventListener('change', fetchSportsData);
document.getElementById('end-date').addEventListener('change', fetchSportsData);
    

// Call the initializeDatePickers function when the page has finished loading
window.addEventListener('load', function() {
    initializeDatePickers();
    // Load the sports data from the new endpoint
    fetchSportsData();
});

function fetchSportsData() {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/sports_with_games/?start_date=${startDate}&end_date=${endDate}`, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            var sportsData = JSON.parse(xhr.responseText);
            populateSportDropdown(sportsData);
        }
    };
    xhr.send();
}

function populateSportDropdown(sportsData) {
    var dropdown = document.getElementById('sport-dropdown');
    var startDate = document.getElementById('start-date').value;
    var endDate = document.getElementById('end-date').value;

    // Filter the sports data based on the 'active' field
    var activeSports = sportsData.filter(sport => sport.is_active);

    dropdown.innerHTML = "";

    // Generate the HTML options
    activeSports.forEach(function(sport) {
        var option = document.createElement('option');
        option.value = sport.key;
        option.textContent = sport.title;
        dropdown.appendChild(option);
    });
}

function onSportSelection(selectedSport, startDate, endDate) {
    const encodedSport = encodeURIComponent(selectedSport);
    const encodedStartDate = encodeURIComponent(startDate);
    const encodedEndDate = encodeURIComponent(endDate);
    const xhr = new XMLHttpRequest();
    xhr.open('GET', `/get_upcoming_games/${encodedSport}?start_date=${encodedStartDate}&end_date=${encodedEndDate}`, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                try {
                    const games = JSON.parse(xhr.responseText);
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

  

  
  

