  (function() {
    var dataEl = document.getElementById('app-data');
    var NEW_ACHIEVEMENTS = [];
    try { NEW_ACHIEVEMENTS = JSON.parse(dataEl && dataEl.dataset.newAchievements || '[]'); } catch(e) {}
    if (!NEW_ACHIEVEMENTS || !NEW_ACHIEVEMENTS.length) return;

    var container = document.getElementById('achievement-toasts');
    if (!container) return;

    function createSparkles(toast) {
      var positions = [
        {top: '5px', left: '10px'}, {top: '8px', right: '20px'},
        {bottom: '5px', left: '40px'}, {top: '15px', right: '40px'},
        {bottom: '10px', right: '10px'}, {top: '2px', left: '60%'},
      ];
      positions.forEach(function(pos, i) {
        var star = document.createElement('span');
        star.className = 'achievement-toast-star';
        star.textContent = ['✨', '⭐', '💫', '✨', '⭐', '💫'][i];
        star.style.animationDelay = (0.3 + i * 0.15) + 's';
        Object.keys(pos).forEach(function(k) { star.style[k] = pos[k]; });
        toast.appendChild(star);
      });
    }

    NEW_ACHIEVEMENTS.forEach(function(ach, i) {
      setTimeout(function() {
        var toast = document.createElement('div');
        toast.className = 'achievement-toast';
        toast.innerHTML =
          '<div class="achievement-toast-icon">' + ach.icon + '</div>' +
          '<div class="achievement-toast-body">' +
            '<div class="achievement-toast-label">Achievement Unlocked!</div>' +
            '<div class="achievement-toast-title">' + ach.title + '</div>' +
            '<div class="achievement-toast-desc">' + ach.desc + '</div>' +
          '</div>';
        createSparkles(toast);
        container.appendChild(toast);

        // Play sound-like visual feedback: briefly pulse the whole page
        document.body.style.transition = 'filter 0.15s';
        document.body.style.filter = 'brightness(1.05)';
        setTimeout(function() { document.body.style.filter = ''; }, 200);

        // Auto-dismiss after 5 seconds
        setTimeout(function() {
          toast.classList.add('leaving');
          setTimeout(function() {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
          }, 500);
        }, 5000);

        // Click to dismiss early
        toast.addEventListener('click', function() {
          toast.classList.add('leaving');
          setTimeout(function() {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
          }, 500);
        });
      }, i * 800); // Stagger multiple notifications
    });
  })();
  
/* ===== block ===== */
  (function(){
    const overlay = document.getElementById('rocket-overlay');
    const wrap = document.getElementById('rocket-wrap');
    const ship = document.getElementById('rocket-ship');
    const flame = document.getElementById('rocket-flame');
    const stars = document.getElementById('rocket-stars');
    const rText = document.getElementById('rocket-text');
    const smoke = document.getElementById('rocket-smoke');
    if(!overlay) return;

    function spawnStars(){
      stars.innerHTML = '';
      for(let i=0; i<60; i++){
        const s = document.createElement('div');
        s.className = 'rocket-star';
        s.style.left = Math.random()*100 + '%';
        s.style.top = '-5px';
        s.style.animationDuration = (0.5 + Math.random()*0.6) + 's';
        s.style.animationDelay = (Math.random()*2) + 's';
        s.style.width = (2 + Math.random()*3) + 'px';
        s.style.height = s.style.width;
        s.style.opacity = (0.4 + Math.random()*0.6);
        stars.appendChild(s);
      }
    }

    function launchRocket(href){
      overlay.style.pointerEvents = 'all';
      overlay.style.opacity = '1';
      spawnStars();

      // Reset
      wrap.style.transition = 'none';
      wrap.style.bottom = '-160px';
      wrap.style.left = '50%';
      wrap.style.transform = 'translateX(-50%)';
      ship.style.transform = 'rotate(0deg)';
      flame.style.opacity = '0';
      rText.style.opacity = '0';
      smoke.style.opacity = '0';

      // Phase 1: Rumble + smoke + flame ignition
      setTimeout(() => {
        smoke.style.transition = 'opacity .3s';
        smoke.style.opacity = '1';
        flame.style.transition = 'opacity .2s';
        flame.style.opacity = '1';
        wrap.style.animation = 'rumble .08s linear infinite';
        wrap.style.transition = 'bottom 0.7s cubic-bezier(0.1, 0, 0.3, 1)';
        wrap.style.bottom = '25vh';
        rText.style.transition = 'opacity .3s';
        rText.style.opacity = '1';
      }, 200);

      // Phase 2: Hover + tilt
      setTimeout(() => {
        wrap.style.animation = 'none';
        rText.style.opacity = '0';
        smoke.style.opacity = '0';
        ship.style.transition = 'transform .4s ease-in-out';
        ship.style.transform = 'rotate(-18deg)';
        wrap.style.transition = 'bottom 0.4s ease-in, left 0.4s ease-in';
        wrap.style.bottom = '40vh';
        wrap.style.left = '55%';
      }, 950);

      // Phase 3: Blast off in an arc!
      setTimeout(() => {
        ship.style.transition = 'transform .1s';
        ship.style.transform = 'rotate(-5deg)';
        wrap.style.transition = 'bottom 0.4s cubic-bezier(0.4, 0, 1, 0.3), left 0.4s cubic-bezier(0.4, 0, 1, 0.3)';
        wrap.style.bottom = '130vh';
        wrap.style.left = '42%';
        document.querySelectorAll('.rocket-star').forEach(s => {
          s.style.animationDuration = '0.25s';
        });
      }, 1350);

      // Phase 4: Navigate
      setTimeout(() => {
        window.location.href = href;
      }, 1800);
    }

    // Intercept only Mission 1 / first exercise links
    document.addEventListener('click', function(e){
      const link = e.target.closest('a.btn-primary, a.btn-secondary');
      if(!link) return;
      const href = link.href || '';
      const text = link.textContent.toLowerCase().trim();
      // Only trigger rocket for Mission 1 links (exercise/1, first mission start)
      if((text.includes('mission 1') || text === 'start mission') &&
         (href.includes('/exercise/1') || href.includes('/intro'))) {
        e.preventDefault();
        launchRocket(href);
      }
    });
  })();
  
