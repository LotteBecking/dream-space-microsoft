(function(){
  var stepCount = 8;
  var btn = document.getElementById('add-step-btn');
  if (btn) btn.addEventListener('click', function() {
    stepCount++;
    var c = document.getElementById('steps-container');
    var row = document.createElement('div');
    row.className = 'step-row';
    row.innerHTML = '<span class="step-index">' + stepCount + '</span>' +
      '<input type="text" name="step_' + stepCount + '" class="input" placeholder="..." />';
    c.appendChild(row);
  });
})();
