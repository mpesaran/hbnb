// Mock data for places
const places = [
  {
    id: 1,
    name: 'Cozy Cabin',
    description: 'A beautiful cabin in the mountains.',
    price: '$80/night',
    location: 'Aspen, CO',
    image: 'assets/cozy-cabin.jpg',
    amenities: ['Wi-Fi', 'Kitchen', 'Fireplace', 'Parking']
  },
  {
    id: 2,
    name: 'Beach Resort',
    description: 'A luxury resort by the beach.',
    price: '$150/night',
    location: 'Malibu, CA',
    image: 'assets/beach-resort.jpg',
    amenities: ['Pool', 'Wi-Fi', 'Beachfront', 'Gym']
  },
  {
    id: 3,
    name: 'City Apartment',
    description: 'Modern apartment in downtown New York.',
    price: '$250/night',
    location: 'New York, NY',
    image: 'assets/city-apartment.jpg',
    amenities: ['Wi-Fi', 'Air Conditioning', 'Gym', 'Elevator']
  }
];

// Display places dynamically
function displayPlaces(places) {
  const placesContainer = document.getElementById('places-container');
  placesContainer.innerHTML = '';  // Clear the container before appending new places

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';

    const amenitiesList = place.amenities.map(amenity => `<li>${amenity}</li>`).join('');

    card.innerHTML = `
      <img src="${place.image}" alt="${place.name}" class="place-img" />
      <h3>${place.name}</h3>
      <p>${place.description}</p>
      <p>${place.location}</p>
      <p><strong>${place.price}</strong></p>
      <ul class="amenities-list">
        ${amenitiesList}
      </ul>
      <button onclick="viewPlace(${place.id})">View Details</button>
    `;
    placesContainer.appendChild(card);
  });
}

// Filter places by price
document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;
  const filteredPlaces = places.filter(place => {
    if (selectedPrice === 'All') return true;
    const price = parseInt(place.price.replace('$', '').replace('/night', '').trim());
    return selectedPrice === 'Under $150' ? price <= 150 : price > 150;
  });
  displayPlaces(filteredPlaces);
});

// Function to check authentication
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';  // Show login link if not authenticated
  } else {
    loginLink.style.display = 'none';  // Hide login link if authenticated
  }

  return token;
}

// Helper function to get a cookie by name
function getCookie(name) {
  const cookies = document.cookie.split('; ');
  const cookie = cookies.find(row => row.startsWith(name));
  return cookie ? cookie.split('=')[1] : null;
}

// Fetch places from API (example API request)
async function fetchPlaces() {
  const token = checkAuthentication();
  const response = await fetch('https://api.example.com/places', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (response.ok) {
    const placesData = await response.json();
    displayPlaces(placesData);  // Display fetched places
  } else {
    console.error('Failed to fetch places');
  }
}

// Display details of a place (for example, on a new page)
function viewPlace(placeId) {
  window.location.href = `place.html?id=${placeId}`;  // Redirect to the place detail page
}

// Review submission for a place
document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication();
  const placeId = getPlaceIdFromURL();

  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review-text').value;
      
      // Send review to the API
      const response = await submitReview(token, placeId, reviewText);

      if (response.ok) {
        alert('Review submitted successfully!');
        reviewForm.reset(); // Clear the form
      } else {
        alert('Failed to submit review');
      }
    });
  }
});

// Submit review data to the API
async function submitReview(token, placeId, reviewText) {
  const response = await fetch('https://api.example.com/reviews', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      place_id: placeId,
      review_text: reviewText
    })
  });
  return response;
}

// Get place ID from URL (for viewing or adding a review)
function getPlaceIdFromURL() {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get('id');
}

// Initial page setup - Check authentication and fetch places
checkAuthentication();
displayPlaces(places);  // Display places on the home page
