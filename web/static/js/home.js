document.addEventListener("DOMContentLoaded", () => {
  const token = sessionStorage.getItem("authToken");
  if (!token) {
    window.location.href = "index.html";
    return;
  }

  const API_BASE = window.API_BASE || window.location.origin;

  const profileIcon = document.getElementById('homeProfileIcon');
  const profileImage = document.getElementById('homeProfileImage');

  // Mostrar icono por defecto
  const showIconFallback = () => {
    if (profileImage) profileImage.style.display = 'none';
    if (profileIcon) profileIcon.style.display = 'block';
  };

  const resolveImageUrl = (raw) => {
    if (!raw) return null;
    const s = String(raw).trim();
    if (!s) return null;
    if (/^https?:\/\//i.test(s)) return s;
    const path = s.startsWith('/') ? s : `/${s}`;
    return `${API_BASE}${path}`;
  };

  const setProfileImageFromUrl = async (rawUrl) => {
    const absUrl = resolveImageUrl(rawUrl);
    if (!absUrl) { showIconFallback(); return; }

    // Clean previous
    profileIcon.style.display = 'none';
    profileImage.style.display = 'block';

    const directUrl = absUrl + (absUrl.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`);
    profileImage.onerror = async () => {
      try {
        const res = await fetch(absUrl, { headers: { Authorization: `Bearer ${token}` } });
        if (!res.ok) throw new Error('fetch image not ok');
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        profileImage.src = url;
        profileImage.onload = () => {
          profileImage.style.display = 'block';
          profileIcon.style.display = 'none';
        };
      } catch {
        showIconFallback();
      }
    };
    profileImage.onload = () => {
      profileImage.style.display = 'block';
      profileIcon.style.display = 'none';
    };
    profileImage.src = directUrl;
  };

  // Load user info
  fetch(`${API_BASE}/api/auth/me/`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + token
    }
  })
  .then(res => { if (!res.ok) throw new Error("No autorizado"); return res.json(); })
  .then(data => {
    document.getElementById("username").textContent = data.first_name || "Usuario";
    if (data && data.profile_image) {
      setProfileImageFromUrl(data.profile_image);
    }
    // Mostrar botón Admin solo para staff/superuser
    try {
      const adminBtn = document.getElementById('adminBtn');
      if (adminBtn) {
        const isAdmin = !!(data && (data.is_staff || data.is_superuser));
        if (isAdmin) {
          adminBtn.style.display = 'inline-block';
          adminBtn.addEventListener('click', (e) => {
            e.preventDefault();
            e.stopPropagation();
            window.location.href = `${window.location.origin}/admin/`;
          });
        } else {
          adminBtn.style.display = 'none';
        }
      }
    } catch (_) {}
  })
  .catch(err => { console.error("Error al cargar datos:", err); });

  // Logout
  const logoutBtn = document.getElementById("logoutBtn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", (e) => {
      try { e.preventDefault(); e.stopPropagation(); } catch(_) {}
      sessionStorage.removeItem("authToken");
      sessionStorage.removeItem("firstName");
      window.location.href = "index.html";
    });
  }
});
