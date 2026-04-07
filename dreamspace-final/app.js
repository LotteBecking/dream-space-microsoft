const app = document.getElementById('app');

const state = {
  screen: 'welcome',
  selectedAnswer: null,
  answerResult: null,
  activeLessonId: null,
  profile: { why: null, level: null, commitment: null },
  completedLessons: [],
  xp: 180,
  streak: 7,
  gems: 120,
  hearts: 5,
  reflections: {},
  game: null,
};

const whyOptions = [
  ['I want to help people'],
  ['I like puzzles'],
  ['I want cool skills'],
  ['I care about privacy'],
  ['I want to build apps'],
  ['I want to spot fake stuff'],
  ['I like being creative'],
  ['I want to make AI fair'],
];

const levels = ['I am brand new', 'I know a little', 'I feel pretty good', 'I want a big challenge'];
const commitments = [
  ['5 min a day', 'Tiny steps'],
  ['15 min a day', 'Good pace'],
  ['30 min a day', 'Let’s go'],
  ['60 min a day', 'Space mode'],
];

const benefits = [
  ['Play with purpose', 'Each world teaches computational thinking through a bigger mission.'],
  ['Unlock smarter tools', 'Hints, upgrades, and creation modes keep the game moving.'],
  ['Build for real life', 'Protect privacy, fix systems, spot falsehoods, test fairness, and invent.'],
];

const lessons = [
  {
    id: 1,
    title: 'Firewall Run',
    short: 'Defend the city',
    concept: 'Classification · Conditions · Variables',
    value: 'Privacy and personal data protection',
    mapY: 120,
    theme: 'cyber',
    introBubble: 'Trackers are rushing the city gates. Build firewall rules before the data core leaks.',
    learn: 'Sort requests, decide what is necessary, and build privacy rules that protect the whole city.',
    status() { return getLessonStatus(1); },
  },
  {
    id: 2,
    title: 'Metro Mind',
    short: 'Repair systems',
    concept: 'Sequencing · Debugging · Decomposition',
    value: 'Civic problem-solving and public service design',
    mapY: 245,
    theme: 'city',
    introBubble: 'The city network is jammed. Repair routes, remove bugs, and keep the district moving.',
    learn: 'Break city problems into steps, place them in the right order, and debug systems that waste time.',
    status() { return getLessonStatus(2); },
  },
  {
    id: 3,
    title: 'Signal Detectives',
    short: 'Solve media cases',
    concept: 'Pattern recognition · Classification · Logic testing',
    value: 'Misinformation awareness and digital citizenship',
    mapY: 380,
    theme: 'mystery',
    introBubble: 'False signals are spreading. Collect clues, verify evidence, and stop bad info before it spreads.',
    learn: 'Investigate suspicious content, test trust signals, and build a repeatable truth-check routine.',
    status() { return getLessonStatus(3); },
  },
  {
    id: 4,
    title: 'Algorithm Arena',
    short: 'Balance the system',
    concept: 'Abstraction · Classification · Rule testing',
    value: 'Responsible AI, fairness, and inclusion',
    mapY: 515,
    theme: 'arena',
    introBubble: 'A powerful decision engine is unfair. Run simulations, diagnose bias, and rebalance the arena.',
    learn: 'See how rules shape outcomes, test what changes results, and redesign systems so they treat people better.',
    status() { return getLessonStatus(4); },
  },
  {
    id: 5,
    title: 'Dreamspace Lab',
    short: 'Invent for good',
    concept: 'Decomposition · Functions · Logic flow',
    value: 'Civic tech and meaningful innovation',
    mapY: 650,
    theme: 'lab',
    introBubble: 'You have unlocked the makerspace. Assemble a tech-for-good invention and test it live.',
    learn: 'Choose a real-world problem, combine modules into a logic flow, and build a useful prototype.',
    status() { return getLessonStatus(5); },
  },
];

function getLessonStatus(id) {
  if (state.completedLessons.includes(id)) return 'completed';
  const locked = lessons.filter(l => !state.completedLessons.includes(l.id));
  const nextId = locked.length ? Math.min(...locked.map(l => l.id)) : 5;
  return id === nextId ? 'current' : 'locked';
}

function currentLesson() {
  return lessons.find(l => l.id === state.activeLessonId);
}

