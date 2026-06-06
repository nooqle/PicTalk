#!/usr/bin/env python3
"""Render PicTalk storyboard JSON to PNG images using locked HTML layouts.

Usage:
    python render_storyboard.py <storyboard.json> [--template <template.html>] [--output-dir <dir>] [--keep-html]

The renderer is intentionally low-freedom: every supported layout has an explicit
HTML skeleton. Unsupported layouts fail instead of silently degrading to a card grid.
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: playwright is required. Install with: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(2)


DEFAULT_WIDTH = 1086
DEFAULT_HEIGHT = 1448


ICONS = {
    "book-open": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/><circle cx="17" cy="14" r="3"/><path d="m19.2 16.2 2 2"/></svg>',
    "folder": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h6l2 2h8v10a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2z"/></svg>',
    "edit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
    "network": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><path d="M10.6 7.6 6.4 16.4"/><path d="m13.4 7.6 4.2 8.8"/><path d="M8 19h8"/></svg>',
    "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"/><circle cx="10" cy="7" r="4"/><path d="M21 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
    "trophy": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 21h8"/><path d="M12 17v4"/><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M17 6h3a2 2 0 0 1-2 2h-1"/><path d="M7 6H4a2 2 0 0 0 2 2h1"/></svg>',
    "target": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/><path d="m16 8 4-4"/><path d="m16 4h4v4"/></svg>',
    "layers": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m12 2 10 5-10 5L2 7z"/><path d="m2 12 10 5 10-5"/><path d="m2 17 10 5 10-5"/></svg>',
    "clipboard": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="4" width="12" height="18" rx="2"/><path d="M9 4a3 3 0 0 1 6 0"/><path d="M9 11h6"/><path d="M9 16h6"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m20 6-11 11-5-5"/></svg>',
    "code": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m8 9-4 3 4 3"/><path d="m16 9 4 3-4 3"/><path d="m14 4-4 16"/></svg>',
    "refresh": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 0 1-15.5 6.2"/><path d="M3 12A9 9 0 0 1 18.5 5.8"/><path d="M18 2v5h-5"/><path d="M6 22v-5h5"/></svg>',
    "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v7"/><path d="M12 15v7"/><path d="M2 12h7"/><path d="M15 12h7"/><path d="m5 5 5 5"/><path d="m14 14 5 5"/><path d="m19 5-5 5"/><path d="m10 14-5 5"/></svg>',
    "log-in": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="M10 17l5-5-5-5"/><path d="M15 12H3"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h3l2-3h6l2 3h3a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2z"/><circle cx="12" cy="14" r="4"/></svg>',
    "upload": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 16V4"/><path d="m7 9 5-5 5 5"/><path d="M4 20h16"/></svg>',
    "scan": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7V5a1 1 0 0 1 1-1h2"/><path d="M17 4h2a1 1 0 0 1 1 1v2"/><path d="M20 17v2a1 1 0 0 1-1 1h-2"/><path d="M7 20H5a1 1 0 0 1-1-1v-2"/><path d="M7 12h10"/><path d="M12 7v10"/></svg>',
    "report": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h9l3 3v15H6z"/><path d="M15 3v4h4"/><path d="M9 17v-5"/><path d="M13 17V9"/><path d="M17 17v-3"/></svg>',
    "stream": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h10"/><path d="M4 12h16"/><path d="M4 17h12"/><path d="m18 8 3 4-3 4"/></svg>',
    "meal": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11h16a8 8 0 0 1-16 0z"/><path d="M7 11c0-3 2-5 5-5s5 2 5 5"/><path d="M8 21h8"/></svg>',
    "umbrella": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11a9 9 0 0 1 18 0z"/><path d="M12 11v8a3 3 0 0 0 6 0"/><path d="M7 11a5 5 0 0 1 10 0"/></svg>',
    "flame": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c4 0 7-3 7-7 0-3-1.6-5.4-4.8-8.1-.2 2-1.2 3.5-2.7 4.6.2-3-1.1-5.9-4-8.5.3 3.5-2.5 5.5-2.5 9.6A7 7 0 0 0 12 22z"/><path d="M12 18a3 3 0 0 0 3-3c0-1.2-.6-2.3-1.8-3.3-.1 1-.6 1.8-1.4 2.3.1-1.5-.5-2.9-2-4.2.2 1.8-1.3 2.8-1.3 4.8A3.5 3.5 0 0 0 12 18z"/></svg>',
    "eye": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 12s3.5-6 9.5-6 9.5 6 9.5 6-3.5 6-9.5 6-9.5-6-9.5-6z"/><circle cx="12" cy="12" r="3"/></svg>',
    "vase": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6"/><path d="M10 3v4l-3 4v8a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-8l-3-4V3"/><path d="M8 13h8"/><path d="M9 17h6"/></svg>',
    "wheel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="2"/><path d="M12 4v6"/><path d="M12 14v6"/><path d="M4 12h6"/><path d="M14 12h6"/><path d="m6.3 6.3 4.2 4.2"/><path d="m13.5 13.5 4.2 4.2"/><path d="m17.7 6.3-4.2 4.2"/><path d="m10.5 13.5-4.2 4.2"/></svg>',
    "scroll": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M8 5h10a3 3 0 0 1 0 6H8"/><path d="M8 11h8a3 3 0 0 1 0 6H6"/><path d="M6 17a3 3 0 0 1 0-6h2"/><path d="M8 5a3 3 0 0 0 0 6"/><path d="M6 17a3 3 0 0 0 0-6"/></svg>',
}

ICON_ALIASES = {
    "box": "layers",
    "stack": "layers",
    "globe": "network",
    "map-pin": "target",
    "type": "edit",
    "share": "network",
    "book": "book-open",
    "file-text": "clipboard",
    "login": "log-in",
    "photo": "camera",
    "meal-photo": "meal",
    "recognition": "scan",
    "analysis": "scan",
    "chart": "report",
}

THEME_COLORS = ["blue", "green", "orange", "purple", "gray"]
TONE_COLORS = {
    "blue": "#0757D8",
    "green": "#128348",
    "orange": "#E77800",
    "purple": "#5A2BAE",
    "gray": "#6B7280",
}


def tone_class(value: Any, fallback: str = "blue") -> str:
    tone = str(value or "").strip().lower()
    return tone if tone in TONE_COLORS else fallback


def first_text(value: Any) -> str:
    if isinstance(value, list):
        return str(value[0]) if value else ""
    return str(value or "")


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def icon(name: str | None) -> str:
    key = ICON_ALIASES.get(name or "", name or "layers")
    return ICONS.get(key, ICONS["layers"])


def motif_visual(item: dict[str, Any], tone: str, base_icon: str | None = None) -> str:
    icons = item.get("motif_icons") or [item.get("icon") or base_icon or "layers"]
    if not isinstance(icons, list):
        icons = [icons]
    clean_icons = [str(value) for value in icons if value][:3] or [str(item.get("icon") or base_icon or "layers")]
    primary = clean_icons[0]
    primary_key = ICON_ALIASES.get(primary, primary)
    style = str(item.get("visual_style") or ("single" if len(clean_icons) == 1 else "constellation"))
    if style not in {"single", "stack", "constellation", "shield", "bridge", "pyramid"}:
        style = "single" if len(clean_icons) == 1 else "constellation"

    # A motif is allowed one semantic icon only. Extra depth must be expressed
    # through geometric decoration so small diagram anchors do not become
    # repeated, overlapped icon piles.
    return f"""
        <div class="visual-motif motif-{esc(style)} tone-{tone}" data-motif-icon="{esc(primary_key)}">
          <span class="motif-decor decor-a"></span>
          <span class="motif-decor decor-b"></span>
          <span class="motif-decor decor-c"></span>
          <span class="motif-symbol">{icon(primary)}</span>
        </div>"""


def color_class(index: int, preferred: str | None = None) -> str:
    if preferred in {"blue", "green", "orange", "purple", "gray"}:
        return preferred
    return THEME_COLORS[index % 4]


def card_canvas(card: dict[str, Any]) -> tuple[int, int]:
    canvas = card.get("canvas") or {}
    return int(canvas.get("width", DEFAULT_WIDTH)), int(canvas.get("height", DEFAULT_HEIGHT))


def title_block(card: dict[str, Any]) -> str:
    subtitle = card.get("subtitle", "")
    subtitle_html = f'<div class="subtitle-row">{esc(subtitle)}</div>' if subtitle else ""
    return f"""
    <div class="title-block">
      <h1>{esc(card.get("title", ""))}</h1>
      {subtitle_html}
    </div>"""


def top_flow(card: dict[str, Any]) -> str:
    items = card.get("top_flow") or []
    if not items:
        return ""
    chunks = []
    for item in items:
        chunks.append(
            f"""
      <div class="flow-item">
        <div class="flow-icon">{icon(item.get("icon"))}</div>
        <div class="flow-label">{esc(item.get("label", ""))}</div>
        <div class="flow-arrow">→</div>
      </div>"""
        )
    return f'<div class="top-flow" style="--flow-count:{len(items)}">{"".join(chunks)}</div>'


def section_list(section: dict[str, Any]) -> str:
    body = section.get("body") or []
    if not body:
        return ""
    return '<ul class="section-body">' + "".join(f"<li>{esc(item)}</li>" for item in body) + "</ul>"


def metrics(card: dict[str, Any]) -> str:
    metric_items = card.get("metrics") or []
    if not metric_items:
        return ""
    chunks = []
    for i, metric in enumerate(metric_items):
        color = metric.get("color") or {
            "blue": "#0757D8",
            "green": "#128348",
            "orange": "#E77800",
            "purple": "#5A2BAE",
        }.get(color_class(i), "#0757D8")
        chunks.append(
            f"""
      <div class="metric-card">
        <div class="metric-dot" style="background:{esc(color)}"></div>
        <div>
          <div class="metric-label">{esc(metric.get("label", ""))}</div>
          <div class="metric-value">{esc(metric.get("value", ""))}</div>
        </div>
      </div>"""
        )
    return f'<div class="metric-row" style="--metric-count:{len(metric_items)}">{"".join(chunks)}</div>'


def conclusion(card: dict[str, Any]) -> str:
    text = card.get("conclusion", "")
    if not text:
        return ""
    style = card.get("conclusion_style", "blue")
    return f"""
    <div class="conclusion-band {esc(style)}">
      <div class="band-icon">{icon(card.get("conclusion_icon", "target"))}</div>
      <div class="band-text">{esc(text)}</div>
    </div>"""


def sheet(card: dict[str, Any], layout_class: str, inner: str) -> str:
    width, height = card_canvas(card)
    return f"""
  <main class="sheet {esc(layout_class)}" style="--canvas-w:{width}px;--canvas-h:{height}px">
    {title_block(card)}
    {top_flow(card)}
    {inner}
    <div class="footer-note">{esc(card.get("footer_note", ""))}</div>
  </main>"""


def render_cycle(card: dict[str, Any]) -> str:
    positions = [
        "left:50%;top:18px;transform:translateX(-50%)",
        "right:20px;top:210px;transform:none",
        "right:46px;bottom:80px;transform:none",
        "left:50%;bottom:0;transform:translateX(-50%)",
        "left:20px;bottom:80px;transform:none",
        "left:20px;top:210px;transform:none",
    ]
    nodes = []
    for i, section in enumerate(card.get("sections", [])[:6]):
        cc = color_class(i, section.get("color"))
        nodes.append(
            f"""
      <div class="cycle-node panel" style="{positions[i]}">
        <div class="node-index">{i + 1}</div>
        <div class="node-icon iw-{cc}">{icon(section.get("icon"))}</div>
        <h3>{esc(section.get("heading", ""))}</h3>
        <p>{esc((section.get("body") or [""])[0])}</p>
      </div>"""
        )
    outputs_title = card.get("outputs_title", "关键产出")
    inner = f"""
    <section class="layout-region layout-cycle">
      <div class="cycle-canvas">
        <svg class="cycle-arrows" viewBox="0 0 980 650" fill="none" aria-hidden="true">
          <defs>
            <marker id="arrow-blue" markerWidth="10" markerHeight="10" refX="7" refY="5" orient="auto"><path d="M0 0 10 5 0 10Z" fill="#0757D8"/></marker>
          </defs>
          <path d="M498 132 C680 120 807 206 842 340" stroke="#8DB3FF" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-blue)" opacity=".68"/>
          <path d="M820 424 C735 575 580 625 422 580" stroke="#0757D8" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-blue)" opacity=".72"/>
          <path d="M330 568 C170 515 115 365 172 216" stroke="#0757D8" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-blue)" opacity=".72"/>
          <path d="M214 160 C284 92 370 80 456 110" stroke="#8DB3FF" stroke-width="10" stroke-linecap="round" marker-end="url(#arrow-blue)" opacity=".68"/>
          <path d="M490 154 C570 198 616 260 640 338" stroke="#0757D8" stroke-width="3" stroke-dasharray="7 9" marker-end="url(#arrow-blue)" opacity=".85"/>
        </svg>
        <div class="cycle-center"><div class="cycle-center-text">{esc(card.get("center_text", card.get("thesis", "")))}</div></div>
        {"".join(nodes)}
      </div>
      <div class="output-band">
        <div class="output-title">{esc(outputs_title)}</div>
        {metrics(card)}
      </div>
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-cycle-sheet", inner)


