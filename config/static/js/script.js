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
  document.getElementById('sport-select').addEventListener('change', function(event) {
    const selectedSport = event.target.value;
    // Perform the filtering based on the selected sport
    // Call a function or update the game list accordingly
  });
  
  // Call the initializeDatePickers function when the page has finished loading
  window.addEventListener('load', function() {
    initializeDatePickers();
  });

  // Load the sports.json file
var xhr = new XMLHttpRequest();
xhr.open('GET', 'sports.json', true);
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
    // Make an AJAX request to retrieve the upcoming games based on the selected sport
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/get_upcoming_games/' + selectedSport, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            // Handle the response from the server if needed
        }
    };
    xhr.send();
}