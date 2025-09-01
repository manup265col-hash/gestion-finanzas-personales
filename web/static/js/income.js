document.addEventListener('DOMContentLoaded', async () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) { window.location.href = 'index.html'; return; }
  const API_BASE = window.API_BASE || window.location.origin;
  try {
    const res = await fetch(`${API_BASE}/api/auth/me/`, { headers: { 'Authorization': 'Bearer ' + token } });
    if (res.ok) {
      const data = await res.json();
      const nameEl = document.getElementById('incomeUsername');
      if (nameEl) nameEl.textContent = data.first_name || data.email || 'Usuario';
    }
  } catch (_) {}
  // TODO: wire endpoints (IngresosFijos/Extra) and render into tables
});

