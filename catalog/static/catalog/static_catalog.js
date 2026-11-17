/* Search, filters and sorting for the static catalog. Never contacts a backend. */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form.filters");
  const grid = document.querySelector(".product-grid");
  if (!form || !grid) return;
  const cards = Array.from(grid.querySelectorAll(".product-card"));
  const search = form.querySelector('[name="q"]');
  const category = form.querySelector('[name="category"]');
  const condition = form.querySelector('[name="condition"]');
  const sorting = form.querySelector('[name="sort"]');
  const total = document.querySelector(".listing-top strong");
  const lang = document.documentElement.lang || "ru";
  const emptyText = {
    ru: "По выбранным фильтрам оборудование не найдено.",
    kk: "Таңдалған сүзгілер бойынша жабдық табылмады.",
    en: "No equipment matches the selected filters."
  }[lang] || "No results";

  const empty = document.createElement("p");
  empty.className = "static-catalog-empty";
  empty.textContent = emptyText;
  empty.hidden = true;
  grid.after(empty);

  const normalize = text => (text || "").toLocaleLowerCase().trim();

  function apply() {
    const q = normalize(search?.value);
    const cat = category?.value || "";
    const cond = condition?.value || "";
    let shown = [];
    for (const card of cards) {
      const matches = (!q || normalize(card.textContent).includes(q)) &&
        (!cat || card.dataset.category === cat) &&
        (!cond || card.dataset.condition === cond);
      card.hidden = !matches;
      if (matches) shown.push(card);
    }
    const mode = sorting?.value || "newest";
    if (mode === "price_low" || mode === "price_high") {
      shown.sort((a, b) => {
        const aPrice = a.dataset.price === "" ? null : Number(a.dataset.price);
        const bPrice = b.dataset.price === "" ? null : Number(b.dataset.price);
        if (aPrice === null) return 1;
        if (bPrice === null) return -1;
        if (a.dataset.currency !== b.dataset.currency) return 0; // no FX conversion
        return mode === "price_low" ? aPrice - bPrice : bPrice - aPrice;
      });
    } else {
      shown.sort((a, b) => cards.indexOf(a) - cards.indexOf(b));
    }
    shown.forEach(card => grid.append(card));
    if (total) total.textContent = String(shown.length);
    empty.hidden = shown.length !== 0;
  }
  form.addEventListener("submit", event => { event.preventDefault(); apply(); });
  [search, category, condition, sorting].filter(Boolean).forEach(control => {
    control.addEventListener(control === search ? "input" : "change", apply);
  });
  const clear = document.querySelector(".listing-top a");
  clear?.addEventListener("click", event => {
    event.preventDefault();
    form.reset();
    apply();
  });
  apply();
});
