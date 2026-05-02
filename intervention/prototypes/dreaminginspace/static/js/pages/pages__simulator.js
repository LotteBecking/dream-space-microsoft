  (function() {
    // Hint button click: fills the input
    document.querySelectorAll('.cmd-hint-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        document.getElementById('cmd-input').value = btn.dataset.cmd;
        document.getElementById('cmd-input').focus();
      });
    });

    // Randomize the hint buttons order on page load
    var hintContainer = document.getElementById('cmd-hint-buttons');
    if (hintContainer) {
      var btns = Array.from(hintContainer.children);
      for (var i = btns.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        hintContainer.appendChild(btns[j]);
        btns.splice(j, 1, btns[i]);
      }
    }

    // Drag-to-reorder for command list
    var cmdRows = document.querySelectorAll('.cmd-row');
    if (cmdRows.length > 0) {
      var cmdList = cmdRows[0].parentElement;
      var dragItem = null;

      cmdRows.forEach(function(row) {
        row.setAttribute('draggable', 'true');
        row.style.cursor = 'grab';
        row.style.transition = 'opacity .15s';

        row.addEventListener('dragstart', function(e) {
          dragItem = row;
          row.style.opacity = '0.4';
          e.dataTransfer.effectAllowed = 'move';
        });
        row.addEventListener('dragend', function() {
          row.style.opacity = '1';
          dragItem = null;
          renumberCmds();
        });
        row.addEventListener('dragover', function(e) {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
        });
        row.addEventListener('drop', function(e) {
          e.preventDefault();
          if (dragItem && dragItem !== row) {
            var allRows = Array.from(cmdList.querySelectorAll('.cmd-row'));
            var fromIdx = allRows.indexOf(dragItem);
            var toIdx = allRows.indexOf(row);
            if (fromIdx < toIdx) {
              cmdList.insertBefore(dragItem, row.nextSibling);
            } else {
              cmdList.insertBefore(dragItem, row);
            }
          }
        });
      });

      function renumberCmds() {
        cmdList.querySelectorAll('.cmd-row').forEach(function(r, i) {
          r.querySelector('.cmd-index').textContent = i + 1;
        });
      }
    }

    // On Run form submit: inject current command order as hidden fields
    var runForm = document.getElementById('run-form');
    if (runForm) {
      runForm.addEventListener('submit', function() {
        var container = document.getElementById('run-order-fields');
        container.innerHTML = '';
        document.querySelectorAll('.cmd-row .cmd-text').forEach(function(el) {
          var inp = document.createElement('input');
          inp.type = 'hidden';
          inp.name = 'cmd_order';
          inp.value = el.textContent.trim();
          container.appendChild(inp);
        });
      });
    }
  })();
