#!/usr/bin/env python3
"""Validate a PicTalk storyboard JSON file before rendering."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


GENERIC_RENDER_LAYOUTS = {
    "transformation",
    "comparison",
    "cycle",
    "arrow-flow",
    "timeline",
    "matrix",
    "layer-stack",
}

PREMIUM_RENDER_LAYOUTS = {
    "premium-cycle-system",
    "premium-hierarchy-diffusion",
    "premium-process-flow",
    "premium-transformation-logic",
}

SUPPORTED_RENDER_LAYOUTS = GENERIC_RENDER_LAYOUTS | PREMIUM_RENDER_LAYOUTS

LAYOUT_SECTION_LIMITS = {
    "transformation": (2, 3),
    "comparison": (2, 3),
    "cycle": (4, 6),
    "arrow-flow": (3, 6),
    "timeline": (3, 6),
    "layer-stack": (3, 5),
}

ALLOWED_TONES = {"blue", "green", "orange", "purple", "gray"}
DEFAULT_HIERARCHY_LABELS = {
    "typical_behavior": "典型行为",
    "core_blocker": "核心卡点",
    "matched_audience": "匹配人群",
}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def collect_strings(value: Any) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str) and value.strip():
        strings.append(value.strip())
    elif isinstance(value, list):
        for item in value:
            strings.extend(collect_strings(item))
    elif isinstance(value, dict):
        for item in value.values():
            strings.extend(collect_strings(item))
    return strings


def common_rendered_strings(card: dict[str, Any]) -> list[str]:
    keys = [
        "title",
        "subtitle",
        "center_text",
        "outputs_title",
        "conclusion",
        "footer_note",
        "side_note_title",
        "side_note",
    ]
    strings: list[str] = []
    for key in keys:
        value = card.get(key)
        if isinstance(value, str) and value.strip():
            strings.append(value.strip())

    for item in card.get("top_flow") or []:
        strings.extend(collect_strings({"label": item.get("label")}))

    for metric in card.get("metrics") or []:
        strings.extend(collect_strings({
            "label": metric.get("label"),
            "value": metric.get("value"),
        }))

    return strings


def generic_rendered_strings(card: dict[str, Any]) -> list[str]:
    strings: list[str] = []

    for section in card.get("sections") or []:
        strings.extend(collect_strings({
            "heading": section.get("heading"),
            "body": section.get("body"),
            "footer": section.get("footer"),
            "badge": section.get("badge"),
        }))

    for section in card.get("side_sections") or []:
        strings.extend(collect_strings({
            "heading": section.get("heading"),
            "body": section.get("body"),
        }))

    matrix = card.get("matrix")
    if isinstance(matrix, dict):
        strings.extend(collect_strings(matrix.get("columns")))
        for row in matrix.get("rows") or []:
            strings.extend(collect_strings({
                "label": row.get("label") if isinstance(row, dict) else None,
                "values": row.get("values") if isinstance(row, dict) else None,
            }))

    return strings


def premium_rendered_strings(card: dict[str, Any]) -> list[str]:
    layout_type = card.get("layout_type")
    strings: list[str] = []

    if layout_type == "premium-hierarchy-diffusion":
        labels = DEFAULT_HIERARCHY_LABELS.copy()
        labels.update(card.get("field_labels") or {})
        strings.extend(labels.values())
        strings.append(card.get("essence_label", "需求本质"))
        strings.append(card.get("tiers_title", "用户层级"))
        strings.append(card.get("mechanisms_title", "扩散机制"))
        strings.append(card.get("summary_title", "结构判断"))
        strings.extend(collect_strings({"axis": (card.get("axis") or {}).get("label")}))
        tier_callout = card.get("tier_callout")
        if isinstance(tier_callout, dict):
            strings.extend(collect_strings({"text": tier_callout.get("text")}))

        for layer in card.get("layers") or []:
            strings.extend(collect_strings({
                "no": layer.get("no"),
                "title": layer.get("title"),
                "type": layer.get("type"),
                "typical_behavior": layer.get("typical_behavior"),
                "core_blocker": layer.get("core_blocker"),
                "matched_audience": layer.get("matched_audience"),
                "essence": layer.get("essence"),
            }))

        for tier in card.get("user_tiers") or []:
            strings.extend(collect_strings({
                "label": tier.get("label"),
                "headline": tier.get("headline"),
                "body": tier.get("body"),
            }))

        for mechanism in card.get("mechanisms") or []:
            strings.extend(collect_strings({
                "no": mechanism.get("no"),
                "title": mechanism.get("title"),
                "body": mechanism.get("body"),
            }))

        for summary in card.get("summary_cards") or []:
            strings.extend(collect_strings({
                "title": summary.get("title"),
                "body": summary.get("body"),
            }))

    elif layout_type == "premium-cycle-system":
        center = card.get("center") or {}
        strings.extend(collect_strings({
            "main": center.get("main"),
            "lines": center.get("lines"),
        }))
        strings.append(card.get("outputs_title", "关键产出"))
        for phase in card.get("cycle_phases") or []:
            strings.extend(collect_strings({"label": phase.get("label") if isinstance(phase, dict) else None}))

        for node in card.get("loop_nodes") or []:
            strings.extend(collect_strings({
                "no": node.get("no"),
                "title": node.get("title"),
                "subtitle": node.get("subtitle"),
            }))

        for output in card.get("outputs") or []:
            strings.extend(collect_strings({
                "title": output.get("title"),
                "body": output.get("body"),
            }))

    elif layout_type == "premium-transformation-logic":
        strings.append("核心转化判断")
        strings.extend(collect_strings({"thesis": card.get("thesis")}))
        for zone in card.get("zones") or []:
            strings.extend(collect_strings({
                "label": zone.get("label"),
                "title": zone.get("title"),
                "insight": zone.get("insight"),
                "bullets": zone.get("bullets"),
                "essence": zone.get("essence"),
            }))
        for relation in card.get("relations") or []:
            strings.extend(collect_strings({"label": relation.get("label")}))
        artifact = card.get("conversion_artifact")
        if isinstance(artifact, dict):
            strings.extend(collect_strings({
                "title": artifact.get("title"),
                "subtitle": artifact.get("subtitle"),
                "items": artifact.get("items"),
            }))
    elif layout_type == "premium-process-flow":
        for stage in card.get("stages") or []:
            strings.extend(collect_strings({
                "no": stage.get("no"),
                "title": stage.get("title"),
                "subtitle": stage.get("subtitle"),
                "body": stage.get("body"),
            }))
        stream = card.get("stream")
        if isinstance(stream, dict):
            strings.extend(collect_strings({
                "title": stream.get("title"),
                "subtitle": stream.get("subtitle"),
                "items": stream.get("items"),
            }))
        for checkpoint in card.get("checkpoints") or []:
            strings.extend(collect_strings({
                "title": checkpoint.get("title"),
                "body": checkpoint.get("body"),
            }))

    return strings


def rendered_strings(card: dict[str, Any]) -> list[str]:
    strings = common_rendered_strings(card)
    if card.get("layout_type") in PREMIUM_RENDER_LAYOUTS:
        strings.extend(premium_rendered_strings(card))
    else:
        strings.extend(generic_rendered_strings(card))

    seen = set()
    result = []
    for string in strings:
        if string and string not in seen:
            result.append(string)
            seen.add(string)
    return result


def validate_common_card(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    for key in ["id", "title", "layout_type", "primary_pattern", "thesis"]:
        require(is_nonempty_string(card.get(key)), f"{prefix}.{key} is required", errors)

    layout_type = card.get("layout_type")
    require(
        layout_type in SUPPORTED_RENDER_LAYOUTS,
        f"{prefix}.layout_type must be one of renderer-supported layouts {sorted(SUPPORTED_RENDER_LAYOUTS)}",
        errors,
    )

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


def validate_generic_card(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    layout_type = card.get("layout_type")
    sections = card.get("sections")
    require(isinstance(sections, list) and bool(sections), f"{prefix}.sections must be a non-empty list", errors)
    if isinstance(sections, list):
        limit = LAYOUT_SECTION_LIMITS.get(str(layout_type))
        if limit:
            lo, hi = limit
            require(lo <= len(sections) <= hi, f"{prefix}.sections count must be {lo}-{hi} for layout_type={layout_type}", errors)
        for section_index, section in enumerate(sections, start=1):
            section_prefix = f"{prefix}.sections[{section_index}]"
            require(isinstance(section, dict), f"{section_prefix} must be an object", errors)
            if not isinstance(section, dict):
                continue
            require(is_nonempty_string(section.get("id")), f"{section_prefix}.id is required", errors)
            require(is_nonempty_string(section.get("heading")), f"{section_prefix}.heading is required", errors)
            require(isinstance(section.get("body"), list), f"{section_prefix}.body must be a list", errors)

    if layout_type == "matrix":
        matrix = card.get("matrix")
        require(isinstance(matrix, dict), f"{prefix}.matrix is required for layout_type=matrix", errors)
        if isinstance(matrix, dict):
            columns = matrix.get("columns")
            rows = matrix.get("rows")
            require(isinstance(columns, list) and 2 <= len(columns) <= 4, f"{prefix}.matrix.columns must contain 2-4 columns", errors)
            require(isinstance(rows, list) and 2 <= len(rows) <= 5, f"{prefix}.matrix.rows must contain 2-5 rows", errors)
            if isinstance(columns, list) and isinstance(rows, list):
                for row_index, row in enumerate(rows, start=1):
                    values = row.get("values") if isinstance(row, dict) else None
                    require(isinstance(row, dict), f"{prefix}.matrix.rows[{row_index}] must be an object", errors)
                    require(isinstance(values, list) and len(values) == len(columns), f"{prefix}.matrix.rows[{row_index}].values must match columns length", errors)


def require_tone(value: Any, path: str, errors: list[str]) -> None:
    require(value in ALLOWED_TONES, f"{path} must be one of {sorted(ALLOWED_TONES)}", errors)


def validate_premium_canvas(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    canvas = card.get("canvas")
    if isinstance(canvas, dict) and not card.get("allow_custom_canvas"):
        require(canvas.get("width") == 1086 and canvas.get("height") == 1448, f"{prefix}.canvas must be 1086x1448 for premium layouts", errors)


def validate_hierarchy(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    validate_premium_canvas(card, prefix, errors)
    require(card.get("layout_family") == "premium", f"{prefix}.layout_family must be premium", errors)
    require(card.get("quality_target") in {"presentation", "reference-grade"}, f"{prefix}.quality_target must be presentation or reference-grade", errors)

    axis = card.get("axis")
    require(isinstance(axis, dict), f"{prefix}.axis must be an object", errors)
    if isinstance(axis, dict):
        require(is_nonempty_string(axis.get("label")), f"{prefix}.axis.label is required", errors)
        require(axis.get("direction", "up") == "up", f"{prefix}.axis.direction must be up", errors)

    layers = card.get("layers")
    require(isinstance(layers, list) and len(layers) == 4, f"{prefix}.layers must contain exactly 4 layers", errors)
    layer_keys: set[str] = set()
    if isinstance(layers, list):
        for i, layer in enumerate(layers, start=1):
            layer_prefix = f"{prefix}.layers[{i}]"
            require(isinstance(layer, dict), f"{layer_prefix} must be an object", errors)
            if not isinstance(layer, dict):
                continue
            for key in ["no", "title", "type", "icon", "tone", "typical_behavior", "core_blocker", "matched_audience", "essence"]:
                require(is_nonempty_string(layer.get(key)), f"{layer_prefix}.{key} is required", errors)
            require_tone(layer.get("tone"), f"{layer_prefix}.tone", errors)
            if is_nonempty_string(layer.get("essence")):
                require(len(layer["essence"]) <= 24, f"{layer_prefix}.essence should be 24 characters or fewer", errors)
            for key in [layer.get("id"), layer.get("no"), layer.get("title")]:
                if key is not None:
                    layer_keys.add(str(key))

    tiers = card.get("user_tiers")
    require(isinstance(tiers, list) and len(tiers) == 3, f"{prefix}.user_tiers must contain exactly 3 tiers", errors)
    tier_keys: set[str] = set()
    if isinstance(tiers, list):
        for i, tier in enumerate(tiers, start=1):
            tier_prefix = f"{prefix}.user_tiers[{i}]"
            require(isinstance(tier, dict), f"{tier_prefix} must be an object", errors)
            if not isinstance(tier, dict):
                continue
            for key in ["id", "label", "headline", "tone"]:
                require(is_nonempty_string(tier.get(key)), f"{tier_prefix}.{key} is required", errors)
            require_tone(tier.get("tone"), f"{tier_prefix}.tone", errors)
            require(isinstance(tier.get("body"), list) and bool(tier.get("body")), f"{tier_prefix}.body must be a non-empty list", errors)
            label = str(tier.get("label", ""))
            for key in [tier.get("id"), label, label.split()[0] if label else None]:
                if key is not None:
                    tier_keys.add(str(key))

    tier_callout = card.get("tier_callout")
    if tier_callout is not None:
        require(isinstance(tier_callout, dict), f"{prefix}.tier_callout must be an object when provided", errors)
        if isinstance(tier_callout, dict):
            require(is_nonempty_string(tier_callout.get("text")), f"{prefix}.tier_callout.text is required", errors)
            require_tone(tier_callout.get("tone", "orange"), f"{prefix}.tier_callout.tone", errors)

    connectors = card.get("connectors")
    require(isinstance(connectors, list) and len(connectors) >= 3, f"{prefix}.connectors must contain at least 3 layer-to-tier relations", errors)
    if isinstance(connectors, list):
        for i, connector in enumerate(connectors, start=1):
            connector_prefix = f"{prefix}.connectors[{i}]"
            require(isinstance(connector, dict), f"{connector_prefix} must be an object", errors)
            if not isinstance(connector, dict):
                continue
            require(str(connector.get("from_layer")) in layer_keys, f"{connector_prefix}.from_layer must reference a layer no/id/title", errors)
            require(str(connector.get("to_tier")) in tier_keys, f"{connector_prefix}.to_tier must reference a tier id/label", errors)
            require_tone(connector.get("tone", "blue"), f"{connector_prefix}.tone", errors)

    mechanisms = card.get("mechanisms")
    require(isinstance(mechanisms, list) and len(mechanisms) == 3, f"{prefix}.mechanisms must contain exactly 3 mechanisms", errors)
    if isinstance(mechanisms, list):
        for i, mechanism in enumerate(mechanisms, start=1):
            mechanism_prefix = f"{prefix}.mechanisms[{i}]"
            require(isinstance(mechanism, dict), f"{mechanism_prefix} must be an object", errors)
            if not isinstance(mechanism, dict):
                continue
            for key in ["no", "title", "body", "tone"]:
                require(is_nonempty_string(mechanism.get(key)), f"{mechanism_prefix}.{key} is required", errors)
            require_tone(mechanism.get("tone"), f"{mechanism_prefix}.tone", errors)

    summaries = card.get("summary_cards")
    require(isinstance(summaries, list) and 2 <= len(summaries) <= 3, f"{prefix}.summary_cards must contain 2-3 cards", errors)
    if isinstance(summaries, list):
        for i, summary in enumerate(summaries, start=1):
            summary_prefix = f"{prefix}.summary_cards[{i}]"
            require(isinstance(summary, dict), f"{summary_prefix} must be an object", errors)
            if isinstance(summary, dict):
                require(is_nonempty_string(summary.get("title")), f"{summary_prefix}.title is required", errors)
                require(is_nonempty_string(summary.get("body")), f"{summary_prefix}.body is required", errors)

    require(is_nonempty_string(card.get("conclusion")), f"{prefix}.conclusion is required", errors)


def validate_cycle(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    validate_premium_canvas(card, prefix, errors)
    require(card.get("layout_family") == "premium", f"{prefix}.layout_family must be premium", errors)
    require(card.get("quality_target") in {"presentation", "reference-grade"}, f"{prefix}.quality_target must be presentation or reference-grade", errors)

    center = card.get("center")
    require(isinstance(center, dict), f"{prefix}.center must be an object", errors)
    if isinstance(center, dict):
        require(is_nonempty_string(center.get("main")), f"{prefix}.center.main is required", errors)
        require(isinstance(center.get("lines"), list) and bool(center.get("lines")), f"{prefix}.center.lines must be a non-empty list", errors)
        if is_nonempty_string(center.get("main")):
            require(len(center["main"]) <= 24, f"{prefix}.center.main should be 24 characters or fewer", errors)

    top_flow = card.get("top_flow")
    require(isinstance(top_flow, list) and 3 <= len(top_flow) <= 5, f"{prefix}.top_flow must contain 3-5 items", errors)

    cycle_phases = card.get("cycle_phases")
    if cycle_phases is not None:
        require(isinstance(cycle_phases, list) and 3 <= len(cycle_phases) <= 5, f"{prefix}.cycle_phases must contain 3-5 phase labels when provided", errors)
        if isinstance(cycle_phases, list):
            for i, phase in enumerate(cycle_phases, start=1):
                phase_prefix = f"{prefix}.cycle_phases[{i}]"
                require(isinstance(phase, dict), f"{phase_prefix} must be an object", errors)
                if isinstance(phase, dict):
                    require(is_nonempty_string(phase.get("label")), f"{phase_prefix}.label is required", errors)
                    if phase.get("tone") is not None:
                        require_tone(phase.get("tone"), f"{phase_prefix}.tone", errors)

    nodes = card.get("loop_nodes")
    require(isinstance(nodes, list) and 5 <= len(nodes) <= 6, f"{prefix}.loop_nodes must contain 5-6 nodes", errors)
    if isinstance(nodes, list):
        for i, node in enumerate(nodes, start=1):
            node_prefix = f"{prefix}.loop_nodes[{i}]"
            require(isinstance(node, dict), f"{node_prefix} must be an object", errors)
            if not isinstance(node, dict):
                continue
            for key in ["no", "title", "subtitle", "icon", "tone"]:
                require(is_nonempty_string(node.get(key)), f"{node_prefix}.{key} is required", errors)
            require_tone(node.get("tone"), f"{node_prefix}.tone", errors)

    outputs = card.get("outputs")
    require(isinstance(outputs, list) and 3 <= len(outputs) <= 5, f"{prefix}.outputs must contain 3-5 outputs", errors)
    if isinstance(outputs, list):
        for i, output in enumerate(outputs, start=1):
            output_prefix = f"{prefix}.outputs[{i}]"
            require(isinstance(output, dict), f"{output_prefix} must be an object", errors)
            if not isinstance(output, dict):
                continue
            for key in ["title", "body", "icon", "tone"]:
                require(is_nonempty_string(output.get(key)), f"{output_prefix}.{key} is required", errors)
            require_tone(output.get("tone"), f"{output_prefix}.tone", errors)

    require(is_nonempty_string(card.get("conclusion")), f"{prefix}.conclusion is required", errors)


def validate_transformation(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    validate_premium_canvas(card, prefix, errors)
    require(card.get("layout_family") == "premium", f"{prefix}.layout_family must be premium", errors)
    require(card.get("quality_target") in {"presentation", "reference-grade"}, f"{prefix}.quality_target must be presentation or reference-grade", errors)

    zones = card.get("zones")
    require(isinstance(zones, list) and len(zones) == 3, f"{prefix}.zones must contain exactly 3 zones", errors)
    zone_ids: set[str] = set()
    if isinstance(zones, list):
        for i, zone in enumerate(zones, start=1):
            zone_prefix = f"{prefix}.zones[{i}]"
            require(isinstance(zone, dict), f"{zone_prefix} must be an object", errors)
            if not isinstance(zone, dict):
                continue
            for key in ["id", "label", "title", "icon", "essence", "tone"]:
                require(is_nonempty_string(zone.get(key)), f"{zone_prefix}.{key} is required", errors)
            require_tone(zone.get("tone"), f"{zone_prefix}.tone", errors)
            require(isinstance(zone.get("bullets"), list) and 2 <= len(zone.get("bullets")) <= 4, f"{zone_prefix}.bullets must contain 2-4 bullets", errors)
            if card.get("quality_target") == "reference-grade":
                require(is_nonempty_string(zone.get("insight")), f"{zone_prefix}.insight is required for reference-grade transformation cards", errors)
            if is_nonempty_string(zone.get("id")):
                zone_ids.add(str(zone.get("id")))

    if isinstance(zones, list) and len(zones) >= 2 and isinstance(zones[1], dict):
        middle = zones[1]
        require(middle.get("tone") == "blue" or middle.get("emphasis") is True, f"{prefix}.zones[2] must be emphasized or blue", errors)

    relations = card.get("relations")
    require(isinstance(relations, list) and len(relations) == 2, f"{prefix}.relations must contain exactly 2 relations", errors)
    if isinstance(relations, list):
        for i, relation in enumerate(relations, start=1):
            relation_prefix = f"{prefix}.relations[{i}]"
            require(isinstance(relation, dict), f"{relation_prefix} must be an object", errors)
            if not isinstance(relation, dict):
                continue
            for key in ["from", "to", "label", "tone"]:
                require(is_nonempty_string(relation.get(key)), f"{relation_prefix}.{key} is required", errors)
            require(str(relation.get("from")) in zone_ids, f"{relation_prefix}.from must reference a zone id", errors)
            require(str(relation.get("to")) in zone_ids, f"{relation_prefix}.to must reference a zone id", errors)
            require_tone(relation.get("tone"), f"{relation_prefix}.tone", errors)

    metrics = card.get("metrics")
    require(isinstance(metrics, list) and 2 <= len(metrics) <= 4, f"{prefix}.metrics must contain 2-4 metric cards", errors)

    artifact = card.get("conversion_artifact")
    if card.get("quality_target") == "reference-grade":
        require(isinstance(artifact, dict), f"{prefix}.conversion_artifact is required for reference-grade transformation cards", errors)
    if artifact is not None:
        require(isinstance(artifact, dict), f"{prefix}.conversion_artifact must be an object when provided", errors)
        if isinstance(artifact, dict):
            require(is_nonempty_string(artifact.get("title")), f"{prefix}.conversion_artifact.title is required", errors)
            require(is_nonempty_string(artifact.get("subtitle")), f"{prefix}.conversion_artifact.subtitle is required", errors)
            require(isinstance(artifact.get("items"), list) and 2 <= len(artifact.get("items")) <= 5, f"{prefix}.conversion_artifact.items must contain 2-5 items", errors)
            if artifact.get("tone") is not None:
                require_tone(artifact.get("tone"), f"{prefix}.conversion_artifact.tone", errors)
    require(is_nonempty_string(card.get("conclusion")), f"{prefix}.conclusion is required", errors)


def validate_process_flow(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    canvas = card.get("canvas")
    if isinstance(canvas, dict) and not card.get("allow_custom_canvas"):
        require(canvas.get("width") == 1536 and canvas.get("height") == 1024, f"{prefix}.canvas must be 1536x1024 for premium-process-flow unless allow_custom_canvas is true", errors)

    require(card.get("layout_family") == "premium", f"{prefix}.layout_family must be premium", errors)
    require(card.get("quality_target") in {"presentation", "reference-grade"}, f"{prefix}.quality_target must be presentation or reference-grade", errors)

    stages = card.get("stages")
    require(isinstance(stages, list) and len(stages) == 4, f"{prefix}.stages must contain exactly 4 stages", errors)
    if isinstance(stages, list):
        for i, stage in enumerate(stages, start=1):
            stage_prefix = f"{prefix}.stages[{i}]"
            require(isinstance(stage, dict), f"{stage_prefix} must be an object", errors)
            if not isinstance(stage, dict):
                continue
            for key in ["no", "title", "subtitle", "icon", "tone"]:
                require(is_nonempty_string(stage.get(key)), f"{stage_prefix}.{key} is required", errors)
            require_tone(stage.get("tone"), f"{stage_prefix}.tone", errors)
            require(isinstance(stage.get("body"), list) and 1 <= len(stage.get("body")) <= 3, f"{stage_prefix}.body must contain 1-3 items", errors)

    stream = card.get("stream")
    require(isinstance(stream, dict), f"{prefix}.stream is required", errors)
    if isinstance(stream, dict):
        for key in ["title", "subtitle", "icon", "tone"]:
            require(is_nonempty_string(stream.get(key)), f"{prefix}.stream.{key} is required", errors)
        require_tone(stream.get("tone"), f"{prefix}.stream.tone", errors)
        require(isinstance(stream.get("items"), list) and 2 <= len(stream.get("items")) <= 5, f"{prefix}.stream.items must contain 2-5 items", errors)

    checkpoints = card.get("checkpoints")
    require(isinstance(checkpoints, list) and 2 <= len(checkpoints) <= 3, f"{prefix}.checkpoints must contain 2-3 checkpoint cards", errors)
    if isinstance(checkpoints, list):
        for i, checkpoint in enumerate(checkpoints, start=1):
            checkpoint_prefix = f"{prefix}.checkpoints[{i}]"
            require(isinstance(checkpoint, dict), f"{checkpoint_prefix} must be an object", errors)
            if isinstance(checkpoint, dict):
                for key in ["title", "body", "icon", "tone"]:
                    require(is_nonempty_string(checkpoint.get(key)), f"{checkpoint_prefix}.{key} is required", errors)
                require_tone(checkpoint.get("tone"), f"{checkpoint_prefix}.tone", errors)

    require(is_nonempty_string(card.get("conclusion")), f"{prefix}.conclusion is required", errors)


def validate_premium_card(card: dict[str, Any], prefix: str, errors: list[str]) -> None:
    layout_type = card.get("layout_type")
    if layout_type == "premium-hierarchy-diffusion":
        validate_hierarchy(card, prefix, errors)
    elif layout_type == "premium-cycle-system":
        validate_cycle(card, prefix, errors)
    elif layout_type == "premium-process-flow":
        validate_process_flow(card, prefix, errors)
    elif layout_type == "premium-transformation-logic":
        validate_transformation(card, prefix, errors)


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

    if len(cards) >= 3:
        distinct_layouts = {card.get("layout_type") for card in cards if isinstance(card, dict)}
        require(len(distinct_layouts) >= 3, "3+ cards must use at least 3 distinct layout_type values", errors)

    for index, card in enumerate(cards, start=1):
        prefix = f"cards[{index}]"
        require(isinstance(card, dict), f"{prefix} must be an object", errors)
        if not isinstance(card, dict):
            continue

        validate_common_card(card, prefix, errors)
        if card.get("layout_type") in PREMIUM_RENDER_LAYOUTS:
            validate_premium_card(card, prefix, errors)
        else:
            validate_generic_card(card, prefix, errors)

        text_ledger = card.get("text_ledger")
        require(isinstance(text_ledger, list) and bool(text_ledger), f"{prefix}.text_ledger must be a non-empty list", errors)
        ledger_set = set()
        if isinstance(text_ledger, list):
            for item_index, item in enumerate(text_ledger, start=1):
                require(is_nonempty_string(item), f"{prefix}.text_ledger[{item_index}] must be a non-empty string", errors)
                if isinstance(item, str):
                    ledger_set.add(item.strip())
                    if not allow_visible_brand:
                        require("pictalk" not in item.lower(), f"{prefix}.text_ledger[{item_index}] contains visible PicTalk branding", errors)

        for required_string in rendered_strings(card):
            if required_string and required_string not in ledger_set:
                errors.append(f"{prefix}.text_ledger missing visible string: {required_string}")

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
