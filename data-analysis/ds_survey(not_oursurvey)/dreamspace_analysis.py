"""
dreamspace_analysis.py — DreamSpace NL Survey Analysis Dashboard
Usage: python dreamspace_analysis.py [Results.xlsx]
Output: dreamspace_report.html
"""

import sys
import subprocess
import importlib

# ── Self-installer ─────────────────────────────────────────────────────────────
REQUIRED = ["pandas", "numpy", "openpyxl", "plotly", "scipy", "seaborn", "matplotlib", "anthropic"]
OPTIONAL = ["wordcloud"]

def ensure_deps():
    for pkg in REQUIRED:
        mod = pkg.replace("-", "_")
        try:
            importlib.import_module(mod)
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg, "-q"])
    for pkg in OPTIONAL:
        try:
            importlib.import_module(pkg)
        except ImportError:
            print(f"  Optional '{pkg}' not found — word clouds will be skipped.")

ensure_deps()

# ── Imports ────────────────────────────────────────────────────────────────────
import os
import json
import html
import base64
import io
import argparse
import warnings
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats

warnings.filterwarnings("ignore")

try:
    from wordcloud import WordCloud
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False

# ── Palette & constants ────────────────────────────────────────────────────────
PALETTE = {
    "primary": "#7F77DD",
    "teal":    "#1D9E75",
    "amber":   "#EF9F27",
    "coral":   "#D85A30",
    "blue":    "#378ADD",
    "pink":    "#D4537E",
    "gray":    "#888780",
    "green":   "#639922",
    "bg":      "#FAFAF8",
    "card":    "#FFFFFF",
}

LIKERT_COLORS = ["#D85A30", "#EF9F27", "#888780", "#639922", "#1D9E75"]
SENTIMENT_COLORS = {
    "positive": "#1D9E75",
    "neutral":  "#888780",
    "negative": "#D85A30",
    "mixed":    "#EF9F27",
}
MIN_N = 5  # minimum rows needed to render a chart

PLOTLY_CFG = {"displayModeBar": False}

# Canonical column name → substring to match in actual columns
CANONICAL_MAP = {
    "start_time":     "시작 시간",
    "end_time":       "완료 시간",
    "location":       "Waar heb je vandaag",
    "role":           "Ben je een leerling",
    "educ_type":      "Welk type onderwijs",
    "age_po":         "Hoe oud ben jij?",
    "gender_po":      "Welke van deze past het beste bij jou?",
    "age_vo":         "Hoe oud ben jij?2",
    "gender_vo":      "Welke van deze past het beste bij jou?2",
    "tech_study":     "Ik wil later een technische studie",
    "age_mbo":        "Hoe oud ben jij?3",
    "gender_mbo":     "Hoe definieër jij jezelf",
    "workshop_s":     "Welke workshop heb je gevolgd?",
    "prev_programmed":"Heb je eerder geprogrammeerd",
    "prog_more":      "Zou je na vandaag vaker willen programmeren",
    "prev_minecraft": "Heb je eerder met Minecraft",
    "more_minecraft": "Zou je nu verder willen bouwen in Minecraft",
    "hacker_interest":"Heeft deze workshop je meer geïnteresseerd gemaakt om (ethisch) hacker",
    "drone_interest": "Ben je nu geïnteresseerd om vaker met drones",
    "datacenter_int": "Heb je interesse om later in een datacenter",
    "datacenter_text":"Wat spreekt je het meest aan in datacenters",
    "ai_interest":    "Na vandaag zou ik vaker met AI",
    "learning_gain":  "Ik weet nu meer over dit onderwerp",
    "enjoyment":      "Hoe leuk vond je de workshop",
    "best_parts":     "Wat vond je het leukste",
    "teacher_score":  "Hoe vond je de docent",
    "describe_ds":    "Beschrijf Dream Space",
    "proud":          "Ben je na vandaag trots",
    "tips":           "Heb je nog tips",
    # Teacher block
    "t_educ_level":   "In welk onderwijsniveau",
    "t_digi_known":   "Hoe bekend ben je met de conceptkerndoelen",
    "t_digi_prev":    "Heb je eerder lessen gegeven over digitale geletterdheid",
    "t_challenges":   "Ervaar je uitdagingen bij het lesgeven",
    "t_explain":      "Kun je dit kort toelichten",
    "t_workshop":     "Welke workshop heb je gevolgd?2",
    "t_use_workshop": "Ga je elementen uit de workshop gebruiken",
    "t_returning":    "Heb je eerder een Dream Space workshop gevolgd",
    "t_satisfaction": "Hoe tevreden ben je over jouw bezoek",
    "t_quality":      "Hoe beoordeel je de kwaliteit",
    "t_teacher":      "Hoe beoordeel je de docent",
    "t_nps":          "Hoe waarschijnlijk is het dat je Dream Space",
    "t_suggestions":  "Wat zou volgens jou beter kunnen",
    # OBA/TUMO
    "location_score": "Wat vond je van de locatie",
    "oba_aware":      "Heb je voor vandaag al gehoord van OBA",
    "oba_again":      "Ben je na vandaag van plan om mee te doen aan andere activiteiten van OBA",
    "tumo_interest":  "Lijkt het je leuk om mee te doen aan TUMO",
    "curious_topics": "Waar ben je nieuwsgierig naar",
}

# Human-readable English labels per canonical name
LABELS = {
    "location":       "Workshop location",
    "role":           "Student or teacher",
    "educ_type":      "Education level",
    "age_po":         "Age (primary school)",
    "gender_po":      "Gender (primary school)",
    "age_vo":         "Age (secondary school)",
    "gender_vo":      "Gender (secondary school)",
    "tech_study":     "Want to study tech later (VO)",
    "age_mbo":        "Age (MBO/HBO/WO)",
    "gender_mbo":     "Gender identity (MBO/HBO/WO)",
    "workshop_s":     "Workshop type",
    "prev_programmed":"Prior coding experience",
    "prog_more":      "Want to code more post-workshop",
    "prev_minecraft": "Prior Minecraft experience",
    "more_minecraft": "Want to continue Minecraft",
    "hacker_interest":"Interested in ethical hacking",
    "drone_interest": "Interested in drones",
    "datacenter_int": "Interested in datacenters",
    "datacenter_text":"What appeals about datacenters",
    "ai_interest":    "Want to work with AI more",
    "learning_gain":  "Knowledge gained",
    "enjoyment":      "Workshop enjoyment",
    "best_parts":     "What they enjoyed most (multi-select)",
    "teacher_score":  "Instructor rating",
    "describe_ds":    "Describe DreamSpace in one sentence",
    "proud":          "Self-pride after workshop",
    "tips":           "Tips & improvement feedback",
    "location_score": "Location rating",
    "oba_aware":      "Prior awareness of OBA / TUMO",
    "oba_again":      "Plans to join OBA activities",
    "tumo_interest":  "Interest in TUMO Amsterdam",
    "curious_topics": "Curious about (multi-select)",
    "t_educ_level":   "Education level taught",
    "t_digi_known":   "Familiarity with SLO digital literacy framework",
    "t_satisfaction": "Overall satisfaction with visit",
    "t_quality":      "Workshop quality rating",
    "t_teacher":      "Instructor quality rating",
    "t_nps":          "Likelihood to recommend",
    "t_suggestions":  "Workshop improvement suggestions",
}

DUTCH_LABELS = {
    "location":       "Waar heb je vandaag de workshop gevolgd?",
    "role":           "Ben je een leerling of docent?",
    "educ_type":      "Welk type onderwijs volg je?",
    "age_po":         "Hoe oud ben jij? (PO)",
    "gender_po":      "Welke van deze past het beste bij jou? (PO)",
    "age_vo":         "Hoe oud ben jij? (VO)",
    "gender_vo":      "Welke van deze past het beste bij jou? (VO)",
    "tech_study":     "Ik wil later een technische studie doen",
    "workshop_s":     "Welke workshop heb je gevolgd?",
    "prev_programmed":"Heb je eerder geprogrammeerd?",
    "prog_more":      "Zou je na vandaag vaker willen programmeren?",
    "learning_gain":  "Ik weet nu meer over dit onderwerp dan voor deze workshop",
    "enjoyment":      "Hoe leuk vond je de workshop?",
    "best_parts":     "Wat vond je het leukste aan deze workshop?",
    "teacher_score":  "Hoe vond je de docent",
    "describe_ds":    "Beschrijf Dream Space in één zin",
    "proud":          "Ben je na vandaag trots op jezelf?",
    "tips":           "Heb je nog tips voor ons? Wat mag beter of anders?",
    "location_score": "Wat vond je van de locatie?",
    "oba_aware":      "Heb je voor vandaag al gehoord van OBA of TUMO?",
    "oba_again":      "Ben je na vandaag van plan om mee te doen aan andere activiteiten van OBA?",
    "tumo_interest":  "Lijkt het je leuk om mee te doen aan TUMO Amsterdam?",
    "curious_topics": "Waar ben je nieuwsgierig naar?",
}

# ── Column mapping ─────────────────────────────────────────────────────────────
def make_col_map(df_cols):
    """Return {canonical: actual_col} by substring matching (strips \\xa0)."""
    cleaned = {c: c.replace('\xa0', ' ').strip() for c in df_cols}
    result = {}
    for canon, substr in CANONICAL_MAP.items():
        substr_clean = substr.replace('\xa0', ' ').strip()
        for actual, actual_clean in cleaned.items():
            if substr_clean.lower() in actual_clean.lower():
                if canon not in result:
                    result[canon] = actual
    return result

