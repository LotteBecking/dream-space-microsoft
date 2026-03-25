#!/usr/bin/env python3
"""
Regenerate intervention/schema.html from prototypes/backend/db/schema.sql.

Run from the intervention/ directory:
    python generate_schema_html.py
"""

import re
from pathlib import Path
from datetime import date

SCHEMA_SQL = Path(__file__).parent / "prototypes" / "backend" / "db" / "schema.sql"
OUTPUT_HTML = Path(__file__).parent / "schema.html"

# Tables that act as M:N junction bridges
JUNCTION_TABLES = {
    "student_achievements", "exercise_attempts",
    "challenge_results", "team_members",
}

# Per-group ERD layout and viewport height
GROUP_CONFIG = {
    "Teacher Dashboard": {"layout_direction": "LR", "height": 520},
    "Kids App":          {"layout_direction": "LR", "height": 560},
    "Auth / Shared":     {"layout_direction": "LR", "height": 420},
    "Other":             {"layout_direction": "LR", "height": 400},
}

# ── Zoom/pan JS (defined outside f-string to avoid brace-escaping) ─────────
ZOOM_PAN_JS = """<script>
(function () {
  function initViewport(viewport) {
    var scale = 1, tx = 0, ty = 0;
    var dragging = false, startX, startY, startTx, startTy;
    var svg = null;
    // Transform the wrapper div, never the SVG itself
    var xform = viewport.querySelector('.erd-transform');

    function applyTransform() {
      xform.style.transform = 'translate(' + tx + 'px,' + ty + 'px) scale(' + scale + ')';
      var label = viewport.parentElement.querySelector('.erd-zoom-label');
      if (label) label.textContent = Math.round(scale * 100) + '%';
    }

    function fitSvg() {
      if (!svg) return;
      // Use the SVG's declared width/height attributes (set by Mermaid to the
      // natural diagram size in CSS pixels, independent of any CSS transforms).
      var svgW = parseFloat(svg.getAttribute('width') || '0');
      var svgH = parseFloat(svg.getAttribute('height') || '0');
      if (svgW === 0 || svgH === 0) { setTimeout(fitSvg, 100); return; }
      var vw = viewport.clientWidth, vh = viewport.clientHeight;
      scale = Math.min(vw / svgW, vh / svgH) * 0.92;
      tx = (vw - svgW * scale) / 2;
      ty = (vh - svgH * scale) / 2;
      applyTransform();
    }

    // Zoom toward a point (cx, cy) in viewport coordinates
    function zoomAt(cx, cy, factor) {
      var ns = Math.min(Math.max(scale * factor, 0.05), 10);
      tx = cx - (cx - tx) * (ns / scale);
      ty = cy - (cy - ty) * (ns / scale);
      scale = ns;
      applyTransform();
    }

    viewport.addEventListener('wheel', function (e) {
      e.preventDefault();
      var rect = viewport.getBoundingClientRect();
      zoomAt(e.clientX - rect.left, e.clientY - rect.top, e.deltaY < 0 ? 1.12 : 1 / 1.12);
    }, { passive: false });

    viewport.addEventListener('mousedown', function (e) {
      if (e.button !== 0) return;
      dragging = true; startX = e.clientX; startY = e.clientY; startTx = tx; startTy = ty;
      viewport.classList.add('grabbing');
    });
    window.addEventListener('mousemove', function (e) {
      if (!dragging) return;
      tx = startTx + (e.clientX - startX); ty = startTy + (e.clientY - startY);
      applyTransform();
    });
    window.addEventListener('mouseup', function () {
      dragging = false; viewport.classList.remove('grabbing');
    });

    // Buttons zoom toward viewport center
    var p = viewport.parentElement;
    p.querySelector('.erd-zoom-in').addEventListener('click', function () {
      zoomAt(viewport.clientWidth / 2, viewport.clientHeight / 2, 1.3);
    });
    p.querySelector('.erd-zoom-out').addEventListener('click', function () {
      zoomAt(viewport.clientWidth / 2, viewport.clientHeight / 2, 1 / 1.3);
    });
    p.querySelector('.erd-reset').addEventListener('click', fitSvg);

    var obs = new MutationObserver(function () {
      var s = viewport.querySelector('svg');
      if (s && s !== svg) { svg = s; obs.disconnect(); setTimeout(fitSvg, 120); }
    });
    obs.observe(viewport, { childList: true, subtree: true });
    svg = viewport.querySelector('svg');
    if (svg) setTimeout(fitSvg, 120);
  }

  window.addEventListener('load', function () {
    document.querySelectorAll('.erd-viewport').forEach(initViewport);
  });
})();
</script>"""


