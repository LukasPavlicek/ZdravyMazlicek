/* Správa profilu + mazlíčků */
document.addEventListener("DOMContentLoaded", () => {
  const uid = sessionStorage.getItem("user_id");
  if (!uid) return window.location.href = "sign_in_register.html";

  // Načtení profilu
  fetch(`/users/${uid}`)
    .then(r => r.json())
    .then(u => {
      document.getElementById("userEmail").textContent = u.email;
    });

  // Změna hesla
  const passForm = document.getElementById("passForm");
  passForm?.addEventListener("submit", async e => {
    e.preventDefault();
    const p1 = passForm.newPassword.value;
    const p2 = passForm.confirmNewPassword.value;
    if (p1 !== p2) return alert("Hesla se neshodují");
    const res = await fetch(`/users/${uid}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ user_password: p1 })
    });
    if (res.ok) alert("Heslo změněno");
    else      alert("Chyba změny hesla");
  });

  // Správa mazlíčků
  loadPets();
  const petForm = document.getElementById("addPetForm");
  petForm?.addEventListener("submit", async e => {
    e.preventDefault();
    const name    = petForm.petName.value;
    const species = petForm.species.value;
    const age     = parseInt(petForm.age.value) || 0;
    const res = await fetch("/pets/", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ user_id: uid, pet_name: name, species, age })
    });
    if (res.ok) {
      petForm.reset();
      loadPets();
    } else {
      alert("Chyba přidání mazlíčka");
    }
  });

  function loadPets(){
    fetch("/pets/")
      .then(r => r.json())
      .then(arr => {
        const list = document.getElementById("petList");
        list.innerHTML = "";
        arr
         .filter(p => p.user_id == uid)
         .forEach(p => {
           const li = document.createElement("li");
           li.textContent = `${p.pet_name} (${p.species || "?"})`;
           li.onclick = () => {
             // uložíme do sessionStorage skutečné jméno i id
             sessionStorage.setItem("current_pet", p.id);
             sessionStorage.setItem("current_pet_name", p.pet_name);
             sessionStorage.removeItem("current_species");
             window.location.href = "search_page.html";
           };

            const note = document.createElement("span");
          note.className = "pet-note";
          note.textContent = " – (klikněte pro zadání příznaků)";
          li.appendChild(note);

           list.appendChild(li);
         });
      });
  }
});