# ── Data loading ───────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    print(f"  Reading {path}...")
    df = pd.read_excel(path, engine="openpyxl")
    col_map = make_col_map(df.columns.tolist())

    # Rename to canonical names
    rename = {v: k for k, v in col_map.items() if v in df.columns}
    df = df.rename(columns=rename)

    # Parse datetimes
    for col in ["start_time", "end_time"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            if df[col].dt.tz is not None:
                df[col] = df[col].dt.tz_localize(None)

    # Duration in minutes
    if "start_time" in df.columns and "end_time" in df.columns:
        df["duration_min"] = (df["end_time"] - df["start_time"]).dt.total_seconds() / 60

    # Coerce Likert columns
    likert_cols = ["learning_gain", "enjoyment", "teacher_score", "proud",
                   "tech_study", "ai_interest", "location_score",
                   "t_satisfaction", "t_quality", "t_teacher", "t_nps", "t_digi_known"]
    for col in likert_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse multi-select columns
    for col in ["best_parts", "curious_topics"]:
        if col in df.columns:
            df[col] = df[col].fillna("").apply(
                lambda x: [s.strip() for s in str(x).split(";") if s.strip()]
            )
        else:
            df[col] = [[] for _ in range(len(df))]

    # Unified age and gender
    df["age"] = None
    if "age_po" in df.columns:
        df["age"] = pd.to_numeric(df.get("age_po"), errors="coerce")
    if "age_vo" in df.columns:
        df["age"] = df["age"].fillna(pd.to_numeric(df.get("age_vo"), errors="coerce"))

    df["gender"] = None
    if "gender_po" in df.columns:
        df["gender"] = df.get("gender_po")
    if "gender_vo" in df.columns:
        df["gender"] = df["gender"].fillna(df.get("gender_vo"))

    # ISO week
    if "start_time" in df.columns:
        df["iso_week"] = df["start_time"].dt.isocalendar().week.astype(int)
        df["date"] = df["start_time"].dt.date

    return df

# ── Helpers ────────────────────────────────────────────────────────────────────
def col_has_data(df, col, min_rows=1):
    return col in df.columns and df[col].notna().sum() >= min_rows

def n_label(n):
    return f"n = {n}"

def embed_plotly(fig) -> str:
    return fig.to_html(full_html=False, include_plotlyjs=False,
                       config=PLOTLY_CFG)

def embed_matplotlib(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor="white")
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    import matplotlib.pyplot as plt
    plt.close(fig)
    return f'<img src="data:image/png;base64,{b64}" style="max-width:100%;border-radius:8px">'

def placeholder_card(title, msg, dutch=""):
    dutch_html = f'<div class="dutch-label">{html.escape(dutch)}</div>' if dutch else ""
    return f"""
<div class="card placeholder-card">
  <div class="card-title">{html.escape(title)}</div>
  {dutch_html}
  <div class="placeholder-msg">{html.escape(msg)}</div>
</div>"""

def card(title, content, dutch="", badge="", n=None, chart_type=""):
    dutch_html = f'<div class="dutch-label">{html.escape(dutch)}</div>' if dutch else ""
    badge_html = f'<span class="badge">{html.escape(badge)}</span>' if badge else ""
    n_html = f'<span class="n-label">{n_label(n)}</span>' if n is not None else ""
    ct_html = f'<span class="chart-type">{html.escape(chart_type)}</span>' if chart_type else ""
    return f"""
<div class="card">
  <div class="card-header">
    <div class="card-title">{html.escape(title)} {badge_html}</div>
    <div class="card-meta">{n_html} {ct_html}</div>
  </div>
  {dutch_html}
  {content}
</div>"""

# ── Chart builders ─────────────────────────────────────────────────────────────
def chart_hbar(series: pd.Series, title: str, color=None) -> str:
    series = series.dropna().value_counts().sort_values()
    if len(series) == 0:
        return ""
    c = color or PALETTE["primary"]
    fig = go.Figure(go.Bar(
        x=series.values, y=series.index.astype(str),
        orientation="h",
        marker_color=c,
        text=series.values, textposition="outside",
    ))
    fig.update_layout(
        margin=dict(l=10, r=40, t=10, b=10),
        height=max(180, len(series) * 38),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(tickfont=dict(size=12)),
        showlegend=False,
    )
    return embed_plotly(fig)

def chart_donut(series: pd.Series, title: str, colors=None) -> str:
    vc = series.dropna().value_counts()
    if len(vc) == 0:
        return ""
    cols = colors or px.colors.qualitative.Set2
    fig = go.Figure(go.Pie(
        labels=vc.index.astype(str), values=vc.values,
        hole=0.45,
        marker=dict(colors=cols[:len(vc)]),
        textinfo="label+percent",
        textfont=dict(size=12),
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=280,
        showlegend=False,
        plot_bgcolor="white", paper_bgcolor="white",
    )
    return embed_plotly(fig)

def chart_vbar(series: pd.Series, color=None) -> str:
    vc = series.dropna().value_counts().sort_index()
    if len(vc) == 0:
        return ""
    c = color or PALETTE["blue"]
    fig = go.Figure(go.Bar(
        x=vc.index.astype(str), y=vc.values,
        marker_color=c,
        text=vc.values, textposition="outside",
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        height=260,
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(tickfont=dict(size=12)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0"),
        showlegend=False,
    )
    return embed_plotly(fig)

def chart_likert(series: pd.Series, label: str) -> str:
    """Single-row horizontal stacked bar for a 1-5 Likert question."""
    vc = series.dropna().astype(int).value_counts().reindex([1,2,3,4,5], fill_value=0)
    total = vc.sum()
    if total == 0:
        return ""
    pcts = (vc / total * 100).round(1)
    mean_val = series.dropna().mean()

    traces = []
    score_labels = ["1 – Very low", "2", "3 – Neutral", "4", "5 – Very high"]
    for i, score in enumerate([1,2,3,4,5]):
        cnt = vc[score]
        traces.append(go.Bar(
            name=str(score),
            x=[pcts[score]],
            y=[label],
            orientation="h",
            marker_color=LIKERT_COLORS[i],
            text=f"{cnt}" if cnt > 0 else "",
            textposition="inside",
            insidetextanchor="middle",
            hovertemplate=f"Score {score}: {cnt} ({pcts[score]}%)<extra></extra>",
        ))

    fig = go.Figure(traces)
    fig.update_layout(
        barmode="stack",
        margin=dict(l=10, r=80, t=10, b=10),
        height=80,
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(range=[0, 100], showgrid=False, showticklabels=False),
        yaxis=dict(showticklabels=False),
        legend=dict(orientation="h", y=-0.5, x=0),
        showlegend=True,
        annotations=[dict(
            x=103, y=0, text=f"<b>{mean_val:.2f}</b>",
            xref="x", yref="y",
            showarrow=False, font=dict(size=14, color=PALETTE["primary"]),
            xanchor="left",
        )],
    )
    return embed_plotly(fig)

def chart_multiselect(list_series: pd.Series, n_total: int) -> str:
    """Horizontal bar of multi-select tag frequencies."""
    all_tags = []
    for tags in list_series:
        if isinstance(tags, list):
            all_tags.extend(tags)
    if not all_tags:
        return ""
    from collections import Counter
    counts = Counter(all_tags)
    df_tags = pd.DataFrame(counts.items(), columns=["tag", "count"])
    df_tags["pct"] = (df_tags["count"] / n_total * 100).round(1)
    df_tags = df_tags.sort_values("count")

    fig = go.Figure(go.Bar(
        x=df_tags["count"], y=df_tags["tag"],
        orientation="h",
        marker_color=PALETTE["primary"],
        text=[f"{c} ({p}%)" for c, p in zip(df_tags["count"], df_tags["pct"])],
        textposition="outside",
    ))
    fig.update_layout(
        margin=dict(l=10, r=100, t=10, b=10),
        height=max(200, len(df_tags) * 34),
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(tickfont=dict(size=12)),
        showlegend=False,
    )
    return embed_plotly(fig)

def chart_wordcloud(text_series: pd.Series) -> str:
    if not HAS_WORDCLOUD:
        return ""
    texts = " ".join(text_series.dropna().astype(str).tolist())
    if len(texts) < 20:
        return ""
    try:
        wc = WordCloud(
            width=700, height=300,
            background_color="white",
            colormap="cool",
            regexp=r"\w+",
            collocations=False,
            max_words=80,
        ).generate(texts)
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        fig.patch.set_facecolor("white")
        return embed_matplotlib(fig)
    except Exception:
        return ""

# ── KPI computation ────────────────────────────────────────────────────────────
def compute_kpis(df) -> dict:
    kpis = {}
    kpis["total"] = len(df)

    enj = df["enjoyment"].dropna() if "enjoyment" in df.columns else pd.Series(dtype=float)
    kpis["enjoyment_mean"] = round(enj.mean(), 2) if len(enj) > 0 else None
    kpis["enjoyment_sd"]   = round(enj.std(), 2)  if len(enj) > 1 else None

    ts = df["teacher_score"].dropna() if "teacher_score" in df.columns else pd.Series(dtype=float)
    kpis["teacher_mean"] = round(ts.mean(), 2) if len(ts) > 0 else None

    if "prog_more" in df.columns:
        pm = df["prog_more"].dropna()
        kpis["prog_more_pct"] = round((pm == "Ja").mean() * 100, 1) if len(pm) > 0 else None
    else:
        kpis["prog_more_pct"] = None

    proud = df["proud"].dropna() if "proud" in df.columns else pd.Series(dtype=float)
    kpis["proud_mean"] = round(proud.mean(), 2) if len(proud) > 0 else None

    lg = df["learning_gain"].dropna() if "learning_gain" in df.columns else pd.Series(dtype=float)
    kpis["learning_mean"] = round(lg.mean(), 2) if len(lg) > 0 else None

    return kpis

# ── Insights computation ───────────────────────────────────────────────────────
def compute_insights(df, sentiment_results=None) -> dict:
    ins = {}

    # 1. Retention signal
    if col_has_data(df, "prog_more"):
        pm = df["prog_more"].dropna()
        pct = round((pm == "Ja").mean() * 100, 1)
        ins["retention"] = f"{pct}% of students want to code more after the workshop."
    else:
        ins["retention"] = "No data available for coding intent."

    # 2. Gender equity
    ins["gender_equity"] = None
    if col_has_data(df, "gender") and col_has_data(df, "prog_more"):
        gdf = df[["gender", "prog_more"]].dropna()
        gmap = {}
        for g, grp in gdf.groupby("gender"):
            gmap[g] = round((grp["prog_more"] == "Ja").mean() * 100, 1)
        if len(gmap) >= 2:
            sorted_g = sorted(gmap.items(), key=lambda x: x[1], reverse=True)
            gap = sorted_g[0][1] - sorted_g[-1][1]
            if gap > 10:
                ins["gender_equity"] = f"Equity gap detected: {gap:.1f}pp difference in coding intent between genders."
            else:
                ins["gender_equity"] = f"No significant gender gap: {gap:.1f}pp difference in coding intent."

    # 3. Location champion
    ins["location_champion"] = None
    if col_has_data(df, "location") and col_has_data(df, "enjoyment"):
        ldf = df.groupby("location")["enjoyment"].mean()
        best = ldf.idxmax()
        ins["location_champion"] = f"{best} had the highest avg enjoyment: {ldf[best]:.2f}/5."

    # 4. Top engagement driver
    ins["top_driver"] = None
    if col_has_data(df, "best_parts"):
        all_tags = [t for row in df["best_parts"] for t in row]
        if all_tags:
            from collections import Counter
            top = Counter(all_tags).most_common(1)[0]
            pct = round(top[1] / len(df) * 100, 1)
            ins["top_driver"] = f'"{top[0]}" was the top enjoyment driver, selected by {pct}% of respondents.'

    # 5. Knowledge gap
    ins["knowledge_gap"] = None
    if col_has_data(df, "enjoyment") and col_has_data(df, "learning_gain"):
        e_mean = df["enjoyment"].mean()
        l_mean = df["learning_gain"].mean()
        diff = e_mean - l_mean
        if diff > 0.3:
            ins["knowledge_gap"] = f"Curriculum depth opportunity: enjoyment ({e_mean:.2f}) exceeds knowledge gain ({l_mean:.2f}) by {diff:.2f} points."
        else:
            ins["knowledge_gap"] = f"Well-balanced: enjoyment ({e_mean:.2f}) and knowledge gain ({l_mean:.2f}) are closely aligned."

    # 6 & 7 come from sentiment analysis
    ins["sentiment_champion"] = None
    ins["top_feedback_theme"] = None
    if sentiment_results:
        best_col, best_pct = None, 0
        for col_name, res in sentiment_results.items():
            if "scores" in res and res["scores"]:
                pos_pct = res["scores"].get("positive", 0) / max(sum(res["scores"].values()), 1) * 100
                if pos_pct > best_pct:
                    best_pct, best_col = pos_pct, col_name
        if best_col:
            ins["sentiment_champion"] = f'"{LABELS.get(best_col, best_col)}" had the highest positive sentiment: {best_pct:.0f}% positive.'

        for col_name, res in sentiment_results.items():
            if col_name == "tips" and "themes" in res:
                non_pos = [(t, c) for t, c in res["themes"].items()
                           if res.get("theme_sentiments", {}).get(t) != "positive"]
                if non_pos:
                    top_t = max(non_pos, key=lambda x: x[1])
                    ins["top_feedback_theme"] = f'Most common improvement theme in tips: "{top_t[0]}" (mentioned {top_t[1]} times).'
                    break

    return ins

# ── Section 3: Q-by-Q ─────────────────────────────────────────────────────────
def build_qbyq(df) -> str:
    sections = []

    # ── Subsection A: General & Demographics ──────────────────────────────────
    cards_a = []

    if col_has_data(df, "location"):
        n = df["location"].notna().sum()
        cards_a.append(card("Workshop location", chart_hbar(df["location"], ""),
                            dutch=DUTCH_LABELS.get("location",""), n=n, chart_type="Horizontal bar"))

    if col_has_data(df, "role"):
        n = df["role"].notna().sum()
        cards_a.append(card("Student or teacher", chart_donut(df["role"], ""),
                            dutch=DUTCH_LABELS.get("role",""), n=n, chart_type="Donut"))

    if col_has_data(df, "educ_type"):
        n = df["educ_type"].notna().sum()
        cards_a.append(card("Education level", chart_hbar(df["educ_type"], ""),
                            dutch=DUTCH_LABELS.get("educ_type",""), n=n, chart_type="Horizontal bar"))

    if col_has_data(df, "age_po"):
        age_ser = pd.to_numeric(df["age_po"], errors="coerce").dropna().astype(int)
        n = len(age_ser)
        if n >= MIN_N:
            cards_a.append(card("Age (primary school)", chart_vbar(age_ser, PALETTE["blue"]),
                                dutch=DUTCH_LABELS.get("age_po",""), n=n, chart_type="Bar chart"))

    if col_has_data(df, "gender_po"):
        n = df["gender_po"].notna().sum()
        if n >= MIN_N:
            cards_a.append(card("Gender (primary school)", chart_donut(df["gender_po"], ""),
                                dutch=DUTCH_LABELS.get("gender_po",""), n=n, chart_type="Donut"))

    if col_has_data(df, "age_vo"):
        age_ser = pd.to_numeric(df["age_vo"], errors="coerce").dropna().astype(int)
        n = len(age_ser)
        if n >= MIN_N:
            cards_a.append(card("Age (secondary school)", chart_vbar(age_ser, PALETTE["teal"]),
                                dutch=DUTCH_LABELS.get("age_vo",""), n=n, chart_type="Bar chart"))
        elif n > 0:
            cards_a.append(placeholder_card("Age (secondary school)", f"Too few responses for a chart (n={n})."))

    if col_has_data(df, "gender_vo"):
        n = df["gender_vo"].notna().sum()
        if n >= MIN_N:
            cards_a.append(card("Gender (secondary school)", chart_donut(df["gender_vo"], ""),
                                dutch=DUTCH_LABELS.get("gender_vo",""), n=n, chart_type="Donut"))

    if col_has_data(df, "tech_study"):
        n = df["tech_study"].notna().sum()
        liq = chart_likert(df["tech_study"], "Tech study intent")
        mean_v = df["tech_study"].mean()
        if n >= MIN_N and liq:
            cards_a.append(card(f"Want to study tech later (VO) — avg {mean_v:.2f}/5",
                                liq, dutch="Ik wil later een technische studie doen",
                                n=n, chart_type="Likert bar"))
        else:
            cards_a.append(placeholder_card("Want to study tech later (VO)",
                                            f"Too few VO respondents (n={n}) for a chart."))

    # MBO block — empty
    for col, lbl in [("age_mbo","Age (MBO/HBO/WO)"), ("gender_mbo","Gender (MBO/HBO/WO)")]:
        if not col_has_data(df, col):
            cards_a.append(placeholder_card(lbl, "No MBO/HBO/WO respondents in this dataset."))

    sections.append(_subsection("A — General & demographics", cards_a))

    # ── Subsection B: Workshop specifics ──────────────────────────────────────
    cards_b = []

    if col_has_data(df, "workshop_s"):
        n = df["workshop_s"].notna().sum()
        cards_b.append(card("Workshop type", chart_hbar(df["workshop_s"], ""),
                            dutch=DUTCH_LABELS.get("workshop_s",""), n=n, chart_type="Horizontal bar"))

    # Prior coding + want more (grouped)
    if col_has_data(df, "prev_programmed") and col_has_data(df, "prog_more"):
        n = df[["prev_programmed","prog_more"]].dropna().shape[0]
        if n >= MIN_N:
            cross = pd.crosstab(df["prev_programmed"], df["prog_more"])
            fig = go.Figure()
            colors_g = [PALETTE["coral"], PALETTE["teal"]]
            for i, col_name in enumerate(cross.columns):
                fig.add_trace(go.Bar(name=col_name, x=cross.index, y=cross[col_name],
                                     marker_color=colors_g[i % 2],
                                     text=cross[col_name], textposition="outside"))
            fig.update_layout(barmode="group", margin=dict(l=10,r=10,t=10,b=10),
                               height=280, plot_bgcolor="white", paper_bgcolor="white",
                               legend=dict(orientation="h", y=-0.25))
            cc = card("Prior coding × want to code more",
                      embed_plotly(fig),
                      dutch="Heb je eerder geprogrammeerd? × Zou je vaker willen programmeren?",
                      n=n, chart_type="Grouped bar")
            cards_b.append(cc)

    # Minecraft, hacker, drone, datacenter — all empty in this dataset
    for col, lbl, workshop in [
        ("prev_minecraft", "Prior Minecraft experience", "Minecraft"),
        ("more_minecraft", "Want to continue in Minecraft", "Minecraft"),
        ("hacker_interest", "Interest in ethical hacking", "Hacking workshop"),
        ("drone_interest", "Interest in drones", "Drone workshop"),
        ("datacenter_int", "Interest in datacenters", "Datacenter workshop"),
    ]:
        if not col_has_data(df, col):
            cards_b.append(placeholder_card(lbl,
                f"No respondents for {workshop} workshop in this dataset."))

    # AI interest — only n=2
    if col_has_data(df, "ai_interest"):
        n = df["ai_interest"].notna().sum()
        if n < MIN_N:
            vals = df["ai_interest"].dropna().astype(int).value_counts().to_dict()
            table_rows = "".join(f"<tr><td>Score {k}</td><td>{v}</td></tr>" for k, v in sorted(vals.items()))
            tbl = f'<table class="small-table"><tr><th>Score</th><th>Count</th></tr>{table_rows}</table>'
            cards_b.append(card("Want to work with AI more (n=2)",
                                f'<p class="caveat">Too few AI workshop respondents for a chart.</p>{tbl}',
                                dutch="Na vandaag zou ik vaker met AI willen werken?", n=n))

    sections.append(_subsection("B — Workshop specifics", cards_b))

    # ── Subsection C: Core satisfaction ───────────────────────────────────────
    cards_c = []

    for col, lbl in [
        ("learning_gain", "Knowledge gained"),
        ("enjoyment", "Workshop enjoyment"),
        ("teacher_score", "Instructor rating"),
        ("proud", "Self-pride after workshop"),
    ]:
        if col_has_data(df, col):
            n = df[col].notna().sum()
            mean_v = df[col].mean()
            liq = chart_likert(df[col], lbl)
            if liq:
                cards_c.append(card(f"{lbl} — avg {mean_v:.2f}/5", liq,
                                    dutch=DUTCH_LABELS.get(col,""), n=n, chart_type="Likert bar"))

    if col_has_data(df, "best_parts"):
        n_resp = sum(1 for tags in df["best_parts"] if tags)
        ch = chart_multiselect(df["best_parts"], len(df))
        if ch:
            cards_c.append(card("What they enjoyed most (multi-select)", ch,
                                dutch=DUTCH_LABELS.get("best_parts",""),
                                n=n_resp, chart_type="Multi-select bar"))

    if col_has_data(df, "describe_ds"):
        n = df["describe_ds"].notna().sum()
        wc_html = chart_wordcloud(df["describe_ds"])
        content = wc_html if wc_html else '<p class="caveat">See sentiment analysis section for full text analysis.</p>'
        cards_c.append(card("Describe DreamSpace in one sentence", content,
                            dutch=DUTCH_LABELS.get("describe_ds",""), n=n,
                            chart_type="Word cloud" if wc_html else "See Section 5"))

    if col_has_data(df, "tips"):
        n = df["tips"].notna().sum()
        cards_c.append(card("Tips & improvement feedback",
                            '<p class="caveat">Full sentiment analysis and comment cards in Section 5 below.</p>',
                            dutch=DUTCH_LABELS.get("tips",""), n=n))

    sections.append(_subsection("C — Core satisfaction (all respondents)", cards_c))

    # ── Subsection D: OBA/TUMO ────────────────────────────────────────────────
    oba_df = df[df.get("location", pd.Series()).astype(str).str.contains("OBA", na=False)] if "location" in df.columns else pd.DataFrame()
    n_oba = len(oba_df)
    cards_d = []

    if n_oba == 0:
        oba_df = df  # fallback: use all if location col missing

    oba_cols = [
        ("location_score", "Location rating", "Likert stacked bar"),
        ("oba_aware", "Prior awareness of OBA / TUMO", "Donut"),
        ("oba_again", "Plans to join OBA activities", "Donut"),
        ("tumo_interest", "Interest in TUMO Amsterdam", "Donut"),
    ]
    for col, lbl, ctype in oba_cols:
        if col_has_data(oba_df, col):
            n = oba_df[col].notna().sum()
            if "Likert" in ctype:
                mean_v = oba_df[col].mean()
                liq = chart_likert(oba_df[col], lbl)
                if liq:
                    cards_d.append(card(f"{lbl} — avg {mean_v:.2f}/5", liq,
                                        dutch=DUTCH_LABELS.get(col,""), n=n, chart_type=ctype))
            else:
                ch = chart_donut(oba_df[col], "")
                if ch:
                    cards_d.append(card(lbl, ch,
                                        dutch=DUTCH_LABELS.get(col,""), n=n, chart_type=ctype))
        else:
            cards_d.append(placeholder_card(lbl, "No data for this question in this dataset."))

    if col_has_data(oba_df, "curious_topics"):
        n_resp = sum(1 for tags in oba_df["curious_topics"] if tags)
        ch = chart_multiselect(oba_df["curious_topics"], max(n_oba, 1))
        if ch:
            cards_d.append(card("Curious about (multi-select)", ch,
                                dutch=DUTCH_LABELS.get("curious_topics",""),
                                n=n_resp, chart_type="Multi-select bar"))
        else:
            cards_d.append(placeholder_card("Curious about", "No responses for this question."))
    else:
        cards_d.append(placeholder_card("Curious about", "No data for this question."))

    badge = f"OBA Next – Amsterdam only · n={n_oba}"
    sections.append(_subsection("D — OBA / TUMO pilot", cards_d, badge=badge, badge_color="#378ADD"))

    # ── Subsection E: Teacher ─────────────────────────────────────────────────
    teacher_df = df[df.get("role", pd.Series()).astype(str).str.contains("Docent|ocent", na=False)] if "role" in df.columns else pd.DataFrame()
    n_teachers = len(teacher_df)
    cards_e = [placeholder_card("Teacher responses",
                                f"No teacher respondents in this dataset (n={n_teachers}). "
                                "Teacher questions will be displayed when teacher data is available.")]
    badge_t = f"Teacher respondents only · n={n_teachers}"
    sections.append(_subsection("E — Teacher section", cards_e, badge=badge_t, badge_color="#EF9F27"))

    return "\n".join(sections)

def _subsection(title: str, cards: list, badge: str = "", badge_color: str = "") -> str:
    badge_html = f'<span class="badge" style="background:{badge_color};color:white">{html.escape(badge)}</span>' if badge else ""
    cards_html = "\n".join(cards) if cards else placeholder_card("No data", "No questions available for this subsection.")
    return f"""
<details class="subsection" open>
  <summary class="subsection-title">{html.escape(title)} {badge_html}</summary>
  <div class="card-grid">{cards_html}</div>
</details>"""

# ── Section 4: Deep-dives ──────────────────────────────────────────────────────
def build_deepdives(df) -> str:
    parts = []

    # A: Weekly response trend
    if col_has_data(df, "start_time"):
        wdf = df.groupby("iso_week").size().reset_index(name="count")
        fig = go.Figure(go.Bar(
            x=wdf["iso_week"].astype(str).apply(lambda w: f"Week {w}"),
            y=wdf["count"],
            marker_color=PALETTE["primary"],
            text=wdf["count"], textposition="outside",
        ))
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=280,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis_title="ISO Calendar Week", yaxis_title="Responses",
                          yaxis=dict(gridcolor="#f0f0f0"))
        parts.append(_dive("A. Weekly response trend", embed_plotly(fig),
                           "Grouped by ISO week number derived from start timestamp. Each bar = total submissions in that calendar week."))

    # B: Completion time distribution
    if "duration_min" in df.columns:
        dur = df["duration_min"].dropna()
        dur_filtered = dur[dur <= 10]
        n_excluded = len(dur) - len(dur_filtered)
        med = dur_filtered.median()
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=dur_filtered, xbins=dict(size=0.5),
                                   marker_color=PALETTE["blue"], opacity=0.8, name="Responses"))
        fig.add_vline(x=med, line_color=PALETTE["coral"], line_dash="dash",
                      annotation_text=f"Median: {med:.1f} min", annotation_position="top right")
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=280,
                          plot_bgcolor="white", paper_bgcolor="white",
                          xaxis_title="Completion time (minutes)", yaxis_title="Count",
                          yaxis=dict(gridcolor="#f0f0f0"))
        note = f"Duration = completion − start time. Responses > 10 min excluded (n={n_excluded})."
        parts.append(_dive("B. Completion time distribution", embed_plotly(fig), note))

    # C: Gender × coding intent (PO)
    if col_has_data(df, "gender_po") and col_has_data(df, "prog_more"):
        sub = df[["gender_po","prog_more"]].dropna()
        if len(sub) >= MIN_N:
            cross = pd.crosstab(sub["gender_po"], sub["prog_more"], normalize="index") * 100
            fig = go.Figure()
            for col_name, color in zip(["Ja","Nee"], [PALETTE["teal"], PALETTE["coral"]]):
                if col_name in cross.columns:
                    fig.add_trace(go.Bar(name=f"Want more: {col_name}",
                                         x=cross.index, y=cross[col_name].round(1),
                                         marker_color=color,
                                         text=cross[col_name].round(1).astype(str) + "%",
                                         textposition="outside"))
            fig.update_layout(barmode="group", margin=dict(l=10,r=10,t=10,b=10),
                               height=280, plot_bgcolor="white", paper_bgcolor="white",
                               yaxis=dict(title="% within gender", gridcolor="#f0f0f0"),
                               legend=dict(orientation="h", y=-0.25))
            parts.append(_dive("C. Gender × coding intent (PO students)", embed_plotly(fig),
                               "Cross-tab of PO gender vs 'want to code more'. % computed within each gender group."))

    # D: Enjoyment vs knowledge gap by workshop
    if col_has_data(df, "enjoyment") and col_has_data(df, "learning_gain") and col_has_data(df, "workshop_s"):
        gdf = df.groupby("workshop_s")[["enjoyment","learning_gain"]].mean().reset_index()
        gdf = gdf[gdf["workshop_s"].map(lambda w: df[df["workshop_s"]==w].shape[0] >= MIN_N)]
        if len(gdf) > 0:
            gdf["gap"] = (gdf["enjoyment"] - gdf["learning_gain"]).round(2)
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Enjoyment", x=gdf["workshop_s"], y=gdf["enjoyment"].round(2),
                                  marker_color=PALETTE["primary"]))
            fig.add_trace(go.Bar(name="Knowledge gain", x=gdf["workshop_s"], y=gdf["learning_gain"].round(2),
                                  marker_color=PALETTE["teal"]))
            fig.add_trace(go.Scatter(name="Gap", x=gdf["workshop_s"], y=gdf["gap"],
                                      mode="lines+markers+text",
                                      text=gdf["gap"].astype(str), textposition="top center",
                                      line=dict(color=PALETTE["amber"], dash="dot"),
                                      marker=dict(size=8)))
            fig.update_layout(barmode="group", margin=dict(l=10,r=10,t=10,b=10),
                               height=320, plot_bgcolor="white", paper_bgcolor="white",
                               yaxis=dict(title="Mean score (1–5)", gridcolor="#f0f0f0"),
                               legend=dict(orientation="h", y=-0.25))
            parts.append(_dive("D. Enjoyment vs knowledge gap by workshop", embed_plotly(fig),
                               "MEAN(enjoyment) and MEAN(knowledge gain) per workshop type. Gap = enjoyment − knowledge. Only workshops with n≥5 shown."))

    # E: Location multi-metric
    if all(col_has_data(df, c) for c in ["location","enjoyment","teacher_score","proud"]):
        ldf = df.groupby("location")[["enjoyment","teacher_score","proud"]].mean().reset_index()
        fig = go.Figure()
        for metric, color in [("enjoyment", PALETTE["primary"]),
                                ("teacher_score", PALETTE["teal"]),
                                ("proud", PALETTE["amber"])]:
            fig.add_trace(go.Bar(name=metric.replace("_"," ").title(),
                                  x=ldf["location"], y=ldf[metric].round(2),
                                  marker_color=color,
                                  text=ldf[metric].round(2), textposition="outside"))
        fig.update_layout(barmode="group", margin=dict(l=10,r=10,t=10,b=10),
                           height=320, plot_bgcolor="white", paper_bgcolor="white",
                           yaxis=dict(title="Mean score (1–5)", range=[0,5.5], gridcolor="#f0f0f0"),
                           legend=dict(orientation="h", y=-0.25))
        parts.append(_dive("E. Location effect — multi-metric comparison", embed_plotly(fig),
                           "MEAN of enjoyment, instructor rating, and self-pride per location. Only rows with all three non-null included."))

    # F: Prior coding → post-workshop intent
    if col_has_data(df, "prev_programmed") and col_has_data(df, "prog_more"):
        sub = df[["prev_programmed","prog_more"]].dropna()
        if len(sub) >= MIN_N:
            cross = pd.crosstab(sub["prev_programmed"], sub["prog_more"])
            fig = go.Figure()
            for col_name, color in zip(["Ja","Nee"], [PALETTE["teal"], PALETTE["coral"]]):
                if col_name in cross.columns:
                    row_totals = cross.sum(axis=1)
                    pcts = (cross[col_name] / row_totals * 100).round(1)
                    fig.add_trace(go.Bar(name=f"Want more: {col_name}",
                                         x=cross.index, y=cross[col_name],
                                         marker_color=color,
                                         text=[f"{c} ({p}%)" for c,p in zip(cross[col_name], pcts)],
                                         textposition="outside"))
            fig.update_layout(barmode="group", margin=dict(l=10,r=10,t=10,b=10),
                               height=300, plot_bgcolor="white", paper_bgcolor="white",
                               xaxis_title="Had prior coding experience",
                               yaxis=dict(title="Count", gridcolor="#f0f0f0"),
                               legend=dict(orientation="h", y=-0.25))
            parts.append(_dive("F. Prior coding experience → post-workshop intent", embed_plotly(fig),
                               "Cross-tab of prior coding experience vs want to code more. % computed within each prior-experience group."))

    # G: Top enjoyment drivers weighted
    if col_has_data(df, "best_parts"):
        from collections import Counter
        all_tags = [t for row in df["best_parts"] for t in row]
        if all_tags:
            counts = Counter(all_tags)
            df_tags = pd.DataFrame(counts.most_common(15), columns=["tag","count"])
            df_tags["pct"] = (df_tags["count"] / len(df) * 100).round(1)
            df_tags = df_tags.sort_values("count")
            fig = go.Figure(go.Bar(
                x=df_tags["pct"], y=df_tags["tag"], orientation="h",
                marker_color=PALETTE["primary"],
                text=[f"{c} ({p}%)" for c,p in zip(df_tags["count"], df_tags["pct"])],
                textposition="outside",
            ))
            fig.update_layout(margin=dict(l=10,r=120,t=10,b=10),
                               height=max(200, len(df_tags)*36),
                               plot_bgcolor="white", paper_bgcolor="white",
                               xaxis=dict(title="% of respondents", showgrid=False, showticklabels=False),
                               yaxis=dict(tickfont=dict(size=12)),
                               showlegend=False)
            parts.append(_dive("G. Top enjoyment drivers — weighted frequency", embed_plotly(fig),
                               "Multi-select field split by ';'. Each tag counted independently. % = tag count / total respondents × 100."))

    # H: OBA/TUMO conversion funnel
    oba_sub = df[df.get("location", pd.Series()).astype(str).str.contains("OBA", na=False)] if "location" in df.columns else pd.DataFrame()
    if len(oba_sub) >= MIN_N:
        n_oba_total = len(oba_sub)
        n_aware = oba_sub["oba_aware"].notna().sum() if "oba_aware" in oba_sub.columns else 0
        n_tumo = (oba_sub.get("tumo_interest","") == "Ja, zeker!").sum() if "tumo_interest" in oba_sub.columns else 0
        n_oba_again = (oba_sub.get("oba_again","") == "Ja").sum() if "oba_again" in oba_sub.columns else 0

        fig = go.Figure(go.Funnel(
            y=["Total OBA respondents","Heard of OBA/TUMO","Interested in TUMO (Ja, zeker)","Plans to join OBA"],
            x=[n_oba_total, n_aware, n_tumo, n_oba_again],
            textinfo="value+percent initial",
            marker=dict(color=[PALETTE["primary"], PALETTE["blue"], PALETTE["teal"], PALETTE["green"]]),
        ))
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=320,
                           plot_bgcolor="white", paper_bgcolor="white")
        parts.append(_dive("H. OBA/TUMO conversion funnel", embed_plotly(fig),
                           "Sequential count of qualifying responses within OBA Next location subset. Each stage = affirmative responses."))

    # I: Satisfaction radar
    radar_cols = {
        "Workshop enjoyment": "enjoyment",
        "Instructor quality": "teacher_score",
        "Knowledge gained": "learning_gain",
        "Self-pride": "proud",
    }
    radar_vals = {}
    for lbl, col in radar_cols.items():
        if col_has_data(df, col):
            radar_vals[lbl] = round(df[col].mean(), 2)

    if len(radar_vals) >= 3:
        cats = list(radar_vals.keys())
        vals = list(radar_vals.values())
        cats_closed = cats + [cats[0]]
        vals_closed = vals + [vals[0]]
        fig = go.Figure(go.Scatterpolar(
            r=vals_closed, theta=cats_closed, fill="toself",
            line_color=PALETTE["primary"], fillcolor=PALETTE["primary"],
            opacity=0.35, name="Students",
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            margin=dict(l=60,r=60,t=40,b=40), height=360,
            plot_bgcolor="white", paper_bgcolor="white", showlegend=False,
        )
        parts.append(_dive("I. Satisfaction radar scorecard", embed_plotly(fig),
                           "Each axis = MEAN of corresponding Likert column. Scale 0–5."))

    # J: Age distribution across education levels
    age_data = []
    for col, label in [("age_po","Primary school (PO)"), ("age_vo","Secondary school (VO)")]:
        if col_has_data(df, col):
            ages = pd.to_numeric(df[col], errors="coerce").dropna()
            for a in ages:
                age_data.append({"age": a, "level": label})
    if age_data:
        adf = pd.DataFrame(age_data)
        fig = go.Figure()
        colors_age = [PALETTE["blue"], PALETTE["teal"]]
        for i, (level, grp) in enumerate(adf.groupby("level")):
            fig.add_trace(go.Histogram(x=grp["age"], name=level,
                                        marker_color=colors_age[i % 2],
                                        opacity=0.7, xbins=dict(size=1)))
        fig.update_layout(barmode="overlay", margin=dict(l=10,r=10,t=10,b=10),
                           height=280, plot_bgcolor="white", paper_bgcolor="white",
                           xaxis_title="Age", yaxis=dict(title="Count", gridcolor="#f0f0f0"),
                           legend=dict(orientation="h", y=-0.25))
        parts.append(_dive("J. Age distribution across education levels", embed_plotly(fig),
                           "PO and VO age columns combined into one distribution, colour-coded by education level."))

    # K: Correlation heatmap
    likert_available = {k: v for k, v in {
        "Enjoyment": "enjoyment",
        "Knowledge gain": "learning_gain",
        "Teacher score": "teacher_score",
        "Self-pride": "proud",
        "Tech study (VO)": "tech_study",
        "AI interest": "ai_interest",
    }.items() if col_has_data(df, v, min_rows=10)}

    if len(likert_available) >= 3:
        corr_df = df[[v for v in likert_available.values()]].copy()
        corr_df.columns = list(likert_available.keys())
        corr = corr_df.corr(method="pearson")

        # Significance annotations
        n_corr = len(corr_df.dropna())
        annots = []
        for r in corr.index:
            row = []
            for c in corr.columns:
                val = corr.loc[r, c]
                if r == c:
                    row.append(f"1.00")
                else:
                    try:
                        valid = corr_df[[r, c]].dropna()
                        if len(valid) > 5:
                            _, pv = stats.pearsonr(valid[r], valid[c])
                            sig = "**" if pv < 0.01 else ("*" if pv < 0.05 else "")
                            row.append(f"{val:.2f}{sig}")
                        else:
                            row.append("n/a")
                    except Exception:
                        row.append(f"{val:.2f}")
            annots.append(row)

        fig = go.Figure(go.Heatmap(
            z=corr.values,
            x=list(likert_available.keys()),
            y=list(likert_available.keys()),
            colorscale="RdBu",
            zmid=0, zmin=-1, zmax=1,
            text=annots,
            texttemplate="%{text}",
            textfont=dict(size=11),
            colorbar=dict(title="r"),
        ))
        fig.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=380,
                           plot_bgcolor="white", paper_bgcolor="white")
        note = "Pearson r computed pairwise. * p<0.05  ** p<0.01. Scale −1 (blue) to +1 (red)."
        parts.append(_dive("K. Correlation heatmap — Likert scores", embed_plotly(fig), note))

    return "\n".join(parts)

