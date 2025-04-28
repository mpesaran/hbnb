document.addEventListener('DOMContentLoaded', () => {
  // --- Home Page: Display places ---
  const placesContainer = document.getElementById('places-container');

  if (placesContainer) {
    const places = [
      {
        name: 'Cozy Cabin',
        price: '$80/night',
        location: 'Aspen, CO',
        image: 'assets/Cozy Cabin.jpg'
      },
      {
        name: 'Beach Resort',
        price: '$150/night',
        location: 'Malibu, CA',
        image: 'assets/Beach resort.jpg'
      },
      {
        name: 'City Apartment',
        price: '$250/night',
        location: 'New York, NY',
        image: 'assets/City Apartment.jpg'
      }
    ];

    function displayPlaces(data) {
      placesContainer.innerHTML = '<p class="loading">Loading places...</p>';

      setTimeout(() => {
        placesContainer.innerHTML = '';
        data.forEach(place => {
          const card = document.createElement('div');
          card.className = 'place-card';
          card.innerHTML = `
            <img src="${place.image}" alt="${place.name}" class="place-img" />
            <h3>${place.name}</h3>
            <p>${place.location}</p>
            <p><strong>${place.price}</strong></p>
          `;
          placesContainer.appendChild(card);
        });
      }, 1000); // Simulate 1s loading
    }

    displayPlaces(places);

    const filterBtn = document.getElementById('filterBtn');
    if (filterBtn) {
      filterBtn.addEventListener('click', () => {
        const searchVal = document.getElementById('search').value.toLowerCase();
        const filtered = places.filter(place =>
          place.name.toLowerCase().includes(searchVal) ||
          place.location.toLowerCase().includes(searchVal)
        );
        displayPlaces(filtered);
      });
    }
  }

  // --- Login Page: Handle login form ---
  const loginForm = document.getElementById('loginForm');

  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      const loginError = document.getElementById('loginError');

      if (email === 'test@example.com' && password === '123') {
        window.location.href = 'index.html';
      } else {
        loginError.textContent = 'Invalid credentials';
        clearMessage(loginError);
      }
    });
  }

  // --- Add Review Page: Handle review form ---
  const reviewForm = document.getElementById('reviewForm');

  if (reviewForm) {
    reviewForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const name = document.getElementById('reviewerName').value;
      const text = document.getElementById('reviewText').value;
      const rating = document.getElementById('rating').value;
      const reviewMsg = document.getElementById('reviewMsg');

      if (name && text && rating) {
        reviewMsg.textContent = 'Review submitted!';
        reviewForm.reset();
      } else {
        reviewMsg.textContent = 'Please complete all fields.';
      }
      clearMessage(reviewMsg);
    });
  }

  // --- Helper: Clear a message after 3 seconds ---
  function clearMessage(element) {
    setTimeout(() => {
      element.textContent = '';
    }, 3000);
  }
});