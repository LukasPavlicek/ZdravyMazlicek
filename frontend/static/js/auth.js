/* File: frontend/static/js/auth.js */
// Registrace + přihlášení (sessionStorage)

document.addEventListener("DOMContentLoaded", () => {
  const regForm = document.getElementById("registerForm");
  const logForm = document.getElementById("loginForm");

  // Registrace
  regForm?.addEventListener("submit", async e => {
    e.preventDefault();
    const name  = "user";  // případně doplň další pole
    const email = regForm.regEmail.value;
    const pass  = regForm.regPassword.value;
    const pass2 = regForm.confirmPassword.value;

    if (pass !== pass2) {
      alert("Hesla se neshodují!");
      return;
    }

    const res = await fetch("/users/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ user_name: name, email, user_password: pass })
    });
    const data = await res.json();
    if (res.ok) {
      alert("Účet vytvořen! Přihlaste se prosím.");
      showLogin();
      adjustAuthUI();
    } else {
      alert(data.error || data.message || "Chyba registrace");
    }
  });

  // Přihlášení
  logForm?.addEventListener("submit", async e => {
    e.preventDefault();
    const email = logForm.email.value;
    const pass  = logForm.password.value;

    const res = await fetch("/users/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ email, user_password: pass })
    });
    const data = await res.json();
    if (res.ok) {
      sessionStorage.setItem("user_id", data.user_id);
      alert("Přihlášení úspěšné!");
      adjustAuthUI();
      window.location.href = "/";
    } else {
      alert(data.message || "Chybný e‑mail nebo heslo");
    }
  });
});
