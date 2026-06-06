#!/usr/bin/env python3
"""Run basic visual QA checks against rendered PicTalk HTML files."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "Error: playwright is required. Install with: pip install playwright && playwright install chromium",
        file=sys.stderr,
    )
    sys.exit(2)


CHECK_SELECTOR = (
    ".panel,.conclusion-band,.top-flow,.premium-hierarchy-main,.premium-zone-grid,"
    ".premium-cycle-canvas,.metric-card,.transformation-thesis,.conversion-artifact,"
    ".cycle-phase-chip,.process-spine,.process-stage,.process-stream,.process-checkpoint"
)

TEXT_SELECTOR = (
    "h1,h2,h3,p,li,.flow-label,.band-text,.metric-label,.metric-value,"
    ".essence-pill,.tier-label,.tier-callout,.tier-panel-title,.premium-row-title,"
    ".benchmark-essence,.benchmark-facts b,.benchmark-facts p,.premium-layer-head span,"
    ".thesis-kicker,.thesis-text,.zone-label,.zone-insight,.artifact-item-row span,"
    ".conversion-artifact h3,.conversion-artifact p,.cycle-phase-chip span,"
    ".process-stage h2,.process-stage p,.process-stage li,.process-stream h3,.process-stream p,"
    ".stream-lines span,.process-checkpoint h3,.process-checkpoint p"
)


def qa_html(path: Path) -> list[str]:
    errors: list[str] = []
    html = path.read_text(encoding="utf-8")
    width_matches = re.findall(r"--canvas-w\s*:\s*(\d+)px", html)
    height_matches = re.findall(r"--canvas-h\s*:\s*(\d+)px", html)
    viewport_width = int(width_matches[-1]) if width_matches else 1086
    viewport_height = int(height_matches[-1]) if height_matches else 1448
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": viewport_width, "height": viewport_height})
        page.goto(f"file:///{path.resolve().as_posix()}")
        page.wait_for_timeout(250)

        viewport = page.evaluate(
            "() => ({ width: document.documentElement.clientWidth, height: document.documentElement.clientHeight })"
        )
        boxes = page.eval_on_selector_all(
            CHECK_SELECTOR,
            """(els) => els
              .filter((el) => {
                const r = el.getBoundingClientRect();
                const s = getComputedStyle(el);
                return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none';
              })
              .map((el) => {
                const r = el.getBoundingClientRect();
                return { cls: el.className || el.tagName, x: r.x, y: r.y, right: r.right, bottom: r.bottom };
              })""",
        )
        for box in boxes:
            if box["x"] < -1 or box["y"] < -1 or box["right"] > viewport["width"] + 1 or box["bottom"] > viewport["height"] + 1:
                errors.append(
                    f"{path.name}: element out of viewport: {box['cls']} "
                    f"({box['x']:.1f},{box['y']:.1f},{box['right']:.1f},{box['bottom']:.1f})"
                )

        clipped = page.eval_on_selector_all(
            TEXT_SELECTOR,
            """(els) => els
              .filter((el) => {
                const r = el.getBoundingClientRect();
                const s = getComputedStyle(el);
                const text = (el.innerText || el.textContent || '').trim();
                if (!text || r.width <= 0 || r.height <= 0 || s.visibility === 'hidden' || s.display === 'none') return false;
                return el.scrollWidth > el.clientWidth + 2 || el.scrollHeight > el.clientHeight + 2;
              })
              .map((el) => {
                const text = (el.innerText || el.textContent || '').trim();
                return { cls: el.className || el.tagName, text: text.slice(0, 80), sw: el.scrollWidth, cw: el.clientWidth, sh: el.scrollHeight, ch: el.clientHeight };
              })""",
        )
        for item in clipped:
            errors.append(
                f"{path.name}: possible clipped text in {item['cls']}: {item['text']} "
                f"({item['sw']}x{item['sh']} scroll vs {item['cw']}x{item['ch']} client)"
            )

        layout_errors = page.evaluate(
            """() => {
              const errors = [];
              const text = (sel) => Array.from(document.querySelectorAll(sel)).map((el) => (el.innerText || el.textContent || '').trim()).filter(Boolean);
              if (document.querySelector('.premium-cycle')) {
                if (document.querySelectorAll('.premium-loop-node').length < 5) errors.push('premium-cycle requires at least 5 loop nodes');
                if (document.querySelectorAll('.cycle-phase-chip').length < 4) errors.push('premium-cycle requires at least 4 phase chips around the center');
                if (document.querySelectorAll('.premium-output').length < 3) errors.push('premium-cycle requires at least 3 output cards');
                if (document.querySelectorAll('.premium-cycle-arrows path').length < 4) errors.push('premium-cycle requires directional arc paths');
              }
              if (document.querySelector('.premium-transformation')) {
                if (document.querySelectorAll('.premium-zone').length !== 3) errors.push('premium-transformation requires exactly 3 zones');
                if (text('.zone-insight').length !== 3) errors.push('premium-transformation requires one insight sentence per zone');
                if (!document.querySelector('.conversion-artifact')) errors.push('premium-transformation requires a conversion artifact/package band');
                if (text('.artifact-item-row span').length < 2) errors.push('premium-transformation artifact band requires at least 2 item chips');
              }
              if (document.querySelector('.premium-process-flow')) {
                if (document.querySelectorAll('.process-stage').length !== 4) errors.push('premium-process-flow requires exactly 4 process stages');
                if (document.querySelectorAll('.process-arrow').length !== 3) errors.push('premium-process-flow requires 3 arrows between stages');
                if (!document.querySelector('.process-stream')) errors.push('premium-process-flow requires a stream output band');
                if (text('.stream-lines span').length < 2) errors.push('premium-process-flow stream band requires at least 2 streaming lines');
                if (document.querySelectorAll('.process-checkpoint').length < 2) errors.push('premium-process-flow requires checkpoint cards');
              }
              return errors;
            }"""
        )
        errors.extend(f"{path.name}: {error}" for error in layout_errors)

        browser.close()
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="QA rendered PicTalk HTML files")
    parser.add_argument("html", nargs="+", type=Path, help="Rendered HTML file(s)")
    args = parser.parse_args()

    errors: list[str] = []
    for path in args.html:
        if not path.exists():
            errors.append(f"File not found: {path}")
            continue
        errors.extend(qa_html(path))

    if errors:
        print("PicTalk visual QA failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PicTalk visual QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
