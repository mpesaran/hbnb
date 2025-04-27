// scripts/scripts.js

const API_BASE_URL = "http://localhost:5000/api/v1";  // <-- Update if different

// ---------- Authentication ----------
async function login(event) {
  event.preventDefault();

  const email = document.getElementById("email")?.value.trim();
  const password = document.getElementById("password")?.value.trim();
  const errorMsg = document.getElementById("loginError");

  if (!email || !password) {
    errorMsg.textContent = "Please fill in all fields.";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error("Invalid credentials");
    }

    const data = await response.json();
    localStorage.setItem("token", data.token); // Save token
    window.location.href = "index.html"; // Redirect
  } catch (error) {
    errorMsg.textContent = error.message;
  }
}

// ---------- Fetch Places ----------
async function fetchPlaces() {
  const container = document.getElementById("places-container");
  if (!container) return;

  container.innerHTML = "<p class='loading'>Loading places...</p>";

  try {
    const response = await fetch(`${API_BASE_URL}/places/`);
    const places = await response.json();

    displayPlaces(places);
  } catch (error) {
    container.innerHTML = "<p class='loading'>Failed to load places.</p>";
  }
}

function displayPlaces(places) {
  const container = document.getElementById("places-container");
  container.innerHTML = "";

  places.forEach(place => {
    const card = document.createElement("div");
    card.className = "place-card";
    card.innerHTML = `
      <h3>${place.name}</h3>
      <p><strong>Location:</strong> ${place.city || "Unknown"}</p>
      <p><strong>Price:</strong> $${place.price_per_night || "N/A"}/night</p>
      <p><strong>Amenities:</strong> ${(place.amenities || []).join(", ")}</p>
      <button onclick="goToPlace('${place.id}')">View Details</button>
    `;
    container.appendChild(card);
  });
}

function goToPlace(placeId) {
  localStorage.setItem("selectedPlaceId", placeId);
  window.location.href = "place.html";
}

// ---------- Place Details ----------
async function loadPlaceDetails() {
  const placeId = localStorage.getItem("selectedPlaceId");
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }

  const placeDetailsSection = document.getElementById("place-details");
  const reviewList = document.getElementById("reviewList");

  try {
    const [placeRes, reviewsRes] = await Promise.all([
      fetch(`${API_BASE_URL}/places/${placeId}`),
      fetch(`${API_BASE_URL}/places/${placeId}/reviews`)
    ]);

    const place = await placeRes.json();
    const reviews = await reviewsRes.json();

    if (placeDetailsSection) {
      placeDetailsSection.innerHTML = `
        <h2 class="place-title">${place.name}</h2>
        <div class="place-info">
          <p><strong>Location:</strong> ${place.city || "Unknown"}, ${place.state || ""}</p>
          <p><strong>Price:</strong> $${place.price_per_night || "N/A"}/night</p>
          <p><strong>Description:</strong> ${place.description || "No description available."}</p>
          <p><strong>Amenities:</strong> ${(place.amenities || []).join(", ")}</p>
        </div>
      `;
    }

    if (reviewList) {
      reviewList.innerHTML = "";
      reviews.forEach(review => {
        const li = document.createElement("li");
        li.className = "review-card";
        li.innerHTML = `<strong>${review.user_name || "Anonymous"}:</strong> ${review.text}`;
        reviewList.appendChild(li);
      });
    }
  } catch (error) {
    if (placeDetailsSection) {
      placeDetailsSection.innerHTML = "<p class='loading'>Failed to load place details.</p>";
    }
    if (reviewList) {
      reviewList.innerHTML = "<p class='loading'>Failed to load reviews.</p>";
    }
  }
}

// ---------- Submit Review ----------
async function submitReview(event) {
  event.preventDefault();

  const reviewerName = document.getElementById("reviewerName")?.value.trim();
  const reviewText = document.getElementById("reviewText")?.value.trim();
  const rating = document.getElementById("rating")?.value;
  const message = document.getElementById("reviewMsg");
  const placeId = localStorage.getItem("selectedPlaceId");

  const token = localStorage.getItem("token");

  if (!reviewerName || !reviewText || !rating) {
    message.textContent = "Please fill out all fields.";
    return;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/reviews/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        place_id: placeId,
        text: reviewText,
        rating: parseInt(rating),
        user_name: reviewerName,  // Assuming your backend accepts user_name
      }),
    });

    if (!response.ok) {
      throw new Error("Failed to submit review");
    }

    message.style.color = "green";
    message.textContent = "Review submitted successfully!";
    document.getElementById("reviewForm").reset();
  } catch (error) {
    message.style.color = "red";
    message.textContent = error.message;
  }
}

// ---------- Search & Filter ----------
function setupFilters(places) {
  const searchInput = document.getElementById("search");
  const priceFilter = document.getElementById("price-filter");
  const filterBtn = document.getElementById("filterBtn");

  if (!searchInput || !priceFilter || !filterBtn) return;

  filterBtn.addEventListener("click", () => {
    const searchText = searchInput.value.toLowerCase();
    const maxPrice = priceFilter.value;

    const filteredPlaces = places.filter(place => {
      const matchesSearch = place.name.toLowerCase().includes(searchText);
      const matchesPrice = maxPrice === "all" || (place.price_per_night <= parseInt(maxPrice));
      return matchesSearch && matchesPrice;
    });

    displayPlaces(filteredPlaces);
  });
}

// ---------- Initialize ----------
document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname;

  if (path.includes("login.html")) {
    const form = document.querySelector("form");
    if (form) form.addEventListener("submit", login);
  }

  if (path.includes("index.html")) {
    fetchPlaces();
  }

  if (path.includes("place.html")) {
    loadPlaceDetails();
  }

  if (path.includes("add_review.html")) {
    const form = document.getElementById("reviewForm");
    if (form) form.addEventListener("submit", submitReview);
  }
});
