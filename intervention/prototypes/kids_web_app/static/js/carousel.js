/* carousel.js — auto-advancing news carousel with swipe + dots */
(function () {
  var container = document.querySelector('.carousel-container');
  if (!container) return;

  var track = container.querySelector('.carousel-track');
  var dotsEl = container.querySelector('.carousel-dots');
  var prevBtn = container.querySelector('.carousel-btn-prev');
  var nextBtn = container.querySelector('.carousel-btn-next');

  var slides = [];
  var current = 0;
  var timer = null;
  var touchStartX = 0;

  function renderSkeleton() {
    var w = slideWidth();
    track.innerHTML = [
      '<div class="carousel-slide" style="width:' + w + 'px;min-width:' + w + 'px">',
      '  <div class="news-card">',
      '    <div class="news-image-placeholder skeleton" style="width:140px;min-height:100px;"></div>',
      '    <div class="news-body" style="gap:8px;padding:16px;">',
      '      <div class="skeleton" style="height:14px;border-radius:4px;width:80%;"></div>',
      '      <div class="skeleton" style="height:14px;border-radius:4px;width:60%;"></div>',
      '      <div class="skeleton" style="height:12px;border-radius:4px;width:40%;margin-top:auto;"></div>',
      '    </div>',
      '  </div>',
      '</div>',
    ].join('');
  }

  function renderSlides(items) {
    slides = items;
    track.innerHTML = items.map(function (item) {
      var img = item.image
        ? '<img class="news-image" src="' + escHtml(item.image) + '" alt="" loading="lazy" onerror="this.parentNode.innerHTML=\'<div class=news-image-placeholder>📰</div>\'">'
        : '<div class="news-image-placeholder">📰</div>';
      return [
        '<div class="carousel-slide">',
        '  <a class="news-card" href="' + escHtml(item.url) + '" target="_blank" rel="noopener" style="text-decoration:none;color:inherit;">',
        '    ' + img,
        '    <div class="news-body">',
        '      <div class="news-title">' + escHtml(item.title) + '</div>',
        '      <div class="news-meta">' + escHtml(item.source) + ' · ' + escHtml(item.time) + '</div>',
        '    </div>',
        '  </a>',
        '</div>',
      ].join('');
    }).join('');

    // Dots
    if (dotsEl) {
      dotsEl.innerHTML = items.map(function (_, i) {
        return '<button class="carousel-dot' + (i === 0 ? ' active' : '') + '" aria-label="Slide ' + (i + 1) + '"></button>';
      }).join('');
      dotsEl.querySelectorAll('.carousel-dot').forEach(function (dot, i) {
        dot.addEventListener('click', function () { goTo(i); });
      });
    }

    setSlideSizes();
    startAuto();
  }

  function slideWidth() {
    return container.offsetWidth;
  }

  function goTo(index) {
    current = (index + slides.length) % slides.length;
    track.style.transform = 'translateX(-' + (current * slideWidth()) + 'px)';
    if (dotsEl) {
      dotsEl.querySelectorAll('.carousel-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === current);
      });
    }
  }

  function setSlideSizes() {
    var w = slideWidth();
    track.querySelectorAll('.carousel-slide').forEach(function (s) {
      s.style.width = w + 'px';
      s.style.minWidth = w + 'px';
    });
    goTo(current);
  }

  function startAuto() {
    clearInterval(timer);
    timer = setInterval(function () { goTo(current + 1); }, 6000);
  }

  container.addEventListener('mouseenter', function () { clearInterval(timer); });
  container.addEventListener('mouseleave', startAuto);

  container.addEventListener('touchstart', function (e) {
    touchStartX = e.touches[0].clientX;
  }, { passive: true });
  container.addEventListener('touchend', function (e) {
    var diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) goTo(current + (diff > 0 ? 1 : -1));
    startAuto();
  });

  if (prevBtn) prevBtn.addEventListener('click', function () { goTo(current - 1); startAuto(); });
  if (nextBtn) nextBtn.addEventListener('click', function () { goTo(current + 1); startAuto(); });

  function escHtml(s) {
    return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  // Resize handler — recalculate slide widths when window resizes
  window.addEventListener('resize', function () { setSlideSizes(); });

  // Fetch news
  renderSkeleton();
  fetch('/api/news')
    .then(function (r) { return r.json(); })
    .then(renderSlides)
    .catch(function () {
      renderSlides([
        { title: 'Girls Are Changing the World of Coding', url: '#', image: null, source: 'Dream Space', time: 'now' },
        { title: 'How AI Helps Scientists Discover New Medicines', url: '#', image: null, source: 'Dream Space', time: 'now' },
        { title: 'Young Coder Builds App to Help Her Community', url: '#', image: null, source: 'Dream Space', time: 'now' },
      ]);
    });
}());
