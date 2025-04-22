// Načte články z /​articles-api/ a vykreslí je do UL#articleList
document.addEventListener("DOMContentLoaded", () => {
  const list = document.getElementById("articleList");
  if (!list) return;

  fetch("/articles-api/")
    .then(r => r.json())
    .then(arr => {
      if (!Array.isArray(arr) || arr.length === 0) {
        list.innerHTML = "<li class=\"item-section\">Žádné články nebyly nalezeny.</li>";
        return;
      }

      list.innerHTML = arr.map(a => `
        <li class="result-item">
          <div class="item-section" style="flex:0.8">${a.title}</div>
          <div class="item-section" style="flex:0.6">${a.category || "-"}</div>
          <div class="item-section" style="flex:1.6">
            ${a.content.length > 180 ? a.content.slice(0,180) + "&hellip;" : a.content}
          </div>
          <div class="item-section" style="flex:0.6">${new Date(a.date_created).toLocaleDateString()}</div>
        </li>
      `).join("");
    })
    .catch(err => {
      console.error(err);
      list.innerHTML = "<li class=\"item-section\">Nepodařilo se načíst články.</li>";
    });
});
