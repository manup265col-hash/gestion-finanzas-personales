document.getElementById("signup-btn").addEventListener("click", async function () {
    const email = document.getElementById("email").value;
    const firstName = document.getElementById("firstname").value;
    const lastName = document.getElementById("lastname").value;
    const birthday = document.getElementById("birthday").value;
    const phone = document.getElementById("phone").value;
    const country = document.getElementById("country").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm-password").value;

    // Validación básica
    if (!email || !birthday || !phone || !country || !password || !confirmPassword) {
        alert("Por favor completa todos los campos obligatorios.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Las contraseñas no coinciden.");
        return;
    }

    // Construir FormData porque la API no acepta application/json
    const formData = new FormData();
    formData.append('email', email);
    formData.append('password', password);
    formData.append('birthday', birthday);
    formData.append('phone', phone);
    formData.append('country', country);
    if (firstName) formData.append('first_name', firstName);
    if (lastName) formData.append('last_name', lastName);

    try {
        const API_BASE = window.API_BASE || "https://pagina-web-finansas-b6474cfcee14.herokuapp.com";
        const response = await fetch(`${API_BASE}/api/auth/register/`, {
            method: "POST",
            // No establecemos Content-Type manualmente; el navegador añadirá multipart/form-data con boundary
            body: formData
        });

        if (response.ok) {
            alert("Cuenta creada con éxito. Serás redirigido al login.");
            window.location.href = "index.html";
        } else {
            let msg = 'Error en el registro';
            try {
              const errorData = await response.json();
              msg = "Error: " + JSON.stringify(errorData);
            } catch (_) {
              // si no es JSON (p.ej., 415), mantenemos mensaje genérico
            }
            alert(msg);
        }
    } catch (error) {
        console.error("Error en la solicitud:", error);
        alert("Error en la conexión con el servidor.");
    }
});
