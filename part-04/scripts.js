document.getElementById('login-form')?.addEventListener('submit', (e) => {
  e.preventDefault();
  const email = e.target.email.value;
  const password = e.target.password.value;
  // Simulate login
  if (email && password) {
    localStorage.setItem('loggedIn', 'true');
    window.location.href = 'index.html';
  }
});