def _dive(title: str, chart_html: str, note: str) -> str:
    return f"""
<div class="card dive-card">
  <div class="card-title">{html.escape(title)}</div>
  <div class="calc-note"><em>How this was calculated:</em> {html.escape(note)}</div>
  {chart_html}
</div>"""

# ── Section 5: Sentiment analysis ─────────────────────────────────────────────
def run_sentiment(responses: list, question_context: str, client) -> list:
    numbered = "\n".join(f"{i+1}. {r}" for i, r in enumerate(responses))
    prompt = f"""You are analysing open-ended survey responses from Dutch students and teachers
after a STEM/AI workshop called DreamSpace, run by Microsoft in the Netherlands.
Question context: {question_context}

Classify each numbered response. Return ONLY a valid JSON array, no markdown, no preamble.

Each element must have exactly these keys:
- "id": integer (the response number)
- "sentiment": one of "positive", "neutral", "negative", "mixed"
- "themes": array of 1-3 short English theme tags (e.g. ["fun", "wants more time", "liked teacher"])
- "summary_label": a 4-6 word English phrase summarising this specific response
- "quotable": boolean — true if this response is short, vivid, and worth showing as a highlight quote

Responses to classify:
{numbered}

Return only the JSON array."""

    msg = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = msg.content[0].text.strip()
    if raw.startswith("```"):
        lines = raw.split("\n")
        raw = "\n".join(lines[1:])
        if raw.endswith("```"):
            raw = raw[:-3]
    parsed = json.loads(raw.strip())
    return [
        {
            "text": responses[r["id"] - 1],
            "sentiment": r["sentiment"],
            "themes": r.get("themes", []),
            "summary_label": r.get("summary_label", ""),
            "quotable": r.get("quotable", False),
        }
        for r in parsed
        if 1 <= r["id"] <= len(responses)
    ]

