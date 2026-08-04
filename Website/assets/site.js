document.documentElement.classList.remove("no-js");

const navToggle = document.querySelector("[data-nav-toggle]");
const siteNav = document.querySelector("[data-site-nav]");

if (navToggle && siteNav) {
  navToggle.addEventListener("click", () => {
    const willOpen = siteNav.dataset.open !== "true";
    siteNav.dataset.open = String(willOpen);
    navToggle.setAttribute("aria-expanded", String(willOpen));
    navToggle.textContent = willOpen ? "Lukk" : "Meny";
  });

  siteNav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      siteNav.dataset.open = "false";
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.textContent = "Meny";
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && siteNav.dataset.open === "true") {
      siteNav.dataset.open = "false";
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.textContent = "Meny";
      navToggle.focus();
    }
  });
}

const filterButtons = [...document.querySelectorAll("[data-article-filter]")];
const articles = [...document.querySelectorAll("[data-level]")];
const resultCount = document.querySelector("[data-result-count]");

function applyArticleFilter(level) {
  let visible = 0;

  for (const article of articles) {
    const shouldShow = level === "all" || article.dataset.level.split(" ").includes(level);
    article.hidden = !shouldShow;
    if (shouldShow) visible += 1;
  }

  for (const button of filterButtons) {
    button.setAttribute("aria-pressed", String(button.dataset.articleFilter === level));
  }

  if (resultCount) {
    resultCount.textContent = `${visible} ${visible === 1 ? "artikkel" : "artikler"}`;
  }
}

for (const button of filterButtons) {
  button.addEventListener("click", () => applyArticleFilter(button.dataset.articleFilter));
}

if (filterButtons.length && articles.length) {
  applyArticleFilter("all");
}

const requestedArticle = location.hash
  ? document.getElementById(location.hash.slice(1))
  : null;

if (requestedArticle && requestedArticle.dataset.articleRoute) {
  location.replace(requestedArticle.dataset.articleRoute);
}
