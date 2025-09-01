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
    try {
        const API_BASE = window.API_BASE || window.location.origin;
        const response = await fetch( `${API_BASE}/api/auth/signup-request/`, { 
            method: " POST\,
 headers: { \Content-Type\: \application/json\ },
 body: JSON.stringify({
 email,
 password,
 birthday,
 phone,
 country,
 first_name: firstName,
 last_name: lastName,
 })
 });
        if (response.ok) {
            alert("Cuenta creada con éxito. Serás redirigido al login.");
            window.location.href = "index.html";
        const ct = response.headers.get(" content-type\) || \\;
 const data = ct.includes(\application/json\) ? await response.json() : {};

 if (response.ok) {
 sessionStorage.setItem(\signupEmail\, email);
 alert(\Solicitud enviada. Te redirigimos para verificar el codigo.\);
 window.location.href = \verify-signup.html\;
 } else {
 let msg = \Error en la solicitud\;
 try {
 const errorData = await response.json();
 msg = \Error: \ + (errorData.error || errorData.detail || JSON.stringify(errorData));
 } catch (e) {}
 alert(msg);
 }
 } catch (error) {
 console.error(\Error en la solicitud:\, error);
 alert(\Error en la conexion con el servidor.\);
 }
});