def parse_tables(sql: str) -> list[dict]:
    """Extract table definitions from schema.sql."""
    tables = []
    pattern = re.compile(
        r"CREATE TABLE IF NOT EXISTS (\w+)\s*\((.*?)\);",
        re.DOTALL | re.IGNORECASE,
    )
    for match in pattern.finditer(sql):
        name = match.group(1)
        body = match.group(2)
        columns = []
        for line in body.splitlines():
            line = line.strip().rstrip(",")
            if not line or line.upper().startswith(("PRIMARY KEY (", "FOREIGN KEY", "UNIQUE", "CHECK")):
                continue
            col_match = re.match(r"(\w+)\s+(\w+)(.*)", line)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2)
                rest = col_match.group(3)
                is_pk = "PRIMARY KEY" in rest.upper()
                is_fk = "REFERENCES" in rest.upper()
                is_not_null = "NOT NULL" in rest.upper()
                is_unique = "UNIQUE" in rest.upper()
                default_match = re.search(r"DEFAULT\s+(\S+)", rest, re.IGNORECASE)
                default = default_match.group(1) if default_match else ""
                ref_match = re.search(r"REFERENCES\s+(\w+)\((\w+)\)", rest, re.IGNORECASE)
                ref = f"-> {ref_match.group(1)}.{ref_match.group(2)}" if ref_match else ""
                ref_table = ref_match.group(1) if ref_match else ""
                ref_col = ref_match.group(2) if ref_match else ""
                columns.append({
                    "name": col_name,
                    "type": col_type,
                    "pk": is_pk,
                    "fk": is_fk,
                    "not_null": is_not_null,
                    "unique": is_unique,
                    "default": default,
                    "ref": ref,
                    "ref_table": ref_table,
                    "ref_col": ref_col,
                })
        tables.append({"name": name, "columns": columns})
    return tables


def group_tables(tables: list[dict]) -> dict:
    teacher_names = {
        "teacher_profiles", "classes", "students", "achievements",
        "student_achievements", "activity_log", "lessons", "exercises",
        "assignments", "last_viewed_lessons", "class_codes", "exercise_attempts",
    }
    kids_names = {
        "teams", "team_members", "user_profiles", "challenges",
        "challenge_results", "user_tracking",
    }
    auth_names = {"accounts", "auth_sessions"}

    groups = {"Teacher Dashboard": [], "Kids App": [], "Auth / Shared": [], "Other": []}
    for t in tables:
        if t["name"] in teacher_names:
            groups["Teacher Dashboard"].append(t)
        elif t["name"] in kids_names:
            groups["Kids App"].append(t)
        elif t["name"] in auth_names:
            groups["Auth / Shared"].append(t)
        else:
            groups["Other"].append(t)
    return groups