def render_transformation(card: dict[str, Any]) -> str:
    sections = card.get("sections", [])
    columns = []
    for i, section in enumerate(sections[:3]):
        tone = section.get("tone") or ("muted" if i == 0 else "primary" if i == 1 else "explore")
        cc = color_class(i, section.get("color"))
        columns.append(
            f"""
      <div class="transform-card panel {esc(tone)}">
        <div class="transform-head">
          <div class="icon-well iw-{cc}">{icon(section.get("icon"))}</div>
          <h2 class="section-title">{esc(section.get("heading", ""))}</h2>
        </div>
        {section_list(section)}
        <div class="transform-footer">{esc(section.get("footer", ""))}</div>
      </div>"""
        )
        if i < min(len(sections), 3) - 1:
            columns.append('<div class="big-arrow">→</div>')
    inner = f"""
    <section class="layout-region layout-transformation">
      <div class="transformation-grid">
        {"".join(columns)}
      </div>
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-transformation-sheet", inner)


def render_arrow_flow(card: dict[str, Any]) -> str:
    sections = card.get("sections", [])
    steps = []
    for i, section in enumerate(sections):
        cc = color_class(i, section.get("color"))
        steps.append(
            f"""
      <div class="flow-step panel">
        <div class="step-badge">{i + 1}</div>
        <div class="icon-well iw-{cc}">{icon(section.get("icon"))}</div>
        <div>
          <h2 class="section-title">{esc(section.get("heading", ""))}</h2>
          {section_list(section)}
        </div>
      </div>"""
        )
    inner = f"""
    <section class="layout-region layout-arrow-flow">
      <div class="flow-steps" style="--step-count:{len(sections)}">
        {"".join(steps)}
      </div>
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-arrow-flow-sheet", inner)