def build_sentiment_section(df) -> tuple:
    """Returns (html_string, sentiment_results_dict)."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        html_out = """
<div class="card placeholder-card">
  <div class="card-title">Sentiment analysis — not available</div>
  <p>Set the <code>ANTHROPIC_API_KEY</code> environment variable and re-run to enable AI-powered sentiment analysis.</p>
  <pre style="background:#f5f5f3;padding:12px;border-radius:6px;font-size:12px">export ANTHROPIC_API_KEY=sk-ant-...
python dreamspace_analysis.py Results.xlsx</pre>
</div>"""
        return html_out, {}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
    except Exception as e:
        return f'<div class="card placeholder-card"><div class="card-title">Sentiment analysis error</div><p>{html.escape(str(e))}</p></div>', {}

    SENTIMENT_COLUMNS = [
        ("describe_ds",  "Describing DreamSpace in one sentence (students)"),
        ("tips",         "Tips and improvement suggestions (students)"),
        ("datacenter_text", "What appeals about datacenters (students, conditional)"),
        ("t_explain",    "Explaining challenges with digital literacy teaching (teachers, conditional)"),
        ("t_suggestions","Workshop improvement suggestions (teachers, conditional)"),
    ]

    results = {}
    sections_html = []

    for col, ctx in SENTIMENT_COLUMNS:
        if not col_has_data(df, col, min_rows=3):
            continue

        responses = df[col].dropna().astype(str).tolist()
        responses = [r for r in responses if r.strip() and r.strip().lower() not in ["nan","-","."]]
        if len(responses) < 3:
            continue

        print(f"  Running sentiment on '{col}' (n={len(responses)})...")
        try:
            classified = run_sentiment(responses, ctx, client)
        except Exception as e:
            sections_html.append(f'<div class="card placeholder-card"><div class="card-title">Sentiment: {html.escape(col)}</div><p>Error: {html.escape(str(e))}</p></div>')
            continue

        # Aggregate
        from collections import Counter, defaultdict
        scores = Counter(r["sentiment"] for r in classified)
        all_themes = [t for r in classified for t in r["themes"]]
        theme_counts = Counter(all_themes)

        theme_sentiments = defaultdict(list)
        for r in classified:
            for t in r["themes"]:
                theme_sentiments[t].append(r["sentiment"])
        theme_dominant = {t: Counter(v).most_common(1)[0][0] for t, v in theme_sentiments.items()}

        results[col] = {
            "scores": dict(scores),
            "themes": dict(theme_counts),
            "theme_sentiments": theme_dominant,
            "classified": classified,
        }

        total = len(classified)
        pct_pos = round(scores.get("positive",0)/total*100, 1)
        pct_neu = round(scores.get("neutral",0)/total*100, 1)
        pct_neg = round(scores.get("negative",0)/total*100, 1)
        pct_mix = round(scores.get("mixed",0)/total*100, 1)
        badge_str = f"{pct_pos}% positive · {pct_neu}% neutral · {pct_neg}% negative · {pct_mix}% mixed"

        col_html_parts = []

        # 5a: Sentiment donut
        s_labels = list(scores.keys())
        s_values = list(scores.values())
        s_colors = [SENTIMENT_COLORS.get(s, "#888") for s in s_labels]
        fig_donut = go.Figure(go.Pie(
            labels=[l.capitalize() for l in s_labels], values=s_values,
            hole=0.45,
            marker=dict(colors=s_colors),
            textinfo="label+percent",
        ))
        fig_donut.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=260,
                                showlegend=False, plot_bgcolor="white", paper_bgcolor="white")
        col_html_parts.append(f"""
