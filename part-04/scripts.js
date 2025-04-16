// Get cookie value by name
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Extract place ID from URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// Handle login from submission
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          const email = document.getElementById('email').value;
          const password = document.getElementById('password').value;
          await loginUser(email, password);
      });
  }
  const reviewForm = document.getElementById('review-form');
  const placeId = getPlaceIdFromURL();
  const token = checkAuthentication();
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const reviewText = document.getElementById('review-text').value;
      await submitReview(token, placeId, reviewText);
    })
  }
  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
      const selectedPrice = event.target.value;
      const places = document.querySelectorAll('.place');
      places.forEach(place => {
        const price = parseFloat(place.getAttribute('data-price'));
        place.style.display = (!selectedPrice || price <= selectedPrice) ? 'block' : 'none';
      });
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
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    alert('Login failed: ' + response.statusText);
  }
}

function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  const addReviewSection = document.getElementById('add-review');

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }
  if (!token && window.location.pathname.includes('place.html')) {
    window.location.href = 'index.html';
  }
  return token;
}

async function fetchPlaces(token) {
  const response = await fetch('https://your-api-url/places', {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (response.ok) {
    const places = await response.json();
    displayPlaces(places);
  } else {
    alert('Failed to fetch places');
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';
  places.forEach(place => {
    const placeDiv = document.createElement('div');
    placeDiv.className = 'place';
    placeDiv.setAttribute('data-price', place.price);
    placeDiv.innerHTML = `
      <h3>${place.name}</h3>
      <p>${place.description}</p>
      <p>Location: ${place.location}</p>
      <p>Price: $${place.price}</p>
    `;
    placesList.appendChild(placeDiv);
  });
}

async function fetchPlaceDetails(token, placeId) {
  const response = await fetch(`https://your-api-url/places/${placeId}`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (response.ok) {
    const place = await response.json();
    displayPlaceDetails(place);
  } else {
    alert('Failed to fetch place details');
  }
}

function displayPlaceDetails(place) {
  const detailsSection = document.getElementById('place-details');
  detailsSection.innerHTML = `
    <h2>${place.name}</h2>
    <p>${place.description}</p>
    <p>Price: $${place.price}</p>
    <h4>Amenities:</h4>
    <ul>${place.amenities.map(amenity => `<li>${amenity}</li>`).join('')}</ul>
    <h4>Reviews:</h4>
    <ul>${place.reviews.map(review => `<li>${review.user_name}: ${review.text}</li>`).join('')}</ul>
  `;
}

async function submitReview(token, placeId, reviewText) {
  const response = await fetch('https://your-api-url/reviews', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ place_id: placeId, text: reviewText })
  });

  if (response.ok) {
      alert('Review submitted successfully!');
      document.getElementById('review-text').value = '';
  } else {
      alert('Failed to submit review');
  }
}