def render_timeline(card: dict[str, Any]) -> str:
    sections = card.get("sections", [])
    steps = []
    for i, section in enumerate(sections):
        steps.append(
            f"""
      <div class="timeline-card panel">
        <div class="timeline-dot">{esc(section.get("badge", i + 1))}</div>
        <h2 class="section-title">{esc(section.get("heading", ""))}</h2>
        {section_list(section)}
      </div>"""
        )
    inner = f"""
    <section class="layout-region layout-timeline">
      <div class="timeline" style="--step-count:{len(sections)}">
        {"".join(steps)}
      </div>
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-timeline-sheet", inner)


def render_matrix(card: dict[str, Any]) -> str:
    matrix = card.get("matrix") or {}
    columns = matrix.get("columns") or []
    rows = matrix.get("rows") or []
    cells = ['<div class="matrix-cell header"></div>']
    cells.extend(f'<div class="matrix-cell header">{esc(col)}</div>' for col in columns)
    for row in rows:
        cells.append(f'<div class="matrix-cell row-head">{esc(row.get("label", ""))}</div>')
        for value in row.get("values", [])[: len(columns)]:
            cells.append(f'<div class="matrix-cell">{esc(value)}</div>')
    inner = f"""
    <section class="layout-region layout-matrix">
      <div class="matrix-grid" style="--matrix-cols:{len(columns)}">
        {"".join(cells)}
      </div>
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-matrix-sheet", inner)


