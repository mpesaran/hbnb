document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          // Your code to handle form submission
      });
  }
});

async function loginUser(email, password) {
  const response = await fetch('https://your-api-url/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
  });
  // Handle the response
}

if (response.ok) {
  const data = await response.json();
  document.cookie = `token=${data.access_token}; path=/`;
  window.location.href = 'index.html';
} else {
  alert('Login failed: ' + response.statusText);
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
      loginLink.style.display = 'block';
  } else {
      loginLink.style.display = 'none';
      // Fetch places data if the user is authenticated
      fetchPlaces(token);
  }
}
function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
}

async function fetchPlaces(token) {
  // Make a GET request to fetch places data
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaces function
}

function displayPlaces(places) {
  // Clear the current content of the places list
  // Iterate over the places data
  // For each place, create a div element and set its content
  // Append the created element to the places list
}

document.getElementById('price-filter').addEventListener('change', (event) => {
  // Get the selected price value
  // Iterate over the places and show/hide them based on the selected price
});

function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  // Your code here
}

function checkAuthentication() {
  const token = getCookie('token');
  const addReviewSection = document.getElementById('add-review');

  if (!token) {
      addReviewSection.style.display = 'none';
  } else {
      addReviewSection.style.display = 'block';
      // Store the token for later use
      fetchPlaceDetails(token, placeId);
  }
}

function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
}

async function fetchPlaceDetails(token, placeId) {
  // Make a GET request to fetch place details
  // Include the token in the Authorization header
  // Handle the response and pass the data to displayPlaceDetails function
}

function displayPlaceDetails(place) {
  // Clear the current content of the place details section
  // Create elements to display the place details (name, description, price, amenities and reviews)
  // Append the created elements to the place details section
}

function checkAuthentication() {
  const token = getCookie('token');
  if (!token) {
      window.location.href = 'index.html';
  }
  return token;
}

function getCookie(name) {
  // Function to get a cookie value by its name
  // Your code here
}

function getPlaceIdFromURL() {
  // Extract the place ID from window.location.search
  // Your code here
}

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          // Get review text from form
          // Make AJAX request to submit review
          // Handle the response
      });
  }
});

async function submitReview(token, placeId, reviewText) {
  // Make a POST request to submit review data
  // Include the token in the Authorization header
  // Send placeId and reviewText in the request body
  // Handle the response
}

function handleResponse(response) {
  if (response.ok) {
      alert('Review submitted successfully!');
      // Clear the form
  } else {
      alert('Failed to submit review');
  }
}