def render_erd(tables: list[dict], all_table_names: set, layout_direction: str = "LR") -> str:
    """Generate Mermaid erDiagram text for the given tables."""
    init_line = (
        '%%{init: {"er": {"layoutDirection": "' + layout_direction + '", '
        '"diagramPadding": 20, "minEntityWidth": 100, "entityPadding": 10, "useMaxWidth": false}}}%%'
    )
    lines = [init_line, "erDiagram"]

    # Entity blocks
    for table in tables:
        lines.append(f"    {table['name']} {{")
        for col in table["columns"]:
            constraint = ""
            if col["pk"]:
                constraint = " PK"
            elif col["fk"]:
                constraint = " FK"
            elif col["unique"]:
                constraint = " UK"
            lines.append(f"        {col['type']} {col['name']}{constraint}")
        lines.append("    }")

    # Relationship lines
    seen = set()
    for table in tables:
        for col in table["columns"]:
            if col["ref_table"] and col["ref_table"] in all_table_names:
                ref_t = col["ref_table"]
                src_t = table["name"]
                label = col["name"]
                rel_key = f"{ref_t}->{src_t}"
                if rel_key not in seen:
                    seen.add(rel_key)
                    lines.append('    ' + ref_t + ' ||--o{ ' + src_t + ' : "' + label + '"')

    return "\n".join(lines)


def render_table(table: dict) -> str:
    is_junction = table["name"] in JUNCTION_TABLES
    junction_banner = ""
    if is_junction:
        junction_banner = (
            '\n    <div class="px-4 py-1 text-xs font-mono font-semibold '
            'bg-yellow-500/10 text-yellow-400 border-b border-white/10 tracking-wide">'
            'M:N junction \u2014 bridges two parent tables</div>'
        )

    rows = ""
    for col in table["columns"]:
        badges = ""
        if col["pk"]:
            badges += '<span class="badge pk">PK</span>'
        if col["fk"]:
            badges += (
                f'<span class="badge fk" title="{col["ref"]}">FK</span>'
                '<span class="badge card">N:1</span>'
            )
        if col["not_null"]:
            badges += '<span class="badge nn">NN</span>'
        if col["unique"]:
            badges += '<span class="badge uq">UQ</span>'
        default_cell = (
            f'<code class="text-orange-400 text-xs font-mono">{col["default"]}</code>'
            if col["default"] else ""
        )
        ref_cell = (
            f'<span class="ref whitespace-nowrap">{col["ref"]}</span>'
            if col["ref"] else ""
        )
        rows += f"""
        <tr class="border-t border-white/10 hover:bg-white/5 transition-colors">
          <td class="px-3 py-2 font-mono font-semibold text-white text-xs whitespace-nowrap">{col["name"]}</td>
          <td class="px-3 py-2 font-mono text-green-400 text-xs whitespace-nowrap">{col["type"]}</td>
          <td class="px-3 py-2 whitespace-nowrap">{badges}</td>
          <td class="px-3 py-2 whitespace-nowrap">{default_cell}</td>
          <td class="px-3 py-2 whitespace-nowrap">{ref_cell}</td>
        </tr>"""

    return f"""  <div class="rounded-xl overflow-hidden border border-white/10 bg-[#0F3460]">
    <div class="px-4 py-2.5 bg-[#16213e] border-b border-white/10 font-mono font-bold text-yellow-400 text-sm">{table["name"]}</div>{junction_banner}
    <div class="overflow-x-auto">
      <table class="w-full text-xs border-collapse">
        <thead>
          <tr class="bg-white/5">
            <th class="px-3 py-2 text-left text-white/40 font-semibold uppercase text-xs tracking-widest">Column</th>
            <th class="px-3 py-2 text-left text-white/40 font-semibold uppercase text-xs tracking-widest">Type</th>
            <th class="px-3 py-2 text-left text-white/40 font-semibold uppercase text-xs tracking-widest">Flags</th>
            <th class="px-3 py-2 text-left text-white/40 font-semibold uppercase text-xs tracking-widest">Default</th>
            <th class="px-3 py-2 text-left text-white/40 font-semibold uppercase text-xs tracking-widest">References</th>
          </tr>
        </thead>
        <tbody>{rows}
        </tbody>
      </table>
    </div>
  </div>"""


def render_group(
    group_name: str,
    tables: list[dict],
    color: str,
    all_table_names: set,
    note: str = "",
    layout_direction: str = "LR",
    height: int = 560,
) -> str:
    if not tables:
        return ""

    erd_text = render_erd(tables, all_table_names, layout_direction)
    cards = "\n".join(render_table(t) for t in tables)
    note_html = (
        f'<p class="text-sm text-white/50 mt-1 mb-5 pl-4">{note}</p>'
        if note else ""
    )

    return f"""
<section class="max-w-7xl mx-auto mb-20 px-4">
  <h2 class="text-sm font-black uppercase tracking-widest mb-1 pl-3"
      style="border-left: 4px solid {color}; color: {color}">
    {group_name}
    <span class="font-normal opacity-60 text-xs normal-case tracking-normal ml-1">({len(tables)} tables)</span>
  </h2>
  {note_html}

  <div class="rounded-xl border border-white/10 bg-[#0d1b2e] p-5 mb-6">
    <p class="text-xs text-white/30 uppercase tracking-widest mb-2 font-semibold">Entity Relationship Diagram</p>
    <div class="erd-controls" style="display:flex;gap:6px;margin-bottom:8px;align-items:center;">
      <button class="erd-btn erd-zoom-in" title="Zoom in">+</button>
      <button class="erd-btn erd-zoom-out" title="Zoom out">&minus;</button>
      <button class="erd-btn erd-reset" title="Reset view">&#8857;</button>
      <span class="erd-zoom-label" style="font-size:0.65rem;color:rgba(255,255,255,0.3);margin-left:4px;">100%</span>
    </div>
    <div class="erd-viewport" style="height:{height}px;overflow:hidden;position:relative;cursor:grab;">
      <div class="erd-transform" style="position:absolute;top:0;left:0;transform-origin:0 0;display:inline-block;">
        <div class="mermaid">
{erd_text}
        </div>
      </div>
    </div>
  </div>

  <p class="text-xs text-white/30 uppercase tracking-widest mb-3 font-semibold pl-1">Table Reference</p>
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
{cards}
  </div>
</section>"""