/* ===== block ===== */
  (function() {
    'use strict';

    /* ── Confetti System ──────────────────────────────── */
    var canvas = document.getElementById('confetti-canvas');
    if (canvas) {
      var ctx = canvas.getContext('2d');
      var particles = [];
      var animating = false;

      function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
      }
      var resizeQueued = false;
      function queueResize() {
        if (resizeQueued) return;
        resizeQueued = true;
        requestAnimationFrame(function() {
          resizeQueued = false;
          resize();
        });
      }
      resize();
      window.addEventListener('resize', queueResize, { passive: true });

      var COLORS = ['#7c3aed','#a855f7','#22c55e','#f59e0b','#3b82f6','#ec4899','#14b8a6','#f97316','#06b6d4'];

      function Particle(x, y) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() - 0.5) * 12;
        this.vy = Math.random() * -14 - 4;
        this.gravity = 0.35;
        this.drag = 0.98;
        this.size = Math.random() * 8 + 4;
        this.color = COLORS[Math.floor(Math.random() * COLORS.length)];
        this.rotation = Math.random() * 360;
        this.rotSpeed = (Math.random() - 0.5) * 12;
        this.opacity = 1;
        this.shape = Math.random() > 0.5 ? 'rect' : 'circle';
      }

      function drawParticle(p) {
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation * Math.PI / 180);
        ctx.globalAlpha = p.opacity;
        ctx.fillStyle = p.color;
        if (p.shape === 'rect') {
          ctx.fillRect(-p.size/2, -p.size/4, p.size, p.size/2);
        } else {
          ctx.beginPath();
          ctx.arc(0, 0, p.size/2, 0, Math.PI * 2);
          ctx.fill();
        }
        ctx.restore();
      }

      function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var alive = false;
        for (var i = particles.length - 1; i >= 0; i--) {
          var p = particles[i];
          p.vx *= p.drag;
          p.vy += p.gravity;
          p.x += p.vx;
          p.y += p.vy;
          p.rotation += p.rotSpeed;
          p.opacity -= 0.008;
          if (p.opacity > 0 && p.y < canvas.height + 50) {
            drawParticle(p);
            alive = true;
          } else {
            particles.splice(i, 1);
          }
        }
        if (alive) {
          requestAnimationFrame(animate);
        } else {
          animating = false;
          ctx.clearRect(0, 0, canvas.width, canvas.height);
        }
      }

      window.fireConfetti = function(x, y, count) {
        x = x || canvas.width / 2;
        y = y || canvas.height / 3;
        count = count || 80;
        for (var i = 0; i < count; i++) {
          particles.push(new Particle(x, y));
        }
        if (!animating) {
          animating = true;
          animate();
        }
      };

      /* Auto-fire confetti on success callouts */
      var successEl = document.querySelector('.callout-success, [class*="chip-success"]');
      if (successEl) {
        setTimeout(function() {
          var rect = successEl.getBoundingClientRect();
          window.fireConfetti(rect.left + rect.width/2, rect.top + rect.height/2, 100);
        }, 300);
      }
    }

    /* ── Card hover is now shadow-only, no tilt needed ── */

    /* ── Button click ripple effect ────────────────── */
    document.addEventListener('pointerdown', function(e) {
      var btn = e.target.closest('.btn');
      if (!btn || btn.disabled) return;
      if (btn.dataset.rippleReady !== '1') {
        btn.style.position = 'relative';
        btn.style.overflow = 'hidden';
        btn.dataset.rippleReady = '1';
      }
      requestAnimationFrame(function() {
        var ripple = document.createElement('span');
        var rect = btn.getBoundingClientRect();
        var size = Math.max(rect.width, rect.height) * 2;
        ripple.style.cssText = 'position:absolute;border-radius:50%;background:rgba(255,255,255,0.35);' +
          'width:' + size + 'px;height:' + size + 'px;' +
          'left:' + (e.clientX - rect.left - size/2) + 'px;' +
          'top:' + (e.clientY - rect.top - size/2) + 'px;' +
          'transform:scale(0);animation:rippleOut 0.5s ease-out forwards;pointer-events:none;';
        btn.appendChild(ripple);
        setTimeout(function() { ripple.remove(); }, 600);
      });
    }, { passive: true });

    /* ── Counting animation for XP (sidebar only, NOT navbar) ── */
    document.querySelectorAll('#total-xp-num').forEach(function(el) {
      var from = parseInt(el.getAttribute('data-from') || '0');
      var to = parseInt(el.getAttribute('data-to') || el.textContent);
      if (to > from && to > 0) {
        var current = from;
        el.textContent = current;
        var interval = setInterval(function() {
          current += Math.ceil((to - current) / 5);
          if (current >= to) { current = to; clearInterval(interval); }
          el.textContent = current;
        }, 40);
      }
    });

    /* ── Emoji rain on achievement toast ──────────── */
    var observer = new MutationObserver(function(mutations) {
      mutations.forEach(function(m) {
        m.addedNodes.forEach(function(node) {
          if (node.nodeType === 1 && node.querySelector) {
            var emoji = node.querySelector('[style*="font-size:48px"], [style*="font-size: 48px"]');
            if (emoji) {
              emoji.style.animation = 'emojiPop 0.5s cubic-bezier(0.34,1.56,0.64,1) both';
              /* Fire confetti for achievements */
              if (window.fireConfetti) {
                setTimeout(function() { window.fireConfetti(undefined, undefined, 60); }, 200);
              }
            }
          }
        });
      });
    });
    var toastContainer = document.getElementById('achievement-toasts');
    if (toastContainer) {
      observer.observe(toastContainer, { childList: true });
    }

  })();
  