function backdrop(){ return `<div class="backdrop"></div>`; }
function mascot(size='') {
  return `<div class="mascot-wrap"><img class="mascot ${size}" src="assets/space-beaver.png" alt="Space Beaver"></div>`;
}
function footerCTA(label, action, alt = false, disabled = false) {
  return `<div class="footer-cta"><div class="inner"><button class="primary ${alt ? 'alt' : ''}" data-go="${action}" ${disabled ? 'disabled' : ''}>${label}</button></div></div>`;
}
function topbar(progress, backTo = null, showClose = false) {
  return `<div class="topbar">
    <button class="circle-btn" ${backTo ? `data-go="${backTo}"` : ''}>${backTo ? '←' : '•'}</button>
    ${showClose ? `<button class="circle-btn" data-go="journey">×</button>` : ''}
    <div class="progress"><span style="width:${progress}%"></span></div>
  </div>`;
}
function roadSvg(){
  return `<svg class="road-svg" viewBox="0 0 350 720" preserveAspectRatio="none" aria-hidden="true">
    <path class="road-fill" d="M176 92 C252 130, 232 196, 160 245 S104 326, 184 382 S266 482, 150 520 S72 606, 180 650" />
    <path class="road-mid" d="M176 92 C252 130, 232 196, 160 245 S104 326, 184 382 S266 482, 150 520 S72 606, 180 650" />
    <path class="road-dash" d="M176 92 C252 130, 232 196, 160 245 S104 326, 184 382 S266 482, 150 520 S72 606, 180 650" />
  </svg>`;
}
function lessonNodeX(index) { return [176, 235, 120, 245, 160][index]; }

function lessonMap(){
  return `<div class="map-stage">
      ${roadSvg()}
      ${lessons.map((lesson, index) => {
        const status = lesson.status();
        const clickable = status !== 'locked';
        return `<div class="lesson-dot" style="left:${lessonNodeX(index)}px; top:${lesson.mapY}px;">
            <button class="lesson-node ${status}" ${clickable ? `data-lesson="${lesson.id}"` : ''} aria-label="${lesson.title}">
              <img src="assets/space-beaver.png" alt="">
            </button>
            <div class="lesson-label"><strong>${lesson.title}</strong>${status === 'current' ? 'Tap to play' : status === 'locked' ? 'Locked' : 'Done'}</div>
          </div>`;
      }).join('')}
    </div>`;
}

function renderWelcome() {
  return `${backdrop()}<section class="hero"><div class="hero-content">
      <div class="pixel-chip">DREAM SPACE QUEST</div>
      <div class="logo-box">
        <img class="mascot mascot-lg" src="assets/space-beaver.png" alt="Space Beaver">
        <div><h1 class="title">Dreaming in Space</h1><p class="subtitle">Five game worlds. Real digital skills. Tech for good.</p></div>
      </div>
      <div class="hero-panels">
        <div class="feature"><div class="mini"></div><strong>Defend</strong><span>Protect data and people</span></div>
        <div class="feature"><div class="mini"></div><strong>Investigate</strong><span>Repair, verify, and test</span></div>
        <div class="feature"><div class="mini"></div><strong>Invent</strong><span>Build tools that help</span></div>
      </div>
      <button class="primary" data-go="why">Start mission</button>
    </div></section>`;
}

function renderChoiceScreen(title, options, progress, prev, next) {
  return `${backdrop()}<section class="screen">${topbar(progress, prev)}
    <div class="speech-row">${mascot()}<div class="bubble">${title}</div></div>
    <div class="option-grid">${options.map(([label, meta]) => `
      <button class="card option-card" data-go="${next}" data-value="${label}">
        <div class="icon"></div>
        <div><div class="label">${label}</div>${meta ? `<div class="meta">${meta}</div>` : ''}</div>
      </button>`).join('')}</div>
    ${footerCTA('Next', next, true)}
  </section>`;
}

function renderSummary() {
  return `${backdrop()}<section class="screen">${topbar(100,'commitment')}
    <div class="speech-row">${mascot()}<div class="bubble">You are ready for five mission worlds.</div></div>
    <div class="summary-list">${benefits.map(([title,desc]) => `
      <div class="card summary-item"><div class="icon"><img class="mascot" src="assets/space-beaver.png" alt=""></div><div><h3>${title}</h3><p>${desc}</p></div></div>`).join('')}</div>
    ${footerCTA('Go to map','journey')}
  </section>`;
}

