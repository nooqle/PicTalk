#!/usr/bin/env python3
"""Validate a PicTalk storyboard JSON file."""

from __future__ import annotations

import json
import sys
from pathlib import Path


LAYOUT_TYPES = {
    "transformation",
    "timeline",
    "comparison",
    "layer-stack",
    "cycle",
    "arrow-flow",
    "matrix",
    "map",
    "pyramid",
    "funnel",
    "radial",
    "swimlane",
    "principles",
    "hybrid",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    require(isinstance(data, dict), "root must be a JSON object", errors)
    if not isinstance(data, dict):
        return errors

    project = data.get("project")
    require(isinstance(project, dict), "project must be an object", errors)
    if isinstance(project, dict):
        for key in ["title", "output_language", "aspect_ratio", "card_count_rationale"]:
            require(is_nonempty_string(project.get(key)), f"project.{key} is required", errors)
        allow_visible_brand = bool(project.get("allow_visible_pictalk_brand", False))
        title = project.get("title")
        if isinstance(title, str) and not allow_visible_brand:
            require("pictalk" not in title.lower(), "project.title contains visible PicTalk branding", errors)
    else:
        allow_visible_brand = False

    palette = data.get("palette")
    require(isinstance(palette, dict) and bool(palette), "palette must be a non-empty object", errors)

    source_notes = data.get("source_notes")
    require(isinstance(source_notes, list), "source_notes must be a list", errors)

    cards = data.get("cards")
    require(isinstance(cards, list) and bool(cards), "cards must be a non-empty list", errors)
    if not isinstance(cards, list):
        return errors

    for index, card in enumerate(cards, start=1):
        prefix = f"cards[{index}]"
        require(isinstance(card, dict), f"{prefix} must be an object", errors)
        if not isinstance(card, dict):
            continue

        for key in ["id", "title", "layout_type", "primary_pattern", "thesis"]:
            require(is_nonempty_string(card.get(key)), f"{prefix}.{key} is required", errors)

        layout_type = card.get("layout_type")
        require(layout_type in LAYOUT_TYPES, f"{prefix}.layout_type must be one of {sorted(LAYOUT_TYPES)}", errors)

        composition = card.get("composition")
        require(isinstance(composition, dict), f"{prefix}.composition must be an object", errors)
        if isinstance(composition, dict):
            require(is_nonempty_string(composition.get("dominant_structure")), f"{prefix}.composition.dominant_structure is required", errors)
            require(composition.get("not_card_grid") is True, f"{prefix}.composition.not_card_grid must be true", errors)
            visible_marks = composition.get("visible_marks")
            require(isinstance(visible_marks, list) and bool(visible_marks), f"{prefix}.composition.visible_marks must be a non-empty list", errors)

        canvas = card.get("canvas")
        require(isinstance(canvas, dict), f"{prefix}.canvas must be an object", errors)
        if isinstance(canvas, dict):
            require(isinstance(canvas.get("width"), int) and canvas["width"] > 0, f"{prefix}.canvas.width must be a positive integer", errors)
            require(isinstance(canvas.get("height"), int) and canvas["height"] > 0, f"{prefix}.canvas.height must be a positive integer", errors)

        sections = card.get("sections")
        require(isinstance(sections, list) and bool(sections), f"{prefix}.sections must be a non-empty list", errors)
        if isinstance(sections, list):
            for section_index, section in enumerate(sections, start=1):
                section_prefix = f"{prefix}.sections[{section_index}]"
                require(isinstance(section, dict), f"{section_prefix} must be an object", errors)
                if not isinstance(section, dict):
                    continue
                require(is_nonempty_string(section.get("id")), f"{section_prefix}.id is required", errors)
                require(is_nonempty_string(section.get("heading")), f"{section_prefix}.heading is required", errors)
                require(isinstance(section.get("body"), list), f"{section_prefix}.body must be a list", errors)

        text_ledger = card.get("text_ledger")
        require(isinstance(text_ledger, list) and bool(text_ledger), f"{prefix}.text_ledger must be a non-empty list", errors)
        if isinstance(text_ledger, list):
            for item_index, item in enumerate(text_ledger, start=1):
                require(is_nonempty_string(item), f"{prefix}.text_ledger[{item_index}] must be a non-empty string", errors)
                if isinstance(item, str) and not allow_visible_brand:
                    require("pictalk" not in item.lower(), f"{prefix}.text_ledger[{item_index}] contains visible PicTalk branding", errors)

        for key in ["title", "subtitle", "conclusion"]:
            value = card.get(key)
            if isinstance(value, str) and not allow_visible_brand:
                require("pictalk" not in value.lower(), f"{prefix}.{key} contains visible PicTalk branding", errors)

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_storyboard.py <storyboard.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    try:
        errors = validate(path)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        return 1

    if errors:
        print("PicTalk storyboard validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PicTalk storyboard validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
