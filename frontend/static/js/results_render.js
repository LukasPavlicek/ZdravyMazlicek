// File: frontend/static/js/results_render.js
// -------------------------------------------------------------
//  ▸ vykreslí výsledky uložené v localStorage.last_result
//  ▸ tlačítko „Uložit“ – zapíše do /diagnosis/ (diagnosis_history)
// -------------------------------------------------------------

const list   = document.getElementById("resultList");
const result = JSON.parse(localStorage.getItem("last_result")   || "[]");
const sympt  = JSON.parse(localStorage.getItem("last_symptoms") || "[]");

const uid     = sessionStorage.getItem("user_id");          // přihlášený?
const petId   = sessionStorage.getItem("current_pet") || null;
const species = sessionStorage.getItem("species")     || null;

/* --- pomocné vykreslení závažnosti --------------------------- */
const sevBox = lvl => ({
  high  : '<span class="severity-box3"></span>',
  medium: '<span class="severity-box2"></span>',
  low   : '<span class="severity-box1"></span>'
}[lvl] || '<span class="severity-box1"></span>');

/* --- řádek tabulky ------------------------------------------- */
function rowHTML(d){
  const btn = uid
    ? `<button class="saveBtn" data-did="${d.id}">Uložit</button>`
    : "";                                      // nepřihlášen → bez tlačítka

  return `
  <li class="result-item">
    <div class="item-section col-1">${d.diseases_name}</div>
    <div class="item-section col-2">${d.diseases_description}</div>
    <div class="item-section col-3">${sevBox(d.severity)}</div>
    <div class="item-section col-4">${btn}</div>
  </li>`;
}

/* --- vykresli seznam ---------------------------------------- */
list.innerHTML = result.length
  ? result.map(rowHTML).join("")
  : '<li class="result-item"><div class="item-section">Žádná shoda</div></li>';

/* --- ULOŽIT DO HISTORIE ------------------------------------- */
list.addEventListener("click", async e => {
  if (!e.target.classList.contains("saveBtn")) return;

  const body = {
    user_id   : uid,
    pet_id    : petId,
    disease_id: e.target.dataset.did,
    symptoms  : JSON.stringify(sympt),         // uložíme id vybraných symptomů
    diagnosis : species || ""                  // species, pokud není pet
  };

  const res = await fetch("/diagnosis/", {
    method :"POST",
    headers: {"Content-Type":"application/json"},
    body   : JSON.stringify(body)
  });

  if (res.ok){
    e.target.textContent = "Uloženo";
    e.target.disabled = true;
  }else{
    alert("Nepodařilo se uložit do historie.");
  }
});