<div class="card">
  <div class="card-title">Sentiment distribution</div>
  <div class="calc-note">Each response classified by Claude Haiku · n={total} · {pct_pos}% positive</div>
  {embed_plotly(fig_donut)}
</div>""")

        # 5b: Top themes bar
        if theme_counts:
            top_themes = theme_counts.most_common(10)
            t_names = [t[0] for t in top_themes]
            t_vals = [t[1] for t in top_themes]
            t_colors = [SENTIMENT_COLORS.get(theme_dominant.get(n,"neutral"), "#888") for n in t_names]
            fig_themes = go.Figure(go.Bar(
                x=t_vals, y=t_names, orientation="h",
                marker_color=t_colors,
                text=t_vals, textposition="outside",
            ))
            fig_themes.update_layout(margin=dict(l=10,r=60,t=10,b=10),
                                      height=max(200, len(t_names)*32),
                                      plot_bgcolor="white", paper_bgcolor="white",
                                      xaxis=dict(showgrid=False, showticklabels=False),
                                      yaxis=dict(tickfont=dict(size=12)), showlegend=False)
            col_html_parts.append(f"""
<div class="card">
  <div class="card-title">Top themes</div>
  <div class="calc-note">1–3 English theme tags per response, pooled and counted. Bar colour = dominant sentiment for that theme.</div>
  {embed_plotly(fig_themes)}
