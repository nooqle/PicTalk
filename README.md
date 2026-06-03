# PicTalk

> Turn long-form content into presentation-ready infographics that explain the logic at a glance.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Codex Skill](https://img.shields.io/badge/Codex-Skill-0757D8)](./pictalk/SKILL.md)
[![Storyboard Validator](https://img.shields.io/badge/Storyboard-Validated-128348)](./pictalk/scripts/validate_storyboard.py)

PicTalk is a Codex skill for transforming articles, reports, transcripts, meeting notes, and strategy documents into clear visual explanations. It is built for text-heavy Chinese/English material where the final image must preserve exact wording, numbers, acronyms, and logic.

It does not ask an image model to draw final text. Instead, it creates a source-grounded storyboard, chooses a diagram pattern, and renders final typography through deterministic text layers.

## Why PicTalk

Most "article to image" workflows fail in two places: they summarize before understanding the source, and they let image models invent or corrupt text. PicTalk fixes that with a stricter loop:

```text
Read source -> map logic -> choose diagram pattern -> build storyboard -> render exact text -> validate
```

Use it when you want:

- one image that can explain a complex idea in a meeting;
- a small set of executive-ready visual cards;
- Chinese/English infographics with accurate text;
- diagrams that use timelines, arrows, matrices, funnels, layers, loops, or swimlanes;
- custom palettes without losing semantic color roles.

## Features

- **Source-first logic extraction**: identify thesis, claims, evidence, entities, relationships, and uncertain points before designing.
- **Diagram pattern library**: choose from transformation, timeline, arrow flow, layer stack, matrix, responsibility map, cycle, funnel, pyramid, radial map, swimlane, and hybrid layouts.
- **No accidental branding**: PicTalk is the workflow name and should not appear in final images unless explicitly requested.
- **Text accuracy by design**: render Chinese, English, numbers, dates, acronyms, and punctuation with real text layers.
- **Custom palette mapping**: map user colors into semantic roles such as primary, success, warning, explore, neutral, background, and conclusion band.
- **Storyboard validation**: validate card count, diagram pattern, visible marks, text ledger, and branding rules before rendering.

## Quick Start

Copy the `pictalk/` folder into your Codex skills directory, or keep it inside a workspace and invoke it explicitly:

```text
Use $pictalk to turn this article into a concise set of presentation-ready infographics with varied diagram forms.
```

For a typical run, provide source content and optional preferences:

```text
Use $pictalk on this PDF.
Output 3-5 Chinese infographics.
Use a calm blue/green/orange palette.
Do not put the workflow name or any watermark in the images.
```

## Workflow

1. **Ingest the source**  
   Read the article, PDF, transcript, notes, or pasted material.

2. **Extract the argument**  
   Capture the main thesis, supporting claims, causal chain, phases, actors, metrics, tensions, and conclusion.

3. **Choose image count**  
   Use one image for a single central idea, 2-3 for major branches, and 4-7 for dense material with multiple frameworks or workflows.

4. **Select diagram patterns**  
   Avoid defaulting to card grids. Use visible structures such as arrows, timelines, matrices, funnels, loops, ladders, swimlanes, or maps.

5. **Draft the storyboard**  
   Record exact visible text, layout type, primary pattern, evidence, palette roles, and the text ledger.

6. **Render deterministically**  
   Use HTML/CSS, SVG, PPTX, or another renderer with real text layers.

7. **Validate before delivery**  
   Check text accuracy, visual pattern diversity, source grounding, and absence of unintended visible branding.

## Visual Patterns

PicTalk includes a reusable pattern library:

| Pattern | Best for |
| --- | --- |
| Transformation | before/after, old/new model, problem/solution |
| Timeline | agendas, versions, incidents, phases |
| Arrow flow | processes, value chains, handoffs |
| Layer stack | maturity, hierarchy, capability levels |
| Matrix | categories crossed with evidence, owners, decisions, or impact |
| Responsibility map | DRIs, workgroups, interfaces, shared metrics |
| Cycle / flywheel | feedback loops, evaluation, continuous improvement |
| Funnel | filtering signals into cases, decisions, or actions |
| Pyramid | priority, foundations, strategic ladders |
| Radial map | central thesis with surrounding drivers |
| Swimlane | cross-team workflows and handoffs |

See [pattern-library.md](./pictalk/references/pattern-library.md) for selection rules and anti-patterns.

## Storyboard Format

Every output starts with a storyboard. A minimal card entry looks like this:

```json
{
  "id": "card-01",
  "title": "Exact rendered title",
  "layout_type": "timeline",
  "primary_pattern": "timeline",
  "composition": {
    "dominant_structure": "Vertical timeline with six milestone ticks.",
    "not_card_grid": true,
    "visible_marks": ["timeline axis", "milestone ticks", "handoff arrows"]
  },
  "text_ledger": [
    "Exact rendered title"
  ]
}
```

Validate a storyboard with:

```bash
python3 pictalk/scripts/validate_storyboard.py pictalk/assets/storyboard-template.json
```

## Project Structure

```text
pictalk/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── storyboard-template.json
├── references/
│   ├── pattern-library.md
│   ├── storyboard-schema.md
│   ├── style-guide.md
│   └── text-accuracy.md
└── scripts/
    └── validate_storyboard.py
```

## Design Principles

- Source evidence comes before visual polish.
- The image should make the logic visible before the reader finishes the text.
- Cards are containers, not the default composition.
- Every visible string should come from the storyboard text ledger.
- Final images should not contain generated pseudo-text.
- If the source is ambiguous, show the ambiguity instead of inventing certainty.

## Documentation

- [Skill workflow](./pictalk/SKILL.md)
- [Pattern library](./pictalk/references/pattern-library.md)
- [Style guide](./pictalk/references/style-guide.md)
- [Storyboard schema](./pictalk/references/storyboard-schema.md)
- [Text accuracy rules](./pictalk/references/text-accuracy.md)

## Contributing

Contributions are welcome. Useful improvements include:

- new diagram patterns;
- renderer templates for HTML/SVG/PPTX;
- stronger storyboard validation;
- palette presets;
- multilingual text QA workflows;
- examples that use public, non-sensitive source material.

Before opening a pull request, run:

```bash
python3 pictalk/scripts/validate_storyboard.py pictalk/assets/storyboard-template.json
```

## License

MIT. See [LICENSE](./LICENSE).
