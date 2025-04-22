// frontend/static/js/history.js
document.addEventListener("DOMContentLoaded", async () => {
  const uid = sessionStorage.getItem("user_id");
  const tbl = document.getElementById("historyTable");
  const no  = document.getElementById("noHistory");

  // Pokud není přihlášen, skryj tabulku a zobraz hlášku
  if (!uid) {
    tbl.style.display = "none";
    no.textContent   = "Pro zobrazení historie se prosím přihlaste.";
    no.style.display = "";
    return;
  }

  // 1) Načti všechna history
  const res = await fetch("/diagnosis/");
  const all = await res.json();

  // 2) Vyfiltruj jen pro přihlášeného uživatele
  const my = all.filter(r => r.user_id == uid);
  if (my.length === 0) {
    tbl.style.display = "none";
    no.textContent   = "Zatím nemáte žádnou uloženou diagnózu.";
    no.style.display = "";
    return;
  }

  // 3) Načti seznam mazlíčků a nemocí pro překlad ID → jméno
  const [petsRes, disRes] = await Promise.all([
    fetch("/pets/"), fetch("/diseases/")
  ]);
  const pets = await petsRes.json();
  const dis  = await disRes.json();

  // 4) Vykresli řádky
  const tbody = tbl.querySelector("tbody");
  my.forEach(r => {
    const tr = document.createElement("tr");

    // formát data
    const dt = new Date(r.search_date).toLocaleString();

    // jméno mazlíčka:
    // 1) pokud v DB máme pet_name, použij ho,
    // 2) jinak pokud je pet_id, najdi ho v pets,
    // 3) jinak polož prázdné
    let petName = "";
    if (r.pet_name) {
      petName = r.pet_name;
    } else if (r.pet_id) {
      const P = pets.find(p => p.id == r.pet_id);
      petName  = P ? (P.pet_name || P.species || "") : "";
    }

    // diagnóza
    const D = dis.find(d => d.id == r.disease_id);
    const diagName = D
      ? D.diseases_name
      : (r.diagnosis || "");

    tr.innerHTML = `
      <td>${dt}</td>
      <td>${petName}</td>
      <td>${diagName}</td>
    `;
    tbody.appendChild(tr);
  });
});