</div>""")

        # 5c: Theme trend over ISO weeks
        if "iso_week" in df.columns and df["iso_week"].nunique() >= 2:
            col_idx = df[col].notna()
            valid_idx = [i for i, r in enumerate(df[col_idx].index) if i < len(classified)]
            if valid_idx:
                top5 = [t[0] for t in theme_counts.most_common(5)]
                weeks = df.loc[df[col].notna(), "iso_week"].values
                week_theme_data = []
                for i, (r, w) in enumerate(zip(classified, weeks[:len(classified)])):
                    for t in r["themes"]:
                        if t in top5:
                            week_theme_data.append({"week": w, "theme": t})
                if week_theme_data:
                    wtdf = pd.DataFrame(week_theme_data)
                    wtpivot = wtdf.groupby(["week","theme"]).size().unstack(fill_value=0)
                    fig_trend = go.Figure()
                    for t in top5:
                        if t in wtpivot.columns:
                            fig_trend.add_trace(go.Scatter(
                                x=wtpivot.index.astype(str).apply(lambda w: f"Wk {w}"),
                                y=wtpivot[t], mode="lines+markers", name=t,
                            ))
                    fig_trend.update_layout(margin=dict(l=10,r=10,t=10,b=30),
                                             height=260, plot_bgcolor="white", paper_bgcolor="white",
                                             yaxis=dict(title="Count", gridcolor="#f0f0f0"),
                                             legend=dict(orientation="h", y=-0.3))
                    col_html_parts.append(f"""
