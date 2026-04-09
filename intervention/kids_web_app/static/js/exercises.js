/* exercises.js — Interactive exercise widgets for Dream Space lesson detail pages.
   All state persists in localStorage. No server round-trips required.
   Key convention:  ds-ex-<exerciseId>-<dataType>
*/
(function () {
  'use strict';

  // ── Utility ──────────────────────────────────────────────────────────────

  function saveToStorage(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) {}
  }

  function loadFromStorage(key) {
    try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : null; }
    catch (e) { return null; }
  }

  // Fisher-Yates shuffle — returns a new array, does not mutate input
  function shuffle(arr) {
    var a = arr.slice();
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var tmp = a[i]; a[i] = a[j]; a[j] = tmp;
    }
    return a;
  }

  function escHtml(s) {
    return String(s || '')
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }


  // ── Exercise: Written (type = 'Written') ─────────────────────────────────
  // localStorage:
  //   ds-ex-<id>-task   → string
  //   ds-ex-<id>-steps  → array of strings

  function initWritten(widget) {
    var exId      = widget.dataset.exId;
    var select    = widget.querySelector('select');
    var stepsList = widget.querySelector('.steps-list');
    var countEl   = widget.querySelector('.step-count');
    var addBtn    = widget.querySelector('.add-step-btn');
    var submitBtn = widget.querySelector('.submit-steps-btn');
    var confirm   = widget.querySelector('.submit-confirmation');
    var MIN_STEPS = 6;

    var savedTask  = loadFromStorage('ds-ex-' + exId + '-task') || '';
    var savedSteps = loadFromStorage('ds-ex-' + exId + '-steps') || Array(MIN_STEPS).fill('');

    if (savedTask) select.value = savedTask;

    function renderSteps(steps) {
      stepsList.innerHTML = '';
      steps.forEach(function (text, i) {
        var row = document.createElement('div');
        row.className = 'step-row flex items-center gap-2 mb-2';
        row.innerHTML =
          '<span class="step-num text-xs font-bold" style="min-width:22px;color:var(--purple)">' + (i + 1) + '.</span>' +
          '<input class="form-input step-input flex-1" type="text" placeholder="Step ' + (i + 1) + '…" value="' + escHtml(text) + '">';
        stepsList.appendChild(row);
      });
      updateCount();
    }

    function getStepValues() {
      return Array.from(stepsList.querySelectorAll('.step-input'))
                  .map(function (inp) { return inp.value; });
    }

    function updateCount() {
      var filled = getStepValues().filter(function (v) { return v.trim() !== ''; }).length;
      countEl.textContent = filled;
      countEl.style.color = filled >= MIN_STEPS ? '#4CAF50' : 'var(--text-muted)';
    }

    stepsList.addEventListener('input', function () {
      updateCount();
      saveToStorage('ds-ex-' + exId + '-steps', getStepValues());
    });

    select.addEventListener('change', function () {
      saveToStorage('ds-ex-' + exId + '-task', select.value);
    });

    addBtn.addEventListener('click', function () {
      var steps = getStepValues();
      steps.push('');
      renderSteps(steps);
      var inputs = stepsList.querySelectorAll('.step-input');
      inputs[inputs.length - 1].focus();
    });

    submitBtn.addEventListener('click', function () {
      saveToStorage('ds-ex-' + exId + '-steps', getStepValues());
      confirm.style.display = '';
      setTimeout(function () { confirm.style.display = 'none'; }, 3000);
    });

    renderSteps(savedSteps);
  }


  // ── Exercise: Sorting (type = 'Sorting') ─────────────────────────────────
  // localStorage:
  //   ds-ex-<id>-order  → array of item ids in student's order

  function initSorting(widget) {
    var exId     = widget.dataset.exId;
    var rawItems = JSON.parse(widget.dataset.items || '[]');
    var listEl   = widget.querySelector('.sort-list');
    var checkBtn = widget.querySelector('.check-sort-btn');
    var resetBtn = widget.querySelector('.reset-sort-btn');
    var scoreEl  = widget.querySelector('.sort-score');
    var dragging = null;

    function renderCards(items) {
      listEl.innerHTML = '';
      items.forEach(function (item) {
        var card = document.createElement('div');
        card.className = 'sort-card';
        card.draggable = true;
        card.dataset.id = item.id;
        card.innerHTML =
          '<span class="sort-handle" aria-hidden="true">⠿</span>' +
          '<span class="sort-text">' + escHtml(item.text) + '</span>' +
          '<span class="sort-feedback" aria-hidden="true"></span>';
        listEl.appendChild(card);
      });
      scoreEl.style.display = 'none';
      attachDragListeners();
    }

    function attachDragListeners() {
      listEl.querySelectorAll('.sort-card').forEach(function (card) {
        card.addEventListener('dragstart', function (e) {
          dragging = card;
          setTimeout(function () { card.classList.add('dragging'); }, 0);
          e.dataTransfer.effectAllowed = 'move';
        });

        card.addEventListener('dragend', function () {
          dragging = null;
          card.classList.remove('dragging');
          saveSortOrder();
        });

        card.addEventListener('dragover', function (e) {
          e.preventDefault();
          if (!dragging || dragging === card) return;
          var rect = card.getBoundingClientRect();
          var midY = rect.top + rect.height / 2;
          if (e.clientY < midY) {
            listEl.insertBefore(dragging, card);
          } else {
            listEl.insertBefore(dragging, card.nextSibling);
          }
        });
      });
    }

    function getCurrentIdOrder() {
      return Array.from(listEl.querySelectorAll('.sort-card'))
                  .map(function (c) { return c.dataset.id; });
    }

    function saveSortOrder() {
      saveToStorage('ds-ex-' + exId + '-order', getCurrentIdOrder());
    }

    function checkAnswer() {
      var correctById = {};
      rawItems.forEach(function (item) { correctById[item.id] = item.position; });
      var correct = 0;
      listEl.querySelectorAll('.sort-card').forEach(function (card, idx) {
        var fb = card.querySelector('.sort-feedback');
        var isCorrect = correctById[card.dataset.id] === idx + 1;
        card.classList.remove('sort-correct', 'sort-wrong');
        card.classList.add(isCorrect ? 'sort-correct' : 'sort-wrong');
        fb.textContent = isCorrect ? ' ✓' : ' ✗';
        if (isCorrect) correct++;
      });
      scoreEl.textContent = correct + ' out of ' + rawItems.length + ' correct!';
      scoreEl.style.display = '';
      scoreEl.style.color = correct === rawItems.length ? '#4CAF50' : 'var(--orange)';
    }

    // Restore saved order or shuffle fresh
    var savedOrder = loadFromStorage('ds-ex-' + exId + '-order');
    var startItems;
    if (savedOrder && savedOrder.length === rawItems.length) {
      var byId = {};
      rawItems.forEach(function (item) { byId[item.id] = item; });
      startItems = savedOrder.map(function (id) { return byId[id]; }).filter(Boolean);
    } else {
      startItems = shuffle(rawItems);
    }

    renderCards(startItems);

    checkBtn.addEventListener('click', checkAnswer);

    resetBtn.addEventListener('click', function () {
      saveToStorage('ds-ex-' + exId + '-order', null);
      renderCards(shuffle(rawItems));
    });
  }


  // ── Exercise: Extension (type = 'Extension') ─────────────────────────────
  // localStorage:
  //   ds-ex-<id>-<sectionId>-steps  → array of strings per section

  function initExtension(widget) {
    var exId      = widget.dataset.exId;
    var sections  = JSON.parse(widget.dataset.sections || '[]');
    var container = widget.querySelector('.sections-list');
    var submitBtn = widget.querySelector('.submit-steps-btn');
    var confirm   = widget.querySelector('.submit-confirmation');

    function renderSection(section) {
      var key        = 'ds-ex-' + exId + '-' + section.id + '-steps';
      var savedSteps = loadFromStorage(key) || [''];

      var sectionDiv = document.createElement('div');
      sectionDiv.className = 'ex-section mb-4';
      sectionDiv.dataset.sectionId = section.id;

      var label = document.createElement('div');
      label.className = 'ex-section-label text-xs font-bold mb-2 uppercase tracking-wide';
      label.textContent = section.label;
      sectionDiv.appendChild(label);

      var stepsDiv = document.createElement('div');
      stepsDiv.className = 'section-steps';
      sectionDiv.appendChild(stepsDiv);

      function renderSteps(steps) {
        stepsDiv.innerHTML = '';
        steps.forEach(function (text, i) {
          var row = document.createElement('div');
          row.className = 'step-row flex items-start gap-2 mb-2';
          row.innerHTML =
            '<span class="step-num text-xs font-bold" style="min-width:22px;padding-top:10px;color:var(--purple)">' + (i + 1) + '.</span>' +
            '<textarea class="form-input step-input flex-1" rows="2" placeholder="' + escHtml(section.placeholder) + '">' + escHtml(text) + '</textarea>';
          stepsDiv.appendChild(row);
        });
      }

      renderSteps(savedSteps);

      stepsDiv.addEventListener('input', function () {
        var steps = Array.from(stepsDiv.querySelectorAll('.step-input'))
                         .map(function (t) { return t.value; });
        saveToStorage(key, steps);
      });

      var addBtn = document.createElement('button');
      addBtn.className = 'btn btn-outline btn-sm mt-1';
      addBtn.textContent = '+ Add Step';
      addBtn.addEventListener('click', function () {
        var steps = Array.from(stepsDiv.querySelectorAll('.step-input'))
                         .map(function (t) { return t.value; });
        steps.push('');
        renderSteps(steps);
        var textareas = stepsDiv.querySelectorAll('.step-input');
        textareas[textareas.length - 1].focus();
      });
      sectionDiv.appendChild(addBtn);

      container.appendChild(sectionDiv);
    }

    sections.forEach(renderSection);

    submitBtn.addEventListener('click', function () {
      widget.querySelectorAll('.ex-section').forEach(function (sec) {
        var sid   = sec.dataset.sectionId;
        var key   = 'ds-ex-' + exId + '-' + sid + '-steps';
        var steps = Array.from(sec.querySelectorAll('.step-input'))
                         .map(function (t) { return t.value; });
        saveToStorage(key, steps);
      });
      confirm.style.display = '';
      setTimeout(function () { confirm.style.display = 'none'; }, 3000);
    });
  }


  // ── Bootstrap ─────────────────────────────────────────────────────────────

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.ex-written').forEach(initWritten);
    document.querySelectorAll('.ex-sorting').forEach(initSorting);
    document.querySelectorAll('.ex-extension').forEach(initExtension);
  });

}());
