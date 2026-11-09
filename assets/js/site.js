(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  // Mobile menu
  var btn = document.querySelector('.menu-btn');
  if (btn) btn.addEventListener('click', function () {
    var open = document.body.classList.toggle('menu-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // Header over the hero: solid once scrolled
  var head = document.querySelector('.site-head.over');
  if (head) {
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 40); };
    onScroll(); window.addEventListener('scroll', onScroll, { passive: true });
  }

  // Reveal on scroll
  var items = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else items.forEach(function (el) { el.classList.add('in'); });

  // Background videos: play only while visible; respect reduced motion / data saver
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
    (navigator.connection && navigator.connection.saveData);
  document.querySelectorAll('video[data-bg]').forEach(function (v) {
    if (calm) { v.removeAttribute('autoplay'); v.pause(); return; }
    v.muted = true;
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); });
      }).observe(v);
    }
  });

  // Lightbox: films (with sound) and photos
  var lb = document.createElement('div');
  lb.className = 'lb'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
  lb.innerHTML = '<div class="lb-stage"></div><button class="lb-close" aria-label="Close">&times;</button>' +
    '<button class="lb-nav prev" aria-label="Previous">&#8249;</button><button class="lb-nav next" aria-label="Next">&#8250;</button>';
  document.body.appendChild(lb);
  var stage = lb.querySelector('.lb-stage'), group = [], idx = 0, lastFocus = null;

  function close() {
    lb.classList.remove('open'); stage.innerHTML = '';
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }
  function showPhoto(i) {
    idx = (i + group.length) % group.length;
    stage.innerHTML = '<img src="' + group[idx].href + '" alt="' + (group[idx].dataset.alt || '') + '">';
  }
  function open(html, navs) {
    lastFocus = document.activeElement;
    stage.innerHTML = html;
    lb.querySelectorAll('.lb-nav').forEach(function (n) { n.style.display = navs ? '' : 'none'; });
    lb.classList.add('open'); document.body.style.overflow = 'hidden';
    lb.querySelector('.lb-close').focus();
  }
  document.addEventListener('click', function (e) {
    var f = e.target.closest('[data-film]');
    if (f) {
      e.preventDefault();
      open('<video src="' + f.dataset.film + '" poster="' + (f.dataset.poster || '') + '" controls autoplay playsinline></video>', false);
      return;
    }
    var p = e.target.closest('.gallery a, [data-photo]');
    if (p) {
      e.preventDefault();
      group = Array.prototype.filter.call(document.querySelectorAll('.gallery a, [data-photo]'), function (a) { return !a.classList.contains('hide'); });
      open('', true); showPhoto(group.indexOf(p));
    }
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.prev').addEventListener('click', function () { showPhoto(idx - 1); });
  lb.querySelector('.next').addEventListener('click', function () { showPhoto(idx + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (group.length && !stage.querySelector('video')) {
      if (e.key === 'ArrowRight') showPhoto(idx + 1);
      if (e.key === 'ArrowLeft') showPhoto(idx - 1);
    }
  });

  // Gallery filters
  document.querySelectorAll('.filters button').forEach(function (b) {
    b.addEventListener('click', function () {
      document.querySelectorAll('.filters button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      var cat = b.dataset.cat;
      document.querySelectorAll('.gallery a').forEach(function (a) {
        a.classList.toggle('hide', cat !== 'all' && a.dataset.cat !== cat);
      });
    });
  });

  // Calculator iframe: fit its height
  var cf = document.querySelector('.calc-frame');
  if (cf) {
    var fit = function () { try { cf.style.height = cf.contentWindow.document.documentElement.scrollHeight + 'px'; } catch (e) {} };
    cf.addEventListener('load', function () { fit(); setInterval(fit, 800); });
  }

  var y = document.getElementById('year'); if (y) y.textContent = new Date().getFullYear();
})();
