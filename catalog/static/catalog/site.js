document.addEventListener("DOMContentLoaded", () => {
  const primary = document.querySelector(".detail-primary-image img");
  const thumbs = document.querySelectorAll(".photo-thumb");
  if (primary && thumbs.length) {
    thumbs.forEach((button) => {
      button.addEventListener("click", () => {
        const src = button.dataset.image;
        if (!src) return;
        primary.src = src;
        primary.alt = button.dataset.alt || "";
        thumbs.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
      });
    });
  }

  const menu = document.querySelector(".mobile-menu");
  document.addEventListener("click", (event) => {
    if (menu?.open && !menu.contains(event.target)) menu.open = false;
  });
});