/* ========= home page ========= */
(function() {
  // ── 1. XP Bar fill animation (Duolingo-style smooth fill + glow) ──
  var xpFill = document.getElementById('xp-bar-fill');
  var xpGlow = document.getElementById('xp-bar-glow');
  if (xpFill) {
    setTimeout(function() {
      xpFill.style.width = xpFill.dataset.target + '%';
      if (xpGlow) { xpGlow.style.opacity = '1'; }
      setTimeout(function() {
        if (xpGlow) xpGlow.style.opacity = '0';
      }, 1400);
    }, 400);
  }

  // ── 2. XP gain badge pop-in ──
  var xpBadge = document.getElementById('xp-gain-badge');
  if (xpBadge) {
    setTimeout(function() {
      xpBadge.style.transition = 'opacity .4s, transform .4s cubic-bezier(0.34,1.56,0.64,1)';
      xpBadge.style.opacity = '1';
      xpBadge.style.transform = 'translateY(0) scale(1)';
      setTimeout(function() {
        xpBadge.style.transition = 'opacity .6s, transform .6s';
        xpBadge.style.opacity = '0';
        xpBadge.style.transform = 'translateY(-10px) scale(0.8)';
      }, 2500);
    }, 800);
  }

  // ── 3. Total XP count-up animation ──
  var xpNum = document.getElementById('total-xp-num');
  if (xpNum) {
    var from = parseInt(xpNum.dataset.from) || 0;
    var to = parseInt(xpNum.dataset.to) || 0;
    if (from !== to) {
      var duration = 1200;
      var start = null;
      function countUp(ts) {
        if (!start) start = ts;
        var elapsed = ts - start;
        var progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.round(from + (to - from) * eased);
        xpNum.textContent = current;
        if (progress < 1) requestAnimationFrame(countUp);
      }
      setTimeout(function() { requestAnimationFrame(countUp); }, 600);
    }
  }

  // ── 4. Star pop-in animation (new stars bounce) ──
  document.querySelectorAll('.home-star').forEach(function(star, i) {
    if (star.dataset.new === '1') {
      star.style.transform = 'scale(0)';
      star.style.opacity = '0';
      setTimeout(function() {
        star.style.transition = 'transform .5s cubic-bezier(0.34,1.56,0.64,1), opacity .3s, filter .3s';
        star.style.transform = 'scale(1.3)';
        star.style.opacity = '1';
        star.style.filter = '';
        setTimeout(function() {
          star.style.transform = 'scale(1)';
        }, 300);
      }, 1000 + i * 200);
    } else if (star.dataset.earned === '1') {
      // Already earned - just make sure visible
      star.style.opacity = '1';
      star.style.filter = '';
    }
  });

  // ── 5. Checklist staggered entrance ──
  document.querySelectorAll('.checklist-row').forEach(function(row, i) {
    setTimeout(function() {
      row.style.opacity = '1';
      row.style.transform = 'translateX(0)';
      // Bounce the checkmark if done
      if (row.dataset.done === 'true') {
        var icon = row.querySelector('.checklist-icon');
        if (icon) {
          setTimeout(function() {
            icon.style.transform = 'scale(1.3)';
            setTimeout(function() { icon.style.transform = 'scale(1)'; }, 200);
          }, 200);
        }
      }
    }, 300 + i * 120);
  });

  // ── 6. Achievement rows staggered entrance ──
  document.querySelectorAll('.ach-row').forEach(function(row, i) {
    setTimeout(function() {
      row.style.opacity = row.style.opacity === '0' ? '' : row.style.opacity;
      row.style.transform = 'translateY(0)';
      // Restore proper opacity for locked ones
      if (!row.style.background.includes('fef3c7')) {
        row.style.opacity = '.5';
      } else {
        row.style.opacity = '1';
      }
    }, 800 + i * 100);
  });

  // ── 7. Player card floating particles ──
  var particles = document.getElementById('player-particles');
  if (particles) {
    for (var p = 0; p < 8; p++) {
      var dot = document.createElement('div');
      dot.style.cssText = 'position:absolute; width:' + (3 + Math.random()*4) + 'px; height:' + (3 + Math.random()*4) + 'px; border-radius:50%; background:rgba(255,255,255,' + (0.15 + Math.random()*0.2) + '); left:' + (Math.random()*100) + '%; top:' + (Math.random()*100) + '%; animation:particle-float ' + (3 + Math.random()*4) + 's ease-in-out infinite alternate; animation-delay:' + (Math.random()*3) + 's;';
      particles.appendChild(dot);
    }
  }

  // ── 8. Confetti burst (when all exercises done + xp gained) ──
  var canvas = document.getElementById('confetti-canvas');
  var homeData = document.getElementById('home-data');
  var xpGained = homeData ? parseInt(homeData.dataset.xpGained || '0') : 0;
  var allDone = homeData ? homeData.dataset.allDone === 'true' : false;
  if (canvas && xpGained > 0 && allDone) {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var ctx = canvas.getContext('2d');
    var confetti = [];
    var colors = ['#fbbf24', '#7c3aed', '#ec4899', '#16a34a', '#2563eb', '#f97316', '#06b6d4'];
    for (var c = 0; c < 120; c++) {
      confetti.push({
        x: Math.random() * canvas.width,
        y: -20 - Math.random() * 200,
        w: 6 + Math.random() * 6,
        h: 4 + Math.random() * 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        vx: (Math.random() - 0.5) * 4,
        vy: 2 + Math.random() * 4,
        rot: Math.random() * 360,
        vr: (Math.random() - 0.5) * 8,
        opacity: 1,
      });
    }
    var frame = 0;
    function drawConfetti() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      var alive = false;
      confetti.forEach(function(p) {
        if (p.opacity <= 0) return;
        alive = true;
        p.x += p.vx;
        p.y += p.vy;
        p.rot += p.vr;
        p.vy += 0.08;
        if (frame > 60) p.opacity -= 0.008;
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot * Math.PI / 180);
        ctx.globalAlpha = Math.max(0, p.opacity);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
        ctx.restore();
      });
      frame++;
      if (alive && frame < 200) requestAnimationFrame(drawConfetti);
      else ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    setTimeout(function() { requestAnimationFrame(drawConfetti); }, 1500);
  }
})();
/* ----- block ----- */
(function() {
  // Generic accordion factory — works for both track and lesson foldouts
  function makeAccordion(selector, headerSelector, bodySelector) {
    var panels = document.querySelectorAll(selector);
    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function nextFrame(fn) {
      requestAnimationFrame(function() { requestAnimationFrame(fn); });
    }

    function afterHeightTransition(body, timeout, done) {
      var finished = false;
      function finish() {
        if (finished) return;
        finished = true;
        body.removeEventListener('transitionend', onEnd);
        done();
      }
      function onEnd(e) {
        if (e.target === body && e.propertyName === 'height') finish();
      }
      body.addEventListener('transitionend', onEnd);
      setTimeout(finish, timeout || 520);
    }

    function collapse(el) {
      return new Promise(function(resolve) {
        if (el.dataset.animating === '1') { resolve(); return; }
        var body = el.querySelector(bodySelector);
        if (!body) { resolve(); return; }

        el.dataset.animating = '1';
        body.classList.add('is-animating');
        if (reduceMotion) {
          body.style.height = '0px';
          body.style.opacity = '0';
          el.classList.remove('is-open');
          body.classList.remove('is-animating');
          delete el.dataset.animating;
          resolve();
          return;
        }

        body.style.height = body.scrollHeight + 'px';
        body.style.opacity = '1';
        nextFrame(function() {
          el.classList.remove('is-open');
          body.style.height = '0px';
          body.style.opacity = '0';
        });
        afterHeightTransition(body, 450, function() {
          body.classList.remove('is-animating');
          delete el.dataset.animating;
          resolve();
        });
      });
    }

    function expand(el) {
      return new Promise(function(resolve) {
        if (el.dataset.animating === '1') { resolve(); return; }
        var body = el.querySelector(bodySelector);
        if (!body) { resolve(); return; }

        el.dataset.animating = '1';
        body.classList.add('is-animating');
        el.classList.add('is-open');
        if (reduceMotion) {
          body.style.height = 'auto';
          body.style.opacity = '1';
          body.classList.remove('is-animating');
          delete el.dataset.animating;
          resolve();
          return;
        }

        body.style.height = 'auto';
        var h = body.scrollHeight;
        body.style.height = '0px';
        body.style.opacity = '0';
        nextFrame(function() {
          body.style.height = h + 'px';
          body.style.opacity = '1';
        });
        afterHeightTransition(body, 450, function() {
          body.style.height = 'auto';
          body.classList.remove('is-animating');
          delete el.dataset.animating;
          resolve();
        });
      });
    }

    panels.forEach(function(panel) {
      var btn = panel.querySelector(headerSelector);
      if (!btn || btn.disabled) return;

      btn.addEventListener('click', function() {
        if (panel.dataset.animating === '1') return;
        var isOpen = panel.classList.contains('is-open');
        if (isOpen) {
          btn.setAttribute('aria-expanded', 'false');
          collapse(panel);
        } else {
          var sibling = panel.parentElement.querySelector(selector + '.is-open');
          btn.setAttribute('aria-expanded', 'true');
          if (sibling && sibling !== panel) {
            var siblingBtn = sibling.querySelector(headerSelector);
            if (siblingBtn) siblingBtn.setAttribute('aria-expanded', 'false');
            collapse(sibling);
          }
          expand(panel);
        }
      });

      // Auto-open
      if (panel.getAttribute('data-auto-open') === 'true') {
        panel.classList.add('is-open');
        btn.setAttribute('aria-expanded', 'true');
        var body = panel.querySelector(bodySelector);
        if (body) { body.style.height = 'auto'; body.style.opacity = '1'; }
      } else {
        btn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // Track-level accordion
  makeAccordion('.track-foldout', '.track-foldout-header', '.track-foldout-body');

  // Lesson-level accordion (inside each track)
  makeAccordion('.lesson-foldout', '.lesson-foldout-header', '.lesson-foldout-body');
})();
