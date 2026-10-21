'use strict';
const dialog = document.querySelector('#photo-dialog');
if (dialog && typeof dialog.showModal === 'function') {
  const large = dialog.querySelector('img');
  const caption = dialog.querySelector('p');
  let opener;
  document.querySelectorAll('a.photo').forEach(link => {
    link.addEventListener('click', event => {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = link;
      large.src = link.href;
      large.alt = link.querySelector('img').alt;
      caption.textContent = link.closest('figure').querySelector('figcaption').firstChild.textContent;
      dialog.showModal();
    });
  });
  dialog.querySelector('button').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) { const r=dialog.getBoundingClientRect(); if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom) dialog.close(); } });
  dialog.addEventListener('close', () => { large.removeAttribute('src'); opener?.focus({preventScroll:true}); });
}
if ('IntersectionObserver' in window) {
  const links = [...document.querySelectorAll('.toc li a')];
  const observer = new IntersectionObserver(entries => {
    const current = entries.filter(e => e.isIntersecting).sort((a,b) => a.boundingClientRect.top-b.boundingClientRect.top)[0];
    if (!current) return;
    links.forEach(a => { if (a.hash === '#'+current.target.id) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current'); });
  },{rootMargin:'-10% 0px -65% 0px'});
  document.querySelectorAll('.chapter').forEach(s => observer.observe(s));
}
