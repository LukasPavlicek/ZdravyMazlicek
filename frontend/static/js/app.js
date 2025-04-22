// File: frontend/static/js/app.js
// -------------------------------------------------------------
//  ▸ přepínání odkazů (Login / Můj účet / Odhlásit)
//  ▸ odhlášení
//  ▸ uložení species (pes / kočka) z úvodní stránky
//  ▸ drobné util‑funkce (historie, placeholdery)
// -------------------------------------------------------------

window.addEventListener("DOMContentLoaded", () => {
  adjustAuthUI();
  hideCurrentLink();
  setupHistoryButton();
  displaySavedDate();

  // z úvodní stránky nastavíme druh zvířete
  document.querySelectorAll("[data-species]").forEach(btn => {
    btn.onclick = () => {
      sessionStorage.setItem("species", btn.dataset.species);
      sessionStorage.removeItem("current_pet");          // není vybrán mazlíček
    };
  });

  // na /sign_in_register.html vždy zobrazíme login formulář
  if (location.pathname.endsWith("/sign_in_register.html")) showLogin();
});

/* ---------- UI podle přihlášení ------------------------------------ */
function adjustAuthUI(){
  const loginL  = document.querySelector("#loginLink");
  const accL    = document.querySelector("#accountLink");
  const logoutL = document.querySelector("#logoutLink");
  const logged  = !!sessionStorage.getItem("user_id");

  loginL ?.classList.toggle("hidden",  logged);
  accL   ?.classList.toggle("hidden", !logged);
  if (logoutL){
    logoutL.classList.toggle("hidden", !logged);
    logoutL.onclick = logout;
  }
}

/* ---------- odhlášení ---------------------------------------------- */
function logout(){
  sessionStorage.clear();          // smažeme user_id, species, current_pet…
  adjustAuthUI();
  location.href = "/";             // zpět na domovskou
}

/* ---------- zvýraznění aktuální stránky v nav ---------------------- */
function hideCurrentLink(){
  const path = location.pathname.replace(/^\//,"");     // bez úvodního /
  document.querySelectorAll("nav a").forEach(a => {
    if (a.getAttribute("href") === path || (path==="" && a.getAttribute("href")==="/"))
      a.classList.add("hidden");
  });
}

/* ---------- „uložit datum“ na výsledkové stránce ------------------- */
function setupHistoryButton(){
  const btn = document.getElementById("histroyButton");
  if (btn) btn.addEventListener("click", () =>
    sessionStorage.setItem("savedDate", new Date().toLocaleDateString())
  );
}
function displaySavedDate(){
  const el = document.getElementById("displayDate");
  if (el) el.textContent = sessionStorage.getItem("savedDate") || "Datum nebyl uložen.";
}

/* ---------- přepínání login / register na auth stránce ------------- */
function showRegister(){
  document.getElementById("loginContainer")   ?.style.setProperty("display","none");
  document.getElementById("registerContainer")?.style.setProperty("display","block");
}
function showLogin(){
  document.getElementById("registerContainer")?.style.setProperty("display","none");
  document.getElementById("loginContainer")   ?.style.setProperty("display","block");
}