function renderJourney() {
  const completedCount = state.completedLessons.length;
  return `${backdrop()}<section class="home">
      <div class="home-header">
        <div class="row"><div class="brand">Dream Space</div><div class="header-mascot">${mascot()}</div></div>
        <div class="stats">
          <div class="stat">Streak<br><strong>${state.streak}</strong></div>
          <div class="stat">HP<br><strong>${state.hearts}</strong></div>
          <div class="stat">Gems<br><strong>${state.gems}</strong></div>
          <div class="stat">XP<br><strong>${state.xp}</strong></div>
        </div>
      </div>
      <div class="home-main">
        <div class="panel-grid">
          <div class="panel"><h4>Mission path</h4><p>${completedCount}/5 worlds cleared</p><div class="bar"><span style="width:${completedCount*20}%"></span></div><p>Each world has a different game mechanic.</p></div>
          <div class="panel"><h4>Core purpose</h4><p>Use computational thinking to protect, question, balance, and build for good.</p></div>
        </div>
        <div class="map-shell">
          <div style="text-align:center"><div class="map-chip">5 take-home game lessons</div></div>
          <h2 class="map-title">Mission Worlds</h2>
          <div class="speech-row">${mascot()}<div class="bubble">Blue worlds are unlocked. Finish one to open the next.</div></div>
          ${lessonMap()}
        </div>
      </div>
      <div class="bottom-nav"><div class="inner">
        <button class="nav-btn active">Journey</button><button class="nav-btn">Review</button><button class="nav-btn">Build</button><button class="nav-btn">Goals</button><button class="nav-btn">Profile</button>
      </div></div>
    </section>`;
}

function renderLessonIntro() {
  const lesson = currentLesson();
  return `${backdrop()}<section class="screen lesson-screen">${topbar(10,'journey',true)}
    <div class="speech-row">${mascot()}<div class="bubble">${lesson.introBubble}</div></div>
    <div class="question">
      <div class="pill">${lesson.value}</div>
      <h2>${lesson.title}</h2>
      <p><strong>${lesson.concept}</strong></p>
      <p style="margin-top:10px">${lesson.learn}</p>
    </div>
    <div class="card mission-card">
      <h3>World loop</h3>
      <ul class="mission-list"><li>Learn the mission</li><li>Play the system</li><li>Unlock a final creator mode</li></ul>
    </div>
    ${footerCTA('Enter world','lesson-play')}
  </section>`;
}

function initGame(id) {
  if (id === 1) {
    state.game = {
      type: 'firewall',
      round: 0,
      cityHealth: 3,
      score: 0,
      requests: [
        { app: 'Map app', ask: 'Location while using', rule: 'limited', risk: 'low', icon: '🗺️' },
        { app: 'Flashlight app', ask: 'Contacts list', rule: 'deny', risk: 'high', icon: '🔦' },
        { app: 'School portal', ask: 'Name and class', rule: 'allow', risk: 'low', icon: '🏫' },
      ],
      current: null,
      complete: false,
      history: [],
    };
    state.game.current = state.game.requests[0];
  }
  if (id === 2) {
    state.game = {
      type: 'metro',
      scenario: 'Repair the emergency route: get medicine from depot to clinic with no wasted stops.',
      pieces: ['Start at depot', 'Pass the school', 'Turn at the clinic road', 'Deliver at clinic'],
      correct: ['Start at depot', 'Pass the school', 'Turn at the clinic road', 'Deliver at clinic'],
      complete: false,
    };
    state.game.pieces = ['Turn at the clinic road', 'Deliver at clinic', 'Start at depot', 'Pass the school'];
  }
  if (id === 3) {
    state.game = {
      type: 'signal',
      caseTitle: 'Viral Storm Case',
      cluePool: [
        { text: 'No source is named', good: true, icon: '📎' },
        { text: 'Image date does not match the claim', good: true, icon: '🖼️' },
        { text: 'It has many likes', good: false, icon: '❤️' },
        { text: 'The headline uses panic words', good: true, icon: '⚠️' },
        { text: 'A friend shared it', good: false, icon: '👥' },
      ],
      selected: [],
      verdict: null,
      complete: false,
    };
  }
  if (id === 4) {
    state.game = {
      type: 'arena',
      rule: 'postcode',
      transparency: false,
      review: false,
      fairness: 34,
      profiles: [
        { name: 'Amina', skill: 'high', postcode: 'outer zone', result: null },
        { name: 'Milan', skill: 'high', postcode: 'city core', result: null },
      ],
      complete: false,
    };
    recalcArena();
  }
  if (id === 5) {
    state.game = {
      type: 'lab',
      mission: 'Build a tool that helps students check if a post is trustworthy.',
      input: null,
      rule: null,
      output: null,
      launched: false,
      complete: false,
    };
  }
}