<div class="card">
  <div class="card-title">Theme frequency by week (top 5)</div>
  <div class="calc-note">Top 5 themes grouped by ISO week. One line per theme.</div>
  {embed_plotly(fig_trend)}
</div>""")

        # 5d: Sentiment × workshop type
        if col_has_data(df, "workshop_s"):
            ws_list = df.loc[df[col].notna(), "workshop_s"].values
            sw_data = []
            for r, w in zip(classified, ws_list[:len(classified)]):
                sw_data.append({"workshop": str(w), "sentiment": r["sentiment"]})
            if sw_data:
                swdf = pd.DataFrame(sw_data)
                pivot = pd.crosstab(swdf["workshop"], swdf["sentiment"])
                fig_sw = go.Figure()
                for sent, color in SENTIMENT_COLORS.items():
                    if sent in pivot.columns:
                        fig_sw.add_trace(go.Bar(name=sent.capitalize(),
                                                 x=pivot.index, y=pivot[sent],
                                                 marker_color=color))
                fig_sw.update_layout(barmode="stack",
                                      margin=dict(l=10,r=10,t=10,b=40),
                                      height=300, plot_bgcolor="white", paper_bgcolor="white",
                                      yaxis=dict(title="Count", gridcolor="#f0f0f0"),
                                      legend=dict(orientation="h", y=-0.35))
                col_html_parts.append(f"""
<div class="card">
  <div class="card-title">Sentiment by workshop type</div>
  <div class="calc-note">Sentiment labels joined to workshop type by row index. Stacked count per workshop.</div>
  {embed_plotly(fig_sw)}
</div>""")

        # 5e: Highlight comment cards
        positives = [r for r in classified if r["sentiment"] == "positive" and r.get("quotable")]
        if len(positives) < 3:
            positives = sorted([r for r in classified if r["sentiment"] == "positive"],
                               key=lambda r: len(r["text"]))[:3]
        else:
            positives = sorted(positives, key=lambda r: len(r["text"]))[:3]

        constructive = [r for r in classified if r["sentiment"] in ("negative","mixed")]
        constructive = sorted(constructive,
                              key=lambda r: any(w in r.get("summary_label","").lower()
                                                for w in ["more","time","better","should","want","need"]),
                              reverse=True)[:3]

        seen_labels = {r.get("summary_label","") for r in positives + constructive}
        wildcard = [r for r in classified if r.get("summary_label","") not in seen_labels]
        wildcard = sorted(wildcard, key=lambda r: len(r.get("summary_label","")), reverse=True)[:2]

        highlights = positives[:3] + constructive[:3] + wildcard[:2]
        comment_cards_html = ""
        for r in highlights:
            s = r["sentiment"]
            chips = "".join(f'<span class="chip">{html.escape(t)}</span>' for t in r["themes"])
            comment_cards_html += f"""
<div class="comment-card {s}">
  <div class="comment-header">
    <span class="sentiment-pill {s}">● {s.capitalize()}</span>
    <span class="summary-label">{html.escape(r.get("summary_label",""))}</span>
  </div>
  <p class="comment-text">"{html.escape(str(r["text"]))}"</p>
  <div class="theme-chips">{chips}</div>
</div>"""

        col_html_parts.append(f"""
<div class="card full-width">
  <div class="card-title">Highlighted responses</div>
  <div class="comment-grid">{comment_cards_html}</div>
</div>""")

        lbl = LABELS.get(col, col)
        dutch = DUTCH_LABELS.get(col, "")
        dutch_html = f'<div class="dutch-label">{html.escape(dutch)}</div>' if dutch else ""
        sections_html.append(f"""
<div class="sentiment-section">
  <h3 class="sentiment-col-title">
    {html.escape(lbl)}
    <span class="sentiment-badge">{html.escape(badge_str)}</span>
  </h3>
  {dutch_html}
  <div class="card-grid">{''.join(col_html_parts)}</div>
</div>""")

    if not sections_html:
        sections_html.append('<div class="card placeholder-card"><div class="card-title">No open-ended responses</div><p>None of the open-ended columns have sufficient data for analysis.</p></div>')

    return "\n".join(sections_html), results

# ── KPI HTML ───────────────────────────────────────────────────────────────────
def build_kpi_row(kpis: dict) -> str:
    def kpi_card(value, label, sublabel="", color=None):
        c = color or PALETTE["primary"]
        return f"""
<div class="kpi-card" style="border-top:4px solid {c}">
  <div class="kpi-value" style="color:{c}">{value}</div>
  <div class="kpi-label">{html.escape(label)}</div>
  {'<div class="kpi-sub">' + html.escape(sublabel) + '</div>' if sublabel else ''}
</div>"""

    enj_v = f"{kpis['enjoyment_mean']:.2f}/5" if kpis.get("enjoyment_mean") else "—"
    enj_sub = f"±{kpis['enjoyment_sd']:.2f} SD" if kpis.get("enjoyment_sd") else ""
    teacher_v = f"{kpis['teacher_mean']:.2f}/5" if kpis.get("teacher_mean") else "—"
    prog_v = f"{kpis['prog_more_pct']}%" if kpis.get("prog_more_pct") is not None else "—"
    proud_v = f"{kpis['proud_mean']:.2f}/5" if kpis.get("proud_mean") else "—"
    learn_v = f"{kpis['learning_mean']:.2f}/5" if kpis.get("learning_mean") else "—"

    cards = [
        kpi_card(kpis["total"], "Total responses", color=PALETTE["primary"]),
        kpi_card(enj_v, "Avg workshop enjoyment", enj_sub, color=PALETTE["teal"]),
        kpi_card(teacher_v, "Avg instructor rating", color=PALETTE["blue"]),
        kpi_card(prog_v, "Want to code more", color=PALETTE["green"]),
        kpi_card(proud_v, "Avg self-pride", color=PALETTE["amber"]),
        kpi_card(learn_v, "Avg knowledge gain", color=PALETTE["coral"]),
    ]
    return f'<div class="kpi-row">{"".join(cards)}</div>'

# ── Insights HTML ──────────────────────────────────────────────────────────────
def build_insights_row(insights: dict) -> str:
    INSIGHT_META = {
        "retention":         ("🔄", "Retention signal", PALETTE["teal"]),
        "gender_equity":     ("⚖️", "Gender equity check", PALETTE["pink"]),
        "location_champion": ("🏆", "Location champion", PALETTE["amber"]),
        "top_driver":        ("🎯", "Top engagement driver", PALETTE["primary"]),
        "knowledge_gap":     ("📚", "Knowledge gap check", PALETTE["blue"]),
        "sentiment_champion":("💬", "Sentiment champion", PALETTE["green"]),
        "top_feedback_theme":("💡", "Top actionable feedback", PALETTE["coral"]),
    }
    cards = []
    for key, (icon, title, color) in INSIGHT_META.items():
        text = insights.get(key)
        if not text:
            text = "Not available — insufficient data or API key not set."
        cards.append(f"""
<div class="insight-card" style="border-left:4px solid {color}">
  <div class="insight-icon">{icon}</div>
  <div class="insight-title">{html.escape(title)}</div>
  <div class="insight-text">{html.escape(text)}</div>
