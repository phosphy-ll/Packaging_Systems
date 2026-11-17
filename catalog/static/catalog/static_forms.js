/* Contact form submissions are processed by Netlify Forms.
 * No third-party API keys, SMTP passwords or email credentials in the browser.
 */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[data-static-contact]");
  if (!form) return;
  const lang = document.documentElement.lang || "ru";
  const words = {
    ru: {sending: "Отправка...", error: "Заявка не отправлена. Повтори попытку или напиши на info@packaging.kz."},
    kk: {sending: "Жіберілуде...", error: "Өтінім жіберілмеді. Қайта көріңіз немесе info@packaging.kz мекенжайына жазыңыз."},
    en: {sending: "Sending...", error: "Your inquiry was not sent. Please retry or email info@packaging.kz."}
  }[lang] || {sending: "Sending...", error: "Please retry or email info@packaging.kz."};

  const params = new URLSearchParams(window.location.search);
  const slug = params.get("product");
  const product = form.querySelector('input[name="product"]');
  if (product && slug && /^[a-z0-9-]{1,180}$/.test(slug)) product.value = slug;

  const feedback = form.querySelector("[data-form-feedback]");
  const submit = form.querySelector('button[type="submit"]');
  form.addEventListener("submit", async event => {
    if (submit?.disabled || !form.reportValidity()) {
      event.preventDefault();
      return;
    }
    event.preventDefault();
    const previous = submit.textContent;
    submit.disabled = true;
    submit.textContent = words.sending;
    if (feedback) {
      feedback.hidden = true;
      feedback.textContent = "";
    }
    try {
      const data = new FormData(form);
      // Netlify identifies a form from its registered name. Payload must be URL-encoded.
      data.set("form-name", form.getAttribute("name") || "packaging-inquiry");
      const response = await fetch("/", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: new URLSearchParams(data).toString(),
        credentials: "same-origin"
      });
      if (!response.ok) throw new Error("HTTP " + response.status);
      window.location.assign(new URL("../thanks/", window.location.href).href);
    } catch (err) {
      console.error("Netlify Forms failed", err);
      if (feedback) {feedback.textContent = words.error; feedback.hidden = false;}
      submit.disabled = false;
      submit.textContent = previous;
    }
  });
});