function renderLessonPlay() {
  const lesson = currentLesson();
  if (!state.game) initGame(lesson.id);
  const progress = 50;
  const body = lesson.id === 1 ? renderFirewallRun()
    : lesson.id === 2 ? renderMetroMind()
    : lesson.id === 3 ? renderSignalDetectives()
    : lesson.id === 4 ? renderAlgorithmArena()
    : renderDreamspaceLab();
  return `${backdrop()}<section class="screen lesson-screen">${topbar(progress,'journey',true)}${body}</section>`;
}

function renderFirewallRun() {
  const g = state.game;
  const r = g.current;
  const completed = g.round >= g.requests.length;
  if (completed && !g.complete) g.complete = true;
  return `
    <div class="speech-row">${mascot()}<div class="bubble">Sort each request through your firewall. Keep the city core safe.</div></div>
    <div class="question game-panel">
      <div class="pill">Firewall health</div>
      <div class="stat-row"><div class="tiny-stat">Core HP <strong>${'🛡️'.repeat(g.cityHealth)}</strong></div><div class="tiny-stat">Safe calls <strong>${g.score}</strong></div></div>
      ${g.complete ? `<h2>Firewall secured</h2><p>You defended the city by using smart privacy rules.</p>` : `
        <h2>${r.icon} ${r.app}</h2>
        <p>This request wants: <strong>${r.ask}</strong></p>
        <p>Choose the best firewall rule.</p>
        <div class="lane-grid">
          <button class="card game-card" data-action="firewall-choice" data-choice="allow"><strong>ALLOW</strong><span>Safe and needed</span></button>
          <button class="card game-card" data-action="firewall-choice" data-choice="limited"><strong>LIMIT</strong><span>Only while needed</span></button>
          <button class="card game-card" data-action="firewall-choice" data-choice="deny"><strong>DENY</strong><span>Too risky or unnecessary</span></button>
        </div>
        <div class="hint-box">Hint: necessary data and unnecessary data should not pass the same way.</div>`}
    </div>
    <div class="card mission-card"><h3>Request log</h3>${g.history.length ? g.history.map(h => `<div class="log-item">${h}</div>`).join('') : '<p>No requests processed yet.</p>'}</div>
    ${g.complete ? footerCTA('Unlock creator mode','lesson-apply') : ''}`;
}

function renderMetroMind() {
  const g = state.game;
  const orderOk = JSON.stringify(g.pieces) === JSON.stringify(g.correct);
  if (orderOk) g.complete = true;
  return `
    <div class="speech-row">${mascot()}<div class="bubble">Rebuild the route in the best order. Shorter, cleaner, safer.</div></div>
    <div class="question game-panel">
      <div class="pill">Emergency route repair</div>
      <h2>Metro Mind</h2>
      <p>${g.scenario}</p>
      <div class="sequence-list">${g.pieces.map((piece, i) => `
        <div class="sequence-item">
          <div class="sequence-text"><span class="pill">Step ${i + 1}</span>${piece}</div>
          <div class="sequence-controls">
            <button class="circle-btn small" data-action="move-seq" data-index="${i}" data-dir="up">↑</button>
            <button class="circle-btn small" data-action="move-seq" data-index="${i}" data-dir="down">↓</button>
          </div>
        </div>`).join('')}</div>
      <div class="hint-box">Hint: think about the start point, the key turn, and the final delivery.</div>
      ${g.complete ? `<div class="success-banner">Route fixed. You debugged the city system.</div>` : ''}
    </div>
    <div class="card mission-card"><h3>Why this teaches CT</h3><p>You are sequencing steps, testing the route, and debugging wasted moves.</p></div>
    ${g.complete ? footerCTA('Unlock creator mode','lesson-apply') : ''}`;
}