def generate_html(tables: list[dict]) -> str:
    groups = group_tables(tables)
    all_table_names = {t["name"] for t in tables}

    group_colors = {
        "Teacher Dashboard": "#7B4FA6",
        "Kids App": "#E91E8C",
        "Auth / Shared": "#FF6B35",
        "Other": "#888888",
    }
    group_notes = {
        "Kids App": (
            "These 6 tables are shared by <strong>both the iOS app (SwiftUI)</strong> and the "
            "<strong>Kids Web App</strong> — both clients connect to the same backend (port 5000) "
            "and the same SQLite database. There is no separate database per client."
        ),
    }

    sections = "".join(
        render_group(
            name, tbls,
            group_colors.get(name, "#888"),
            all_table_names,
            group_notes.get(name, ""),
            GROUP_CONFIG.get(name, {}).get("layout_direction", "TB"),
            GROUP_CONFIG.get(name, {}).get("height", 400),
        )
        for name, tbls in groups.items()
    )

    total = sum(len(t) for t in groups.values())
    today = date.today().strftime("%B %d, %Y")

    return f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DreamSpace Database Schema</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{}}
      }}
    }}
  </script>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {{
        background: '#0d1b2e',
        mainBkg: '#1a2744',
        nodeBorder: '#7B4FA6',
        lineColor: '#7B4FA6',
        textColor: '#F0F0F0',
        edgeLabelBackground: '#1a2744',
        attributeBackgroundColorOdd: '#0d1b2e',
        attributeBackgroundColorEven: '#16213e',
        fontSize: '14px',
      }},
      er: {{
        diagramPadding: 20,
        layoutDirection: 'LR',
        minEntityWidth: 100,
        minEntityHeight: 50,
        entityPadding: 10,
        useMaxWidth: false,
      }}
    }});
  </script>
  <style>
    body {{ background-color: #1A1A2E; color: #F0F0F0; }}
    .badge {{
      display: inline-block; font-size: 0.6rem; font-weight: 700;
      padding: 1px 5px; border-radius: 4px; margin-right: 2px; letter-spacing: 0.04em;
    }}
    .badge.pk   {{ background: rgba(255,215,0,0.2);    color: #FFD700; }}
    .badge.fk   {{ background: rgba(233,30,140,0.2);   color: #E91E8C; cursor: help; }}
    .badge.nn   {{ background: rgba(244,67,54,0.15);   color: #F44336; }}
    .badge.uq   {{ background: rgba(179,157,219,0.2);  color: #B39DDB; }}
    .badge.card {{ background: rgba(100,220,160,0.15); color: #64DCA0; }}
    .badge.mn   {{ background: rgba(255,180,50,0.18);  color: #FFB432; font-size: 0.55rem; }}
    .ref {{ font-size: 0.7rem; color: rgba(240,240,240,0.5); font-family: monospace; }}
    /* ERD viewport */
    .erd-viewport {{ touch-action: none; overflow: hidden; position: relative; }}
    .erd-viewport.grabbing {{ cursor: grabbing !important; }}
    .erd-transform {{ position: absolute; top: 0; left: 0; transform-origin: 0 0; display: inline-block; }}
    .erd-btn {{
      background: rgba(255,255,255,0.08); color: #F0F0F0;
      border: 1px solid rgba(255,255,255,0.15); border-radius: 5px;
      width: 26px; height: 26px; font-size: 15px; line-height: 1;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
      transition: background 0.15s; user-select: none; flex-shrink: 0;
    }}
    .erd-btn:hover {{ background: rgba(255,255,255,0.18); }}
  </style>
</head>
<body class="font-sans px-4 py-12">

<header class="text-center mb-16 max-w-2xl mx-auto">
  <h1 class="text-4xl font-black mb-3"
      style="background:linear-gradient(135deg,#7B4FA6,#E91E8C,#FF6B35);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">
    DreamSpace Database Schema
  </h1>
  <p class="text-white/40 text-sm">
    Generated from
    <code class="text-pink-400 font-mono">prototypes/backend/db/schema.sql</code>
    &middot; {today}
  </p>
  <div class="flex justify-center gap-5 mt-8 flex-wrap">
    <div class="bg-[#0F3460] border border-white/10 rounded-2xl px-8 py-4 text-center">
      <div class="text-3xl font-black text-purple-400">{total}</div>
      <div class="text-xs text-white/40 uppercase tracking-widest mt-1">Tables</div>
    </div>
    <div class="bg-[#0F3460] border border-white/10 rounded-2xl px-8 py-4 text-center">
      <div class="text-3xl font-black text-purple-400">SQLite</div>
      <div class="text-xs text-white/40 uppercase tracking-widest mt-1">Engine</div>
    </div>
    <div class="bg-[#0F3460] border border-white/10 rounded-2xl px-8 py-4 text-center">
      <div class="text-3xl font-black text-purple-400">1</div>
      <div class="text-xs text-white/40 uppercase tracking-widest mt-1">Shared DB</div>
    </div>
    <div class="bg-[#0F3460] border border-white/10 rounded-2xl px-8 py-4 text-center">
      <div class="text-3xl font-black text-purple-400">3</div>
      <div class="text-xs text-white/40 uppercase tracking-widest mt-1">Client Groups</div>
    </div>
  </div>
</header>

{sections}

<footer class="text-center text-white/25 text-xs mt-8 pb-10">
  DreamSpace &middot; Regenerate with
  <code class="font-mono text-pink-400">python generate_schema_html.py</code>
  from the <code class="font-mono text-white/40">intervention/</code> directory
</footer>
{ZOOM_PAN_JS}
</body>
</html>
"""


def main():
    sql = SCHEMA_SQL.read_text()
    tables = parse_tables(sql)
    html = generate_html(tables)
    OUTPUT_HTML.write_text(html)
    print(f"✅ Generated schema.html with {len(tables)} tables → {OUTPUT_HTML}")


if __name__ == "__main__":
    main()
