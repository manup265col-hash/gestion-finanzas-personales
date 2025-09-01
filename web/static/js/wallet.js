document.addEventListener('DOMContentLoaded', async () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  const API_BASE = window.API_BASE || window.location.origin;
  const nameEl = document.getElementById('walletUsername');
  try {
    const res = await fetch(`${API_BASE}/api/auth/me/`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
      },
    });
    if (!res.ok) throw new Error('No autorizado');
    const data = await res.json();
    if (nameEl) nameEl.textContent = (data.first_name || data.email || 'Usuario');
  } catch (e) {
    // Si falla, fuerza login
    window.location.href = 'index.html';
  }
});