function renderSignalDetectives() {
  const g = state.game;
  const selectedCount = g.selected.length;
  const enoughClues = selectedCount >= 3;
  return `
    <div class="speech-row">${mascot()}<div class="bubble">Build a case board. Collect the clues that actually help verify truth.</div></div>
    <div class="question game-panel">
      <div class="pill">Case file: ${g.caseTitle}</div>
      <h2>Signal Detectives</h2>
      <p>A post claims a dangerous event happened today. Pick the clues that help test whether it is trustworthy.</p>
      <div class="clue-grid">${g.cluePool.map((clue, i) => {
        const active = g.selected.includes(i);
        return `<button class="card clue-card ${active ? 'selected' : ''}" data-action="toggle-clue" data-index="${i}"><strong>${clue.icon} ${clue.text}</strong><span>${active ? 'On case board' : 'Tap to investigate'}</span></button>`;
      }).join('')}</div>
      <div class="hint-box">Good detectives look for source, timing, evidence, and repeated warning signs.</div>
    </div>
    <div class="card mission-card"><h3>Case board</h3>${selectedCount ? g.selected.map(i => `<div class="log-item">• ${g.cluePool[i].text}</div>`).join('') : '<p>No clues selected yet.</p>'}</div>
    ${enoughClues ? footerCTA('Submit verdict','signal-submit') : ''}`;
}

function recalcArena() {
  const g = state.game;
  g.profiles.forEach(p => {
    if (g.rule === 'postcode') {
      p.result = p.postcode === 'city core' ? 'selected' : 'rejected';
    } else {
      p.result = p.skill === 'high' ? 'selected' : 'rejected';
    }
  });
  let fairness = g.rule === 'skills' ? 72 : 34;
  if (g.transparency) fairness += 12;
  if (g.review) fairness += 16;
  g.fairness = Math.min(100, fairness);
  g.complete = g.fairness >= 90;
}

function renderAlgorithmArena() {
  const g = state.game;
  return `
    <div class="speech-row">${mascot()}<div class="bubble">Run tests, compare outcomes, and raise the fairness score without breaking the system.</div></div>
    <div class="question game-panel">
      <div class="pill">Fairness engine</div>
      <h2>Algorithm Arena</h2>
      <div class="fairness-meter"><span style="width:${g.fairness}%"></span></div>
      <p>Fairness score: <strong>${g.fairness}</strong></p>
      <div class="toggle-row">
        <button class="card game-card ${g.rule === 'postcode' ? 'selected' : ''}" data-action="set-rule" data-rule="postcode"><strong>Rule: postcode</strong><span>Fast but unfair</span></button>
        <button class="card game-card ${g.rule === 'skills' ? 'selected' : ''}" data-action="set-rule" data-rule="skills"><strong>Rule: project skills</strong><span>Relevant evidence</span></button>
        <button class="card game-card ${g.transparency ? 'selected' : ''}" data-action="toggle-arena" data-key="transparency"><strong>Explain result</strong><span>Add transparency</span></button>
        <button class="card game-card ${g.review ? 'selected' : ''}" data-action="toggle-arena" data-key="review"><strong>Human review</strong><span>Allow appeals</span></button>
      </div>
      <div class="profile-grid">${g.profiles.map(p => `<div class="card profile-card"><strong>${p.name}</strong><span>Skill: ${p.skill}</span><span>Area: ${p.postcode}</span><span>Result: ${p.result}</span></div>`).join('')}</div>
      <div class="hint-box">Hint: unfair variables lower trust. Relevant evidence and review raise it.</div>
      ${g.complete ? `<div class="success-banner">Arena stabilized. Your redesign is fair enough to pass.</div>` : ''}
    </div>
    ${g.complete ? footerCTA('Unlock creator mode','lesson-apply') : ''}`;
}

