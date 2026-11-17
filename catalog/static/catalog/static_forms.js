/* Client-side contact form for the static export. No passwords or API secrets. */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form[data-static-contact]");
  if (!form) return;
  const lang = document.documentElement.lang || "ru";
  const words = {
    ru: {sending:"Отправка...", error:"Не удалось отправить запрос. Попробуйте ещё раз или напишите на info@packaging.kz."},
    kk: {sending:"Жіберілуде...", error:"Сұраныс жіберілмеді. Қайталап көріңіз немесе info@packaging.kz мекенжайына жазыңыз."},
    en: {sending:"Sending...", error:"Could not submit your inquiry. Please try again or email info@packaging.kz."}
  }[lang] || {sending:"Sending...", error:"Error. Please email info@packaging.kz."};

  const slug = new URLSearchParams(window.location.search).get("product");
  const product = form.querySelector('input[name="product"]');
  if (product && slug && /^[a-z0-9-]{1,180}$/.test(slug)) product.value = slug;

  const feedback = form.querySelector("[data-form-feedback]");
  const submit = form.querySelector('button[type="submit"]');
  form.addEventListener("submit", async (event) => {
    if (submit?.disabled) { event.preventDefault(); return; }
    if (!form.reportValidity()) { event.preventDefault(); return; }
    event.preventDefault();
    const original = submit.textContent;
    submit.disabled = true;
    submit.textContent = words.sending;
    if (feedback) { feedback.hidden = true; feedback.textContent = ""; }
    try {
      const response = await fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" },
        redirect: "follow"
      });
      if (!response.ok) throw new Error("Form provider returned HTTP " + response.status);
      window.location.assign(form.dataset.successUrl || "../thanks/");
    } catch (error) {
      console.error("Contact form submission failed", error);
      if (feedback) { feedback.textContent = words.error; feedback.hidden = false; }
      submit.disabled = false;
      submit.textContent = original;
    }
  });
});
