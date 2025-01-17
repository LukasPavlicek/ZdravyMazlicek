window.addEventListener("DOMContentLoaded", () => {
  hideCurrentLink();

  setupHistoryButton();

  displaySavedDate();

  showRegister();

  showLogin();
});

function hideCurrentLink() {
  const currentPath = window.location.pathname;
  const links = {
    index: document.querySelector('a[href="index.html"]'),
    history: document.querySelector('a[href="history.html"]'),
    articles: document.querySelector('a[href="articles.html"]'),
    aboutApp: document.querySelector('a[href="about_app.html"]'),
    signInRegister: document.querySelector('a[href="sign_in_register.html"]'),
  };

  if (currentPath.endsWith("index.html") || currentPath === "/") {
    links.index?.classList.add("hidden");
  } else if (currentPath.endsWith("history.html")) {
    links.history?.classList.add("hidden");
  } else if (currentPath.endsWith("articles.html")) {
    links.articles?.classList.add("hidden");
  } else if (currentPath.endsWith("about_app.html")) {
    links.aboutApp?.classList.add("hidden");
  } else if (currentPath.endsWith("sign_in_register.html")) {
    links.signInRegister?.classList.add("hidden");
  }
}

function setupHistoryButton() {
  const historyButton = document.getElementById("histroyButton");
  if (historyButton) {
    historyButton.addEventListener("click", () => {
      const currentDate = new Date();
      const dateOnly = currentDate.toLocaleDateString();
      localStorage.setItem("savedDate", dateOnly);
    });
  }
}

function displaySavedDate() {
  const displayElement = document.getElementById("displayDate");
  if (displayElement) {
    const savedDate = localStorage.getItem("savedDate");
    displayElement.textContent = savedDate ? savedDate : "Datum nebyl uložen.";
  }
}

function showRegister() {
  document.getElementById("loginContainer").style.display = "none";
  document.getElementById("registerContainer").style.display = "block";
}

function showLogin() {
  document.getElementById("registerContainer").style.display = "none";
  document.getElementById("loginContainer").style.display = "block";
}
