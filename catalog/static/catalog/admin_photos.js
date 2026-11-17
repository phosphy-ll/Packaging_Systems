// Immediate image preview for new upload fields in Django product editor.
document.addEventListener("change", (event) => {
  const field = event.target;
  if (!(field instanceof HTMLInputElement) || field.type !== "file") return;
  if (!/^images-\d+-image$/.test(field.name)) return;
  const cell = field.closest("td") || field.parentElement;
  if (!cell) return;
  const current = cell.querySelector(".ps-upload-preview");
  if (current) {
    if (current.dataset.url) URL.revokeObjectURL(current.dataset.url);
    current.remove();
  }
  const file = field.files && field.files[0];
  if (!file || !file.type.startsWith("image/")) return;
  const url = URL.createObjectURL(file);
  const img = document.createElement("img");
  img.src = url;
  img.alt = "Предпросмотр загружаемого изображения";
  img.className = "ps-upload-preview";
  img.dataset.url = url;
  img.style.cssText = "display:block;max-width:160px;max-height:120px;object-fit:contain;margin:10px 0;border:1px solid #dce3e7;padding:4px;background:#fff";
  img.addEventListener("load", () => {}, {once:true});
  cell.append(img);
});
