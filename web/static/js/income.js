document.addEventListener('DOMContentLoaded', async () => {
  const token = sessionStorage.getItem('authToken');
  if (!token) { window.location.href = 'index.html'; return; }
  const API_BASE = window.API_BASE || window.location.origin;
  try {
    const res = await fetch(`${API_BASE}/api/auth/me/`, { headers: { 'Authorization': 'Bearer ' + token } });
    if (res.ok) {
      const data = await res.json();
      const nameEl = document.getElementById('incomeUsername');
      const imgEl = document.getElementById('walletProfileImage');
      if (nameEl) nameEl.textContent = data.first_name || data.email || 'Usuario';
    const resolveImageUrl = (raw) => {
      if (!raw) return null;
      const s = String(raw).trim();
      if (!s) return null;
      if (/^https?:\/\//i.test(s)) return s;
      const path = s.startsWith('/') ? s : `/${s}`;
      return `${API_BASE}${path}`;
  }
   const url = resolveImageUrl(data && data.profile_image);
      if (url && imgEl && iconEl) {
        imgEl.onload = () => { imgEl.style.display = 'block'; iconEl.style.display = 'none'; };
        imgEl.onerror = () => { imgEl.style.display = 'none'; iconEl.style.display = 'block'; };
        imgEl.src = url + (url.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`);
      }
    }
  } catch (_) {}

    
   

  // Tabs behavior
  const tabs = document.querySelectorAll('.tab-btn');
  tabs.forEach(btn => {
    btn.addEventListener('click', () => {
      tabs.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const target = document.querySelector(btn.dataset.target);
      document.querySelectorAll('.tab-view').forEach(v => v.style.display = 'none');
      if (target) target.style.display = 'block';
    });
  });

  // Default to Fixed Income
  const first = document.querySelector('.tab-btn');
  if (first) first.click();

  // TODO: wire endpoints (IngresosFijos/Extra) and render into tables
});