function renderDreamspaceLab() {
  const g = state.game;
  const complete = g.input && g.rule && g.output && g.launched;
  if (complete) g.complete = true;
  return `
    <div class="speech-row">${mascot()}<div class="bubble">Choose modules and launch a mini tool that helps real people.</div></div>
    <div class="question game-panel">
      <div class="pill">Makerspace contract</div>
      <h2>Dreamspace Lab</h2>
      <p>${g.mission}</p>
      <div class="builder-grid">
        <div class="card build-slot"><h3>Input</h3>
          <button class="mini-choice ${g.input === 'claim' ? 'on' : ''}" data-action="set-build" data-slot="input" data-value="claim">Claim/post</button>
          <button class="mini-choice ${g.input === 'photo' ? 'on' : ''}" data-action="set-build" data-slot="input" data-value="photo">Photo</button>
        </div>
        <div class="card build-slot"><h3>Rule</h3>
          <button class="mini-choice ${g.rule === 'source-check' ? 'on' : ''}" data-action="set-build" data-slot="rule" data-value="source-check">Check source + date</button>
          <button class="mini-choice ${g.rule === 'popularity' ? 'on' : ''}" data-action="set-build" data-slot="rule" data-value="popularity">Trust popularity</button>
        </div>
        <div class="card build-slot"><h3>Output</h3>
          <button class="mini-choice ${g.output === 'warning' ? 'on' : ''}" data-action="set-build" data-slot="output" data-value="warning">Warning + advice</button>
          <button class="mini-choice ${g.output === 'instant-share' ? 'on' : ''}" data-action="set-build" data-slot="output" data-value="instant-share">Instant share</button>
        </div>
      </div>
      <div class="hint-box">Good tools need the right input, a fair rule, and a helpful output.</div>
      <button class="primary" data-action="launch-build" ${g.input && g.rule && g.output ? '' : 'disabled'}>Launch prototype</button>
      ${g.launched ? `<div class="success-banner ${g.complete ? '' : 'warning'}">${g.complete ? 'Prototype works. You built a tool for good.' : 'Prototype failed. One module is unsafe or unhelpful.'}</div>` : ''}
    </div>
    ${g.complete ? footerCTA('Unlock creator mode','lesson-apply') : ''}`;
}

function renderApply() {
  const lesson = currentLesson();
  const prompts = {
    1: 'Design your own firewall rule: what should happen when an app asks for data it does not need?',
    2: 'Create one smarter city upgrade: what system would you improve next and why?',
    3: 'Write your truth protocol: what 3 checks should every detective do before sharing?',
    4: 'Redesign the arena: what fairness rule should all high-stakes systems follow?',
    5: 'Name your invention: who does it help and what problem does it solve?'
  };
  return `${backdrop()}<section class="screen lesson-screen">${topbar(86,'journey',true)}
    <div class="speech-row">${mascot()}<div class="bubble">Creator mode unlocked. Now use what you learned in your own way.</div></div>
    <div class="question"><div class="pill">Creator mode</div><h2>${lesson.title}</h2><p>${prompts[lesson.id]}</p></div>
    <div class="card mission-card"><h3>Try one idea</h3><textarea class="reflection-box" id="reflectionBox" placeholder="Write a short idea here...">${state.reflections[lesson.id] || ''}</textarea></div>
    ${footerCTA('Finish world','complete-world')}
  </section>`;
}

function renderComplete() {
  const lesson = currentLesson();
  return `${backdrop()}<section class="screen lesson-screen">${topbar(100,'journey',true)}
    <div class="speech-row">${mascot()}<div class="bubble">World cleared! You played a system, learned a skill, and unlocked a creator move.</div></div>
    <div class="question"><div class="pill">Mission complete</div><h2>${lesson.title}</h2><p>${lesson.value}</p></div>
    <div class="card mission-card"><h3>What you practiced</h3><p>${lesson.concept}</p><h3 style="margin-top:14px">XP gained</h3><p>+90 XP and +25 gems</p></div>
    ${footerCTA('Back to map','journey')}
  </section>`;
}

function render() {
  if (state.screen === 'welcome') app.innerHTML = renderWelcome();
  if (state.screen === 'why') app.innerHTML = renderChoiceScreen('Why do you want to learn with Dream Space?', whyOptions, 25, 'welcome', 'level');
  if (state.screen === 'level') app.innerHTML = renderChoiceScreen('How much do you know right now?', levels.map(v => [v, '']), 50, 'why', 'commitment');
  if (state.screen === 'commitment') app.innerHTML = renderChoiceScreen('How much time can you play at home?', commitments, 75, 'level', 'summary');
  if (state.screen === 'summary') app.innerHTML = renderSummary();
  if (state.screen === 'journey') app.innerHTML = renderJourney();
  if (state.screen === 'lesson-intro') app.innerHTML = renderLessonIntro();
  if (state.screen === 'lesson-play') app.innerHTML = renderLessonPlay();
  if (state.screen === 'lesson-apply') app.innerHTML = renderApply();
  if (state.screen === 'lesson-complete') app.innerHTML = renderComplete();
  bindEvents();
}

function startLesson(id) {
  state.activeLessonId = id;
  state.selectedAnswer = null;
  state.answerResult = null;
  state.game = null;
  state.screen = 'lesson-intro';
  render();
}

