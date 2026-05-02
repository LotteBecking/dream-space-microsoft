// Block-palette command builder for robot_commands exercises (used in 10 lessons).
(function () {
  const queue = document.getElementById('cmd-queue');
  const emptyMsg = document.getElementById('cmd-empty');
  const palette = document.getElementById('block-palette');
  const countEl = document.getElementById('cmd-count');
  const hidden = document.getElementById('hidden-steps');
  const form = document.getElementById('cmd-form');
  const addCustomBtn = document.getElementById('add-custom-btn');
  const clearBtn = document.getElementById('clear-btn');

  if (!queue || !palette || !form) return;

  /** @type {{text:string, custom:boolean}[]} */
  let steps = [];
  let dragSrc = null;

  function render() {
    // Clear queue except empty msg
    Array.from(queue.querySelectorAll('.cmd-step')).forEach((n) => n.remove());

    if (steps.length === 0) {
      emptyMsg.style.display = '';
    } else {
      emptyMsg.style.display = 'none';
    }

    steps.forEach((s, i) => {
      const row = document.createElement('div');
      row.className = 'cmd-step';
      row.draggable = true;
      row.dataset.index = i;
      row.style.cssText =
        'display:flex; align-items:center; gap:10px;' +
        'padding:10px 14px; border-radius:12px;' +
        'border:2px solid var(--color-border); background:#fff;' +
        'cursor:grab; transition:opacity .15s, transform .12s, box-shadow .12s;';
      row.innerHTML =
        '<span style="width:28px; height:28px; border-radius:50%;' +
        'background:var(--color-primary); color:#fff;' +
        'display:flex; align-items:center; justify-content:center;' +
        'font-size:13px; font-weight:700; flex-shrink:0;">' + (i + 1) + '</span>' +
        (s.custom
          ? '<input type="text" class="input cmd-custom" data-i="' + i + '" value="' +
              (s.text || '').replace(/"/g, '&quot;') +
              '" placeholder="Type command..." ' +
              'style="flex:1; font-family:var(--font-mono, monospace); font-size:14px; padding:6px 10px;">'
          : '<span style="flex:1; font-family:var(--font-mono, monospace); font-size:14px; color:#111;">' +
              s.text + '</span>') +
        '<button type="button" class="cmd-remove" data-i="' + i + '" ' +
        'style="width:28px; height:28px; border-radius:50%; border:none;' +
        ' background:#fee2e2; color:#dc2626; cursor:pointer; font-size:14px;' +
        ' display:flex; align-items:center; justify-content:center; flex-shrink:0;">✕</button>';
      queue.appendChild(row);
    });

    countEl.textContent =
      '(' + steps.length + ' command' + (steps.length === 1 ? '' : 's') + ')';
  }

  // Add via palette
  palette.addEventListener('click', (e) => {
    const btn = e.target.closest('.cmd-block');
    if (!btn) return;
    steps.push({ text: btn.dataset.cmd, custom: false });
    btn.style.transform = 'scale(0.95)';
    setTimeout(() => {
      btn.style.transform = '';
    }, 120);
    render();
  });

  // Custom step
  addCustomBtn.addEventListener('click', () => {
    steps.push({ text: '', custom: true });
    render();
    setTimeout(() => {
      const inputs = queue.querySelectorAll('.cmd-custom');
      if (inputs.length) inputs[inputs.length - 1].focus();
    }, 50);
  });

  // Remove + edit custom
  queue.addEventListener('click', (e) => {
    const rm = e.target.closest('.cmd-remove');
    if (rm) {
      steps.splice(parseInt(rm.dataset.i, 10), 1);
      render();
    }
  });
  queue.addEventListener('input', (e) => {
    if (e.target.classList.contains('cmd-custom')) {
      steps[parseInt(e.target.dataset.i, 10)].text = e.target.value;
    }
  });

  // Clear
  clearBtn.addEventListener('click', () => {
    steps = [];
    render();
  });

  // Drag-to-reorder
  queue.addEventListener('dragstart', (e) => {
    const row = e.target.closest('.cmd-step');
    if (!row) return;
    dragSrc = parseInt(row.dataset.index, 10);
    row.style.opacity = '0.4';
    e.dataTransfer.effectAllowed = 'move';
  });
  queue.addEventListener('dragend', (e) => {
    const row = e.target.closest('.cmd-step');
    if (row) row.style.opacity = '1';
    dragSrc = null;
  });
  queue.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  });
  queue.addEventListener('drop', (e) => {
    e.preventDefault();
    const row = e.target.closest('.cmd-step');
    if (!row || dragSrc === null) return;
    const to = parseInt(row.dataset.index, 10);
    if (dragSrc !== to) {
      const [item] = steps.splice(dragSrc, 1);
      steps.splice(to, 0, item);
      render();
    }
    dragSrc = null;
  });

  // Scenario picker
  document.querySelectorAll('.scenario-pick').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.scenario-pick').forEach((b) => {
        b.style.borderColor = 'var(--color-border)';
        b.style.background = 'var(--color-surface)';
        b.classList.remove('active');
      });
      btn.style.borderColor = 'var(--color-primary)';
      btn.style.background = 'var(--color-primary-soft)';
      btn.classList.add('active');
      const idx = btn.dataset.idx;
      const inp = document.getElementById('scenario-idx-input');
      if (inp) inp.value = idx;
    });
  });

  // Inject hidden inputs on submit
  form.addEventListener('submit', () => {
    hidden.innerHTML = '';
    steps.forEach((s, i) => {
      if (!s.text || !s.text.trim()) return;
      const inp = document.createElement('input');
      inp.type = 'hidden';
      inp.name = 'step_' + (i + 1);
      inp.value = s.text.trim();
      hidden.appendChild(inp);
    });
  });

  render();
})();