def render_layer_stack(card: dict[str, Any]) -> str:
    sections = card.get("sections", [])
    axis = card.get("axis") or {}
    upgrade_label = card.get("axis_label") or axis.get("label") or "层级逐级升级"
    layer_cards = []
    for i, section in enumerate(sections):
        cc = color_class(i, section.get("color"))
        layer_cards.append(
            f"""
      <div class="layer-card panel">
        <div class="layer-index">{esc(section.get("badge", i + 1))}</div>
        <div>
          <div class="icon-well iw-{cc}" style="float:left;margin-right:14px">{icon(section.get("icon"))}</div>
          <h2 class="section-title">{esc(section.get("heading", ""))}</h2>
          {section_list(section)}
          <div class="transform-footer">{esc(section.get("footer", ""))}</div>
        </div>
      </div>"""
        )

    side_sections = card.get("side_sections") or []
    if side_sections:
        side = '<div class="side-levels">'
        for i, item in enumerate(side_sections):
            cc = color_class(i, item.get("color"))
            side += f"""
        <div class="side-level panel">
          <div class="badge-icon iw-{cc}">{icon(item.get("icon", "users"))}</div>
          <h3>{esc(item.get("heading", ""))}</h3>
          <p>{esc(" / ".join(item.get("body", [])))}</p>
        </div>"""
        side += "</div>"
        body = f"""
      <div class="hierarchy-body">
        <div class="demand-arrow"><div>{esc(upgrade_label)}</div></div>
        <div class="layer-stack" style="--step-count:{len(sections)}">{"".join(layer_cards)}</div>
        {side}
      </div>"""
    else:
        body = f"""
      <div class="layer-wrap">
        <div class="layer-stack" style="--step-count:{len(sections)}">{"".join(layer_cards)}</div>
        <div class="side-note panel">
          <h3>{esc(card.get("side_note_title", "层级指示"))}</h3>
          <p>{esc(card.get("side_note", card.get("thesis", "")))}</p>
        </div>
      </div>"""

    inner = f"""
    <section class="layout-region layout-layer-stack">
      {body}
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "layout-layer-stack-sheet", inner)


def render_premium_hierarchy_diffusion(card: dict[str, Any]) -> str:
    labels = {
        "typical_behavior": "表现线索",
        "core_blocker": "关键阻碍",
        "matched_audience": "适配场景",
    }
    labels.update(card.get("field_labels") or {})

    layers = card.get("layers") or []
    tiers = card.get("tiers") or card.get("user_tiers") or []
    mechanisms = card.get("mechanisms") or []
    summaries = card.get("summary_cards") or []
    axis = card.get("axis") or {}
    tier_callout = card.get("tier_callout") or {}

    layer_chunks = []
    layer_keys: dict[str, int] = {}
    visual_layers = sorted(
        enumerate(layers),
        key=lambda item: int(str(item[1].get("no", item[0] + 1)).strip() or item[0] + 1)
        if str(item[1].get("no", item[0] + 1)).strip().isdigit()
        else item[0] + 1,
        reverse=True,
    )
    visual_layer_position: dict[int, int] = {}
    for visual_index, (original_index, layer) in enumerate(visual_layers):
        tone = tone_class(layer.get("tone"), color_class(visual_index))
        for key in [layer.get("id"), layer.get("no"), layer.get("title")]:
            if key is not None:
                layer_keys[str(key)] = visual_index
        visual_layer_position[original_index] = visual_index
        layer_chunks.append(
            f"""
        <article class="benchmark-layer panel tone-{tone}">
          <div class="benchmark-layer-no">{esc(layer.get("no", visual_index + 1))}</div>
          <div class="benchmark-icon-block tone-{tone}">
            {motif_visual(layer, tone, layer.get("icon"))}
          </div>
          <div class="benchmark-layer-copy">
            <div class="premium-layer-head">
              <h2>{esc(layer.get("title", ""))}</h2>
              <span>{esc(layer.get("type", ""))}</span>
            </div>
            <div class="benchmark-facts">
              <div><b>{esc(labels["typical_behavior"])}</b><p>{esc(layer.get("typical_behavior", ""))}</p></div>
              <div><b>{esc(labels["core_blocker"])}</b><p>{esc(layer.get("core_blocker", ""))}</p></div>
              <div><b>{esc(labels["matched_audience"])}</b><p>{esc(layer.get("matched_audience", ""))}</p></div>
            </div>
            <div class="benchmark-essence"><b>{esc(card.get("essence_label", "结构本质"))}</b><span>{esc(layer.get("essence", ""))}</span></div>
          </div>
        </article>"""
        )

    tier_chunks = []
    tier_keys: dict[str, int] = {}
    visual_tiers = sorted(
        tiers,
        key=lambda tier: str(tier.get("label", "")),
        reverse=True,
    )
    for i, tier in enumerate(visual_tiers):
        tone = tone_class(tier.get("tone"), color_class(i, "green" if i == 0 else None))
        label = str(tier.get("label", ""))
        for key in [tier.get("id"), label, label.split()[0] if label else None]:
            if key is not None:
                tier_keys[str(key)] = i
        body = tier.get("body") or []
        rank_class = " is-top" if i == 0 else ""
        tier_visual = f'<div class="tier-motif-wrap">{motif_visual(tier, tone, tier.get("icon", "layers"))}</div>'
        tier_chunks.append(
            f"""
        <article class="benchmark-tier tone-{tone}{rank_class}">
          {tier_visual}
          <div class="tier-copy">
            <div class="tier-label">{esc(label)}</div>
            <h3>{esc(tier.get("headline", ""))}</h3>
            <p>{esc(" / ".join(str(item) for item in body))}</p>
          </div>
        </article>"""
        )

    connector_paths = []
    connectors = card.get("connectors") or []
    for connector in connectors:
        layer_index = layer_keys.get(str(connector.get("from_layer")))
        tier_index = tier_keys.get(str(connector.get("to_tier")))
        if layer_index is None or tier_index is None:
            continue
        y1 = 102 + layer_index * 200
        y2 = 248 + tier_index * 205
        color = TONE_COLORS[tone_class(connector.get("tone"), "blue")]
        marker = f"hierarchy-arrow-{tone_class(connector.get('tone'), 'blue')}"
        connector_paths.append(
            f'<path d="M690 {y1} C735 {y1} 708 {y2} 748 {y2}" '
            f'stroke="{esc(color)}" stroke-width="4" fill="none" '
            f'stroke-linecap="round" stroke-dasharray="{esc("10 8" if connector.get("kind") == "dashed-arrow" else "0")}" '
            f'marker-end="url(#{marker})" opacity=".68"/>'
        )

    callout_html = ""
    if isinstance(tier_callout, dict) and tier_callout.get("text"):
        tone = tone_class(tier_callout.get("tone"), "orange")
        callout_html = f"""
          <div class="tier-callout tone-{tone}">
            <div class="tier-callout-icon">{icon(tier_callout.get("icon", "trophy"))}</div>
            <div>{esc(tier_callout.get("text", ""))}</div>
          </div>"""

    mechanism_chunks = []
    default_mechanism_icons = ["clipboard", "users", "layers"]
    for i, mechanism in enumerate(mechanisms):
        tone = tone_class(mechanism.get("tone"), color_class(i))
        arrow = '<div class="mechanism-link-arrow">→</div>' if i < len(mechanisms) - 1 else ""
        mechanism_icon = mechanism.get("icon") or default_mechanism_icons[i % len(default_mechanism_icons)]
        mechanism_chunks.append(
            f"""
        <article class="benchmark-mechanism panel tone-{tone}">
          <div class="mechanism-icon-badge iw-{tone}">
            <span>{esc(mechanism.get("no", i + 1))}</span>
            {icon(mechanism_icon)}
          </div>
          <div>
            <h3>{esc(mechanism.get("title", ""))}</h3>
            <p>{esc(mechanism.get("body", ""))}</p>
          </div>
        </article>{arrow}"""
        )

    summary_chunks = []
    default_summary_icons = ["trophy", "network", "target"]
    for i, summary in enumerate(summaries):
        tone = tone_class(summary.get("tone"), color_class(i))
        summary_icon = summary.get("icon") or default_summary_icons[i % len(default_summary_icons)]
        summary_chunks.append(
            f"""
        <article class="benchmark-summary-card panel tone-{tone}">
          <div class="summary-icon-badge iw-{tone}">{icon(summary_icon)}</div>
          <div>
            <h3>{esc(summary.get("title", ""))}</h3>
            <p>{esc(summary.get("body", ""))}</p>
          </div>
        </article>"""
        )

    inner = f"""
    <section class="layout-region premium-hierarchy">
      <div class="premium-hierarchy-main">
        <div class="layer-rail"><div>{esc(axis.get("label", ""))}</div></div>
        <div class="benchmark-layer-stack">{"".join(layer_chunks)}</div>
        <svg class="premium-connectors" viewBox="0 0 1074 812" aria-hidden="true">
          <defs>
            <marker id="hierarchy-arrow-blue" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 12 6 0 12Z" fill="#0757D8"/></marker>
            <marker id="hierarchy-arrow-green" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 12 6 0 12Z" fill="#128348"/></marker>
            <marker id="hierarchy-arrow-orange" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 12 6 0 12Z" fill="#E77800"/></marker>
            <marker id="hierarchy-arrow-purple" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 12 6 0 12Z" fill="#5A2BAE"/></marker>
          </defs>
          {"".join(connector_paths)}
        </svg>
        <aside class="benchmark-tier-panel panel">
          <div class="tier-panel-title">{esc(card.get("tiers_title", "关联层级"))}</div>
          {callout_html}
          <div class="benchmark-tier-stack">{"".join(tier_chunks)}</div>
        </aside>
      </div>
      <div class="premium-row-title">{esc(card.get("mechanisms_title", "扩散机制"))}</div>
      <div class="benchmark-mechanism-chain">{"".join(mechanism_chunks)}</div>
      <div class="premium-row-title summary-title">{esc(card.get("summary_title", "结构判断"))}</div>
      <div class="benchmark-summary-row">{"".join(summary_chunks)}</div>
      {conclusion(card)}
    </section>"""
    return sheet(card, "premium-sheet premium-hierarchy-sheet", inner)


def render_premium_cycle_system(card: dict[str, Any]) -> str:
    center = card.get("center") or {}
    center_lines = center.get("lines") or []
    center_html = f"""
      <div class="cycle-core-halo"></div>
      <div class="premium-cycle-center">
        <h2>{esc(center.get("main", ""))}</h2>
        {"".join(f"<p>{esc(line)}</p>" for line in center_lines)}
      </div>"""

    nodes = card.get("loop_nodes") or []
    positions_6 = [
        "left:50%;top:0;transform:translateX(-50%)",
        "right:18px;top:168px",
        "right:58px;top:548px",
        "left:50%;bottom:0;transform:translateX(-50%)",
        "left:58px;top:548px",
        "left:18px;top:168px",
    ]
    positions_5 = [
        "left:50%;top:0;transform:translateX(-50%)",
        "right:24px;top:218px",
        "right:138px;bottom:38px",
        "left:138px;bottom:38px",
        "left:24px;top:218px",
    ]
    positions = positions_6 if len(nodes) >= 6 else positions_5
    node_chunks = []
    for i, node in enumerate(nodes[:6]):
        tone = tone_class(node.get("tone"), color_class(i))
        node_chunks.append(
            f"""
        <article class="premium-loop-node panel tone-{tone} slot-{i + 1}" style="{positions[i]}">
          <div class="loop-no">{esc(node.get("no", i + 1))}</div>
          <div class="premium-icon loop-icon iw-{tone}">{icon(node.get("icon"))}</div>
          <div class="loop-copy">
            <h3>{esc(node.get("title", ""))}</h3>
            <p>{esc(node.get("subtitle", ""))}</p>
          </div>
        </article>"""
        )

    output_chunks = []
    for i, output in enumerate(card.get("outputs") or []):
        tone = tone_class(output.get("tone"), color_class(i))
        output_chunks.append(
            f"""
        <article class="premium-output panel tone-{tone}">
          <div class="premium-icon iw-{tone}">{icon(output.get("icon"))}</div>
          <div>
            <h3>{esc(output.get("title", ""))}</h3>
            <p>{esc(output.get("body", ""))}</p>
          </div>
        </article>"""
        )

    cycle_conclusion = ""
    if card.get("conclusion"):
        cycle_conclusion = f"""
      <div class="cycle-conclusion-note panel">
        <div class="cycle-conclusion-icon">{icon(card.get("conclusion_icon", "target"))}</div>
        <p>{esc(card.get("conclusion", ""))}</p>
      </div>"""

    inner = f"""
    <section class="layout-region premium-cycle">
      <div class="premium-cycle-canvas">
        <svg class="premium-cycle-arrows" viewBox="0 0 990 880" aria-hidden="true">
          <defs>
            <marker id="cycle-premium-arrow" markerWidth="14" markerHeight="14" refX="11" refY="7" orient="auto" markerUnits="userSpaceOnUse">
              <path d="M0 0 14 7 0 14Z" fill="#0757D8"/>
            </marker>
          </defs>
          <circle cx="495" cy="430" r="378" stroke="#D7E5FF" stroke-width="2" fill="none" opacity=".54"/>
          <path d="M592.8 64.9 A378 378 0 0 1 796.9 202.5" stroke="#7AA7FF" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".78"/>
          <path d="M843.0 282.3 A378 378 0 0 1 831.8 601.6" stroke="#0757D8" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".74"/>
          <path d="M771.5 687.8 A378 378 0 0 1 541.1 805.2" stroke="#7AA7FF" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".78"/>
          <path d="M448.9 805.2 A378 378 0 0 1 218.5 687.8" stroke="#0757D8" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".74"/>
          <path d="M147.0 577.7 A378 378 0 0 1 158.2 258.4" stroke="#0757D8" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".74"/>
          <path d="M218.5 172.2 A378 378 0 0 1 448.9 54.8" stroke="#7AA7FF" stroke-width="7.6" fill="none" stroke-linecap="round" marker-end="url(#cycle-premium-arrow)" opacity=".78"/>
        </svg>
        {center_html}
        {"".join(node_chunks)}
      </div>
      <div class="premium-row-title cycle-output-title">{esc(card.get("outputs_title", "关键产出"))}</div>
      <div class="premium-output-grid" style="--output-count:{len(card.get("outputs") or [])}">{"".join(output_chunks)}</div>
      {cycle_conclusion}
    </section>"""
    return sheet(card, "premium-sheet premium-cycle-sheet", inner)


def render_premium_transformation_logic(card: dict[str, Any]) -> str:
    zones = card.get("zones") or []
    relations = card.get("relations") or []
    chunks = []
    role_classes = ["input", "gate", "output"]
    role_icons = ["spark", "check", "network"]
    for i, zone in enumerate(zones[:3]):
        tone = tone_class(zone.get("tone"), "blue" if zone.get("emphasis") else color_class(i))
        bullets = zone.get("bullets") or []
        role = role_classes[i] if i < len(role_classes) else "output"
        bullet_icon = zone.get("bullet_icon") or (role_icons[i] if i < len(role_icons) else "check")
        insight = zone.get("insight", "")
        insight_html = f'<div class="zone-insight">{esc(insight)}</div>' if insight else ""
        bullet_html = "".join(
            f"""
            <li>
              <span class="zone-bullet-icon">{icon(bullet_icon)}</span>
              <span>{esc(item)}</span>
            </li>"""
            for item in bullets
        )
        chunks.append(
            f"""
        <article class="premium-zone panel tone-{tone} zone-role-{role} {'emphasis' if zone.get('emphasis') else ''}">
          <div class="zone-watermark">{icon(zone.get("icon"))}</div>
          <div class="zone-label">{esc(zone.get("label", ""))}</div>
          <div class="premium-icon iw-{tone}">{icon(zone.get("icon"))}</div>
          <h2>{esc(zone.get("title", ""))}</h2>
          {insight_html}
          <ul>{bullet_html}</ul>
          <div class="essence-pill">{esc(zone.get("essence", ""))}</div>
        </article>"""
        )
        if i < 2:
            relation = relations[i] if i < len(relations) else {}
            chunks.append(
                f"""
        <div class="premium-relation-arrow">
          <div class="relation-label">{esc(relation.get("label", ""))}</div>
          <div class="relation-arrow">→</div>
        </div>"""
            )

    artifact = card.get("conversion_artifact") or {}
    artifact_html = ""
    if isinstance(artifact, dict) and artifact.get("title"):
        tone = tone_class(artifact.get("tone"), "green")
        items = artifact.get("items") or []
        artifact_html = f"""
      <div class="conversion-artifact panel tone-{tone}">
        <div class="conversion-artifact-icon iw-{tone}">{icon(artifact.get("icon", "layers"))}</div>
        <div>
          <h3>{esc(artifact.get("title", ""))}</h3>
          <p>{esc(artifact.get("subtitle", ""))}</p>
        </div>
        <div class="artifact-item-row">{"".join(f'<span>{esc(item)}</span>' for item in items)}</div>
      </div>"""

    inner = f"""
    <section class="layout-region premium-transformation">
      <div class="premium-zone-grid">{"".join(chunks)}</div>
      {artifact_html}
      <div class="transformation-thesis panel">
        <div class="thesis-kicker">核心转化判断</div>
        <div class="thesis-text">{esc(card.get("thesis", ""))}</div>
      </div>
      {metrics(card)}
      {conclusion(card)}
    </section>"""
    return sheet(card, "premium-sheet premium-transformation-sheet", inner)


def render_premium_process_flow(card: dict[str, Any]) -> str:
    stages = card.get("stages") or []
    stage_chunks = []
    for i, stage in enumerate(stages[:4]):
        tone = tone_class(stage.get("tone"), color_class(i))
        body = stage.get("body") or []
        stage_chunks.append(
            f"""
        <article class="process-stage panel tone-{tone}">
          <div class="process-stage-top">
            <div class="process-no">{esc(stage.get("no", i + 1))}</div>
            <div class="process-icon iw-{tone}">{icon(stage.get("icon"))}</div>
          </div>
          <h2>{esc(stage.get("title", ""))}</h2>
          <p>{esc(stage.get("subtitle", ""))}</p>
          <ul>{"".join(f"<li>{esc(item)}</li>" for item in body)}</ul>
        </article>"""
        )
        if i < min(len(stages), 4) - 1:
            stage_chunks.append(
                f"""
        <div class="process-arrow tone-{tone}">
          <span></span>
          <b>→</b>
        </div>"""
            )

    stream = card.get("stream") or {}
    stream_items = stream.get("items") or []
    stream_html = ""
    if isinstance(stream, dict) and stream.get("title"):
        tone = tone_class(stream.get("tone"), "green")
        stream_html = f"""
      <div class="process-stream panel tone-{tone}">
        <div class="stream-icon iw-{tone}">{icon(stream.get("icon", "stream"))}</div>
        <div class="stream-copy">
          <h3>{esc(stream.get("title", ""))}</h3>
          <p>{esc(stream.get("subtitle", ""))}</p>
        </div>
        <div class="stream-lines">{"".join(f'<span style="--line:{index + 1}">{esc(item)}</span>' for index, item in enumerate(stream_items[:5]))}</div>
      </div>"""

    metric_chunks = []
    for i, item in enumerate(card.get("checkpoints") or []):
        tone = tone_class(item.get("tone"), color_class(i))
        metric_chunks.append(
            f"""
        <article class="process-checkpoint panel tone-{tone}">
          <div class="checkpoint-dot iw-{tone}">{icon(item.get("icon", "check"))}</div>
          <div>
            <h3>{esc(item.get("title", ""))}</h3>
            <p>{esc(item.get("body", ""))}</p>
          </div>
        </article>"""
        )

    inner = f"""
    <section class="layout-region premium-process-flow">
      <div class="process-spine">{"".join(stage_chunks)}</div>
      {stream_html}
      <div class="process-checkpoint-row">{"".join(metric_chunks)}</div>
      {conclusion(card)}
    </section>"""
    return sheet(card, "premium-sheet process-flow-sheet", inner)


RENDERERS = {
    "cycle": render_cycle,
    "transformation": render_transformation,
    "comparison": render_transformation,
    "arrow-flow": render_arrow_flow,
    "timeline": render_timeline,
    "matrix": render_matrix,
    "layer-stack": render_layer_stack,
    "premium-cycle-system": render_premium_cycle_system,
    "premium-hierarchy-diffusion": render_premium_hierarchy_diffusion,
    "premium-process-flow": render_premium_process_flow,
    "premium-transformation-logic": render_premium_transformation_logic,
}


def render_card_to_html(card: dict[str, Any], template_html: str) -> str:
    layout = card.get("layout_type")
    renderer = RENDERERS.get(layout)
    if not renderer:
        supported = ", ".join(sorted(RENDERERS))
        raise ValueError(f"Unsupported layout_type '{layout}'. Supported layouts: {supported}")
    content = renderer(card)
    width, height = card_canvas(card)
    style_vars = f"--canvas-w:{width}px;--canvas-h:{height}px;"
    return (
        template_html.replace("{{content}}", content)
        .replace("{{lang}}", esc(card.get("_lang", "zh-CN")))
        .replace("{{style_vars}}", style_vars)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render PicTalk storyboard to PNG images")
    parser.add_argument("storyboard", type=Path, help="Path to storyboard JSON file")
    parser.add_argument("--template", type=Path, default=None, help="Path to HTML template")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory for PNG files")
    parser.add_argument("--keep-html", action="store_true", help="Keep intermediate HTML files for inspection")
    args = parser.parse_args()

    storyboard_path = args.storyboard
    if not storyboard_path.exists():
        print(f"File not found: {storyboard_path}", file=sys.stderr)
        return 2

    template_path = args.template or Path(__file__).parent.parent / "assets" / "template-infographic.html"
    if not template_path.exists():
        print(f"Template not found: {template_path}", file=sys.stderr)
        return 2

    output_dir = args.output_dir or storyboard_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        data = json.loads(storyboard_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid storyboard JSON: {exc}", file=sys.stderr)
        return 1

    cards = data.get("cards", [])
    if not cards:
        print("No cards found in storyboard", file=sys.stderr)
        return 1

    template_html = template_path.read_text(encoding="utf-8")
    rendered_files: list[Path] = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            for card in cards:
                card_id = card["id"]
                width, height = card_canvas(card)
                page.set_viewport_size({"width": width, "height": height})
                html_content = render_card_to_html(card, template_html)

                tmp_html = output_dir / f"{card_id}.html"
                tmp_html.write_text(html_content, encoding="utf-8")

                page.goto(f"file:///{tmp_html.resolve().as_posix()}")
                page.wait_for_timeout(700)

                png_path = output_dir / f"{card_id}.png"
                page.screenshot(
                    path=str(png_path),
                    full_page=False,
                    clip={"x": 0, "y": 0, "width": width, "height": height},
                    type="png",
                )
                rendered_files.append(png_path)
                print(f"Rendered: {png_path}")

                if not args.keep_html:
                    tmp_html.unlink()

            browser.close()
    except Exception as exc:  # noqa: BLE001 - CLI should report a concise renderer failure.
        print(f"Render failed: {exc}", file=sys.stderr)
        return 1

    print(f"\nDone. {len(rendered_files)} image(s) rendered.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