function finishLesson() {
  const id = state.activeLessonId;
  if (!state.completedLessons.includes(id)) {
    state.completedLessons.push(id);
    state.completedLessons.sort((a, b) => a - b);
    state.xp += 90;
    state.gems += 25;
  }
  state.screen = 'lesson-complete';
  render();
}

function handleFirewallChoice(choice) {
  const g = state.game;
  const r = g.current;
  const ok = choice === r.rule;
  if (ok) g.score += 1; else g.cityHealth = Math.max(0, g.cityHealth - 1);
  g.history.unshift(`${r.icon} ${r.app}: ${choice.toUpperCase()} ${ok ? '✓' : '✗'}`);
  g.round += 1;
  if (g.round < g.requests.length) g.current = g.requests[g.round];
  else g.complete = true;
  render();
}

function moveSequence(index, dir) {
  const g = state.game;
  const swap = dir === 'up' ? index - 1 : index + 1;
  if (swap < 0 || swap >= g.pieces.length) return;
  [g.pieces[index], g.pieces[swap]] = [g.pieces[swap], g.pieces[index]];
  render();
}

function toggleClue(index) {
  const g = state.game;
  if (g.selected.includes(index)) g.selected = g.selected.filter(i => i !== index);
  else g.selected.push(index);
  render();
}

function evaluateSignalCase() {
  const g = state.game;
  const correctSet = g.cluePool.map((c, i) => c.good ? i : null).filter(i => i !== null);
  const chosen = [...g.selected].sort((a, b) => a - b);
  const correct = JSON.stringify(chosen) === JSON.stringify(correctSet);
  if (!correct && !g.selected.some(i => g.cluePool[i].good)) return;
  g.complete = true;
  state.screen = 'lesson-apply';
  render();
}

function setArenaRule(rule) {
  state.game.rule = rule;
  recalcArena();
  render();
}

function toggleArena(key) {
  state.game[key] = !state.game[key];
  recalcArena();
  render();
}

function setBuild(slot, value) {
  state.game[slot] = value;
  state.game.launched = false;
  render();
}

function launchBuild() {
  const g = state.game;
  g.launched = true;
  g.complete = g.input === 'claim' && g.rule === 'source-check' && g.output === 'warning';
  render();
}

function bindEvents() {
  document.querySelectorAll('[data-go]').forEach(btn => {
    btn.addEventListener('click', () => {
      const next = btn.getAttribute('data-go');
      const value = btn.getAttribute('data-value');
      if (value) {
        if (state.screen === 'why') state.profile.why = value;
        if (state.screen === 'level') state.profile.level = value;
        if (state.screen === 'commitment') state.profile.commitment = value;
      }
      if (next === 'signal-submit') {
        evaluateSignalCase();
        return;
      }
      if (next === 'complete-world') {
        const box = document.getElementById('reflectionBox');
        if (box) state.reflections[state.activeLessonId] = box.value;
        finishLesson();
        return;
      }
      state.selectedAnswer = null;
      state.answerResult = null;
      state.screen = next;
      render();
    });
  });

  document.querySelectorAll('[data-lesson]').forEach(btn => {
    btn.addEventListener('click', () => startLesson(Number(btn.getAttribute('data-lesson'))));
  });

  document.querySelectorAll('[data-action="firewall-choice"]').forEach(btn => {
    btn.addEventListener('click', () => handleFirewallChoice(btn.getAttribute('data-choice')));
  });
  document.querySelectorAll('[data-action="move-seq"]').forEach(btn => {
    btn.addEventListener('click', () => moveSequence(Number(btn.getAttribute('data-index')), btn.getAttribute('data-dir')));
  });
  document.querySelectorAll('[data-action="toggle-clue"]').forEach(btn => {
    btn.addEventListener('click', () => toggleClue(Number(btn.getAttribute('data-index'))));
  });
  document.querySelectorAll('[data-action="set-rule"]').forEach(btn => {
    btn.addEventListener('click', () => setArenaRule(btn.getAttribute('data-rule')));
  });
  document.querySelectorAll('[data-action="toggle-arena"]').forEach(btn => {
    btn.addEventListener('click', () => toggleArena(btn.getAttribute('data-key')));
  });
  document.querySelectorAll('[data-action="set-build"]').forEach(btn => {
    btn.addEventListener('click', () => setBuild(btn.getAttribute('data-slot'), btn.getAttribute('data-value')));
  });
  document.querySelectorAll('[data-action="launch-build"]').forEach(btn => {
    btn.addEventListener('click', launchBuild);
  });

}

render();
