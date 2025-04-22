// 1) Načte příznaky z /symptoms/api do <select>
// 2) Umožní přidat / odebrat čip
// 3) Uloží vybrané symptom IDs a přejde na výsledky
const symptomSelect = document.getElementById("symptomSelect");
const addBtn        = document.getElementById("addSymptomBtn");
const listEl        = document.getElementById("selectedList");
const submitBtn     = document.getElementById("submitBtn");

let selected = [];     //  [{id, name}, …]

// 1. načtení všech příznaků
async function loadSymptoms() {
  const res  = await fetch("/symptoms/");
  const data = await res.json();
  data.forEach(s => {
    const opt = document.createElement("option");
    opt.value = s.id;
    opt.textContent = s.symptoms_name;
    symptomSelect.appendChild(opt);
  });
}
loadSymptoms();

// 2. přidání do seznamu
addBtn.addEventListener("click", () => {
  const id   = parseInt(symptomSelect.value);
  const name = symptomSelect.options[symptomSelect.selectedIndex].text;
  if (!id || selected.some(s => s.id === id)) return;
  selected.push({id, name});
  render();
});

function render() {
  listEl.innerHTML = "";
  selected.forEach(({id, name}) => {
    const li  = document.createElement("li");
    li.className = "symptom-chip";
    li.textContent = name;
    const x   = document.createElement("span");
    x.textContent = "×";
    x.className = "remove";
    x.onclick = () => { selected = selected.filter(s => s.id !== id); render(); };
    li.appendChild(x);
    listEl.appendChild(li);
  });
}

// 3. odeslání a uložení symptomů do localStorage
submitBtn.addEventListener("click", () => {
  if (selected.length === 0) {
    alert("Vyber alespoň jeden příznak.");
    return;
  }
  const ids = selected.map(s => s.id);
  // uložíme si je pro pozdější POST do historie
  localStorage.setItem("selected_symptoms", JSON.stringify(ids));
  // přejdeme na stránku výsledků
  window.location.href = "results.html";
});
