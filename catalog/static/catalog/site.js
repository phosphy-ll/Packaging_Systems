document.addEventListener("DOMContentLoaded", () => {
  // Catalog cards: autoplay every five seconds while keeping layout dimensions stable.
  document.querySelectorAll(".product-image").forEach(card => {
    const images = [...card.querySelectorAll("[data-card-slide]")];
    if (images.length < 2) return;
    let index = 0;
    const play = () => {
      if (document.hidden || card.matches(":hover")) return;
      images[index].classList.remove("active");
      index = (index + 1) % images.length;
      images[index].classList.add("active");
    };
    setInterval(play, 5000);
  });

  const primary = document.querySelector("[data-gallery-main] img");
  const thumbs = [...document.querySelectorAll(".photo-thumb")];
  const dialog = document.querySelector(".gallery-lightbox");
  let index = 0;
  const images = thumbs.map(node => ({src:node.dataset.image, alt:node.dataset.alt||""}));
  if (primary && images.length) {
    const show = (i) => {
      index = (i + images.length) % images.length;
      primary.src = images[index].src;
      primary.alt = images[index].alt;
      thumbs.forEach((node, n) => node.classList.toggle("active", n===index));
      const enlarged = dialog?.querySelector("[data-lightbox-img]");
      if (enlarged) {enlarged.src=images[index].src;enlarged.alt=images[index].alt;}
      const counter = dialog?.querySelector("[data-gallery-counter]");
      if (counter) counter.textContent=(index+1)+" / "+images.length;
      const original = dialog?.querySelector("[data-original-file]");
      if (original) original.href=images[index].src;
    };
    thumbs.forEach((node,i)=>node.addEventListener("click",()=>show(i)));
    if (images.length > 1) {
      setInterval(()=>{if(!document.hidden&&!dialog?.open)show(index+1);},5000);
    }
    const open = () => {
      if(!dialog) return;
      show(index);
      dialog.showModal();
      document.body.classList.add("gallery-open");
    };
    document.querySelector("[data-gallery-main]")?.addEventListener("click",open);
    document.querySelector("[data-open-gallery]")?.addEventListener("click",open);
    const close = () => {
      dialog?.close();
      document.body.classList.remove("gallery-open");
    };
    dialog?.querySelector("[data-close-gallery]")?.addEventListener("click",close);
    dialog?.querySelector("[data-gallery-prev]")?.addEventListener("click",()=>show(index-1));
    dialog?.querySelector("[data-gallery-next]")?.addEventListener("click",()=>show(index+1));
    dialog?.addEventListener("click",e=>{if(e.target===dialog)close();});
    dialog?.addEventListener("close",()=>document.body.classList.remove("gallery-open"));
    document.addEventListener("keydown",e=>{
      if(!dialog?.open)return;
      if(e.key==="ArrowLeft")show(index-1);
      if(e.key==="ArrowRight")show(index+1);
      if(e.key==="Escape")close();
    });
  }

  const menu=document.querySelector(".mobile-menu");
  document.addEventListener("click",e=>{if(menu?.open&&!menu.contains(e.target))menu.open=false;});
});