</div>""")
    return f'<div class="insight-grid">{"".join(cards)}</div>'

# ── CSS ────────────────────────────────────────────────────────────────────────
CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: #FAFAF8; color: #201F1E; }
.page-header { background: #fff; padding: 32px 48px 24px; border-bottom: 1px solid #e8e8e5; }
.page-title { font-size: 26px; font-weight: 700; color: #7F77DD; margin-bottom: 6px; }
.page-subtitle { font-size: 14px; color: #605E5C; margin-bottom: 12px; }
.badge-row { display: flex; gap: 10px; flex-wrap: wrap; }
.badge-item { background: #F3F2F1; border-radius: 20px; padding: 4px 12px; font-size: 12px; color: #333; }
.toc { background: #fff; position: sticky; top: 0; z-index: 100; border-bottom: 1px solid #e8e8e5;
       display: flex; gap: 0; overflow-x: auto; padding: 0 48px; }
.toc a { display: block; padding: 12px 16px; font-size: 13px; color: #605E5C; text-decoration: none;
          white-space: nowrap; border-bottom: 3px solid transparent; }
.toc a:hover { color: #7F77DD; border-bottom-color: #7F77DD; }
main { max-width: 1300px; margin: 0 auto; padding: 32px 48px; }
.section { margin-bottom: 48px; }
.section-header { font-size: 18px; font-weight: 600; color: #201F1E; margin-bottom: 20px;
                   border-left: 4px solid #7F77DD; padding-left: 12px; }
.kpi-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 16px; margin-bottom: 32px; }
.kpi-card { background: #fff; border-radius: 10px; padding: 20px 16px;
             box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
.kpi-value { font-size: 28px; font-weight: 700; margin-bottom: 4px; }
.kpi-label { font-size: 13px; color: #605E5C; }
.kpi-sub { font-size: 11px; color: #888780; margin-top: 2px; }
.insight-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
.insight-card { background: #fff; border-radius: 10px; padding: 16px 16px 16px 20px;
                 box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
.insight-icon { font-size: 20px; margin-bottom: 6px; }
.insight-title { font-size: 13px; font-weight: 600; color: #333; margin-bottom: 6px; }
.insight-text { font-size: 13px; color: #605E5C; line-height: 1.5; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; margin-top: 16px; }
.card { background: #fff; border-radius: 10px; padding: 18px; box-shadow: 0 1px 6px rgba(0,0,0,0.08); }
.card.full-width { grid-column: 1 / -1; }
.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }
.card-title { font-size: 14px; font-weight: 600; color: #201F1E; }
.card-meta { font-size: 11px; color: #888780; text-align: right; }
.n-label { font-size: 11px; color: #888780; margin-right: 6px; }
.chart-type { font-size: 10px; background: #f3f2f1; color: #888; padding: 2px 6px; border-radius: 4px; }
.dutch-label { font-size: 11px; color: #aaa; margin-bottom: 10px; font-style: italic; }
.badge { display: inline-block; border-radius: 12px; padding: 2px 10px; font-size: 11px;
          background: #605E5C; color: white; margin-left: 8px; }
.placeholder-card { background: #F3F2F1; border: 1px dashed #ccc; }
.placeholder-msg { font-size: 13px; color: #888780; font-style: italic; padding: 12px 0; }
.caveat { font-size: 12px; color: #888780; font-style: italic; padding: 8px 0; }
.small-table { border-collapse: collapse; font-size: 12px; margin-top: 8px; }
.small-table th, .small-table td { border: 1px solid #e0e0e0; padding: 4px 10px; }
.small-table th { background: #f5f5f3; }
.dive-card { grid-column: 1 / -1; }
.calc-note { font-size: 12px; color: #888780; font-style: italic; margin-bottom: 10px; }
.subsection { margin-bottom: 24px; }
.subsection-title { font-size: 15px; font-weight: 600; padding: 10px 0; cursor: pointer;
                     list-style: none; display: flex; align-items: center; gap: 8px; }
.subsection-title::before { content: "▶"; font-size: 10px; color: #7F77DD; }
details[open] .subsection-title::before { content: "▼"; }
.sentiment-section { margin-bottom: 32px; }
.sentiment-col-title { font-size: 15px; font-weight: 600; color: #333; margin-bottom: 8px;
                         display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.sentiment-badge { font-size: 11px; background: #F3F2F1; color: #605E5C; padding: 3px 10px;
                    border-radius: 12px; font-weight: normal; }
.comment-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; margin-top: 12px; }
.comment-card { border-radius: 8px; padding: 14px; border-left: 4px solid #888; }
.comment-card.positive { border-left-color: #1D9E75; background: #F0FAF6; }
.comment-card.neutral  { border-left-color: #888780; background: #F5F5F3; }
.comment-card.negative { border-left-color: #D85A30; background: #FDF2EE; }
.comment-card.mixed    { border-left-color: #EF9F27; background: #FEF8EE; }
.comment-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; flex-wrap: wrap; }
.sentiment-pill { font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 10px; }
.sentiment-pill.positive { background: #1D9E75; color: white; }
.sentiment-pill.neutral  { background: #888780; color: white; }
.sentiment-pill.negative { background: #D85A30; color: white; }
.sentiment-pill.mixed    { background: #EF9F27; color: white; }
.summary-label { font-size: 12px; color: #555; font-style: italic; }
.comment-text { font-size: 13px; color: #333; line-height: 1.5; margin-bottom: 8px; }
.theme-chips { display: flex; gap: 6px; flex-wrap: wrap; }
.chip { background: #F3F2F1; border-radius: 10px; padding: 2px 8px; font-size: 11px; color: #555; }
footer { text-align: center; padding: 24px; font-size: 12px; color: #888; }
@media (max-width: 760px) {
  main { padding: 16px; }
  .page-header { padding: 20px 16px; }
  .toc { padding: 0 8px; }
  .card-grid { grid-template-columns: 1fr; }
  .kpi-row { grid-template-columns: repeat(2, 1fr); }
}
"""

# ── HTML assembler ─────────────────────────────────────────────────────────────
def build_html(df, kpis, insights, qbyq_html, deepdives_html, sentiment_html) -> str:
    min_date = df["start_time"].min().strftime("%-d %b %Y") if "start_time" in df.columns else "?"
    max_date = df["start_time"].max().strftime("%-d %b %Y") if "start_time" in df.columns else "?"
    n_loc = df["location"].nunique() if "location" in df.columns else "?"
    n_workshops = df["workshop_s"].nunique() if "workshop_s" in df.columns else "?"
    n_weeks = df["iso_week"].nunique() if "iso_week" in df.columns else "?"
    n_teachers = 0
    n_students = len(df)

    subtitle = f"{len(df)} responses · {min_date} – {max_date} · {n_loc} locations · {n_workshops} workshop types"

    badges = [
        f'<span class="badge-item">👩‍🎓 {n_students} students</span>',
        f'<span class="badge-item">👩‍🏫 {n_teachers} teachers</span>',
        f'<span class="badge-item">📍 {n_loc} locations</span>',
        f'<span class="badge-item">🛠 {n_workshops} workshop types</span>',
        f'<span class="badge-item">📅 {n_weeks} week(s) of data</span>',
    ]

    generated_at = datetime.now().strftime("%d %b %Y %H:%M")

    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="generator" content="dreamspace_analysis.py">
  <title>DreamSpace NL — Survey Analysis Dashboard</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>{CSS}</style>
</head>
<body>

<header class="page-header">
  <div class="page-title">DreamSpace NL — Survey Analysis Dashboard</div>
  <div class="page-subtitle">{html.escape(subtitle)}</div>
  <div class="badge-row">{''.join(badges)}</div>
</header>

<nav class="toc">
  <a href="#s1">📊 KPI Summary</a>
  <a href="#s2">💡 Key Insights</a>
  <a href="#s3">📋 All Questions</a>
  <a href="#s4">🔍 Deep Dives</a>
  <a href="#s5">💬 Sentiment</a>
</nav>

<main>

  <section class="section" id="s1">
    <div class="section-header">📊 KPI Summary</div>
    {build_kpi_row(kpis)}
  </section>

  <section class="section" id="s2">
    <div class="section-header">💡 Key Insights</div>
    {build_insights_row(insights)}
  </section>

  <section class="section" id="s3">
    <div class="section-header">📋 All survey responses — question by question</div>
    {qbyq_html}
  </section>

  <section class="section" id="s4">
    <div class="section-header">🔍 Analytical deep-dives</div>
    <div class="card-grid">{deepdives_html}</div>
  </section>

  <section class="section" id="s5">
    <div class="section-header">💬 Open-ended feedback &amp; sentiment analysis</div>
    {sentiment_html}
  </section>

</main>

<footer>
  Generated by dreamspace_analysis.py · {html.escape(generated_at)} ·
  Data: {len(df)} responses · {html.escape(min_date)} – {html.escape(max_date)}
</footer>

</body>
</html>"""

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="DreamSpace NL survey dashboard generator")
    parser.add_argument("xlsx", nargs="?", default="Results.xlsx", help="Path to Results.xlsx")
    parser.add_argument("--output", default="dreamspace_report.html")
    parser.add_argument("--no-sentiment", action="store_true", help="Skip sentiment analysis")
    args = parser.parse_args()

    xlsx_path = Path(args.xlsx)
    if not xlsx_path.exists():
        print(f"❌ File not found: {xlsx_path}")
        sys.exit(1)

    print("🔍 Loading data...")
    df = load_data(str(xlsx_path))
    print(f"   {len(df)} rows · {len(df.columns)} columns")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set — sentiment analysis will be skipped.")
    elif args.no_sentiment:
        print("   --no-sentiment flag set — skipping sentiment analysis.")

    print("📊 Computing KPIs...")
    kpis = compute_kpis(df)

    print("💡 Running sentiment analysis...")
    if api_key and not args.no_sentiment:
        sentiment_html, sentiment_results = build_sentiment_section(df)
    else:
        sentiment_html, sentiment_results = build_sentiment_section.__wrapped__(df) if hasattr(build_sentiment_section, '__wrapped__') else ('<div class="card placeholder-card"><div class="card-title">Sentiment analysis</div><p>Set <code>ANTHROPIC_API_KEY</code> and re-run to enable sentiment analysis.</p></div>', {})
        if not api_key or args.no_sentiment:
            sentiment_html = '<div class="card placeholder-card"><div class="card-title">Sentiment analysis — not available</div><p>Set the <code>ANTHROPIC_API_KEY</code> environment variable and re-run to enable AI-powered sentiment analysis.</p><pre style="background:#f5f5f3;padding:12px;border-radius:6px;font-size:12px">export ANTHROPIC_API_KEY=sk-ant-...\npython dreamspace_analysis.py Results.xlsx</pre></div>'
            sentiment_results = {}

    print("💡 Computing insights...")
    insights = compute_insights(df, sentiment_results)

    print("📋 Building Q-by-Q section...")
    qbyq_html = build_qbyq(df)

    print("🔍 Building deep-dives...")
    deepdives_html = build_deepdives(df)

    print("🏗  Assembling HTML...")
    final_html = build_html(df, kpis, insights, qbyq_html, deepdives_html, sentiment_html)

    out_path = xlsx_path.parent / args.output
    out_path.write_text(final_html, encoding="utf-8")
    print(f"✅ Report saved → {out_path}")

if __name__ == "__main__":
    main()
