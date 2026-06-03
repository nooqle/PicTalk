---
name: pictalk
description: Create PicTalk-style presentation-ready infographics from articles, reports, transcripts, notes, or other long-form content. Use when the user wants "one image that explains it", visual logic summaries, Chinese/English text-heavy infographic slides, article-to-image storytelling, custom palette information graphics, or a repeatable workflow that reads content, extracts the argument structure, chooses varied diagram forms such as timelines, layer maps, arrows, loops, matrices, funnels, and responsibility maps, decides the number of images, and renders accurate human-language text into images.
---

# PicTalk

Turn source material into a small set of clean, talk-ready infographics that explain the core logic at a glance.

PicTalk is the workflow name, not a visible watermark. Do not place `PicTalk`, skill names, internal file names, or process labels inside final images unless the user explicitly requests branding.

The outputs are text-accurate information graphics, not decorative AI posters. Use deterministic text rendering for all Chinese, English, numbers, labels, and formulas. Image generation may support backgrounds, icons, or decorative assets, but never rely on raster-generated text as the final text layer.

## Quick Start

1. Ingest the source: article, URL, PDF, transcript, notes, or pasted text.
2. Extract the argument: main thesis, supporting claims, causal chain, phases, actors, metrics, tensions, and conclusion.
3. Choose the card count:
   - `1 card`: one central idea, comparison, or transformation.
   - `2-3 cards`: one thesis with two or three major logic branches.
   - `4-7 cards`: a dense article with multiple frameworks, phases, roles, or workflows.
   - More than `7 cards`: ask whether to split into chapters unless the user explicitly wants a long deck.
4. Select a visual pattern per image. Avoid defaulting to card grids; cards are containers, not the composition. Use timelines, layer diagrams, arrow flows, matrices, loops, funnels, maps, pyramids, or mixed diagrams where the logic calls for them.
5. Draft a storyboard JSON before rendering. Include exact text strings, primary visual pattern, layout type, visual hierarchy, icon ideas, palette roles, and the evidence each image is based on.
6. Render with editable text layers using HTML/SVG, slide tooling, design software, or another deterministic renderer.
7. Verify text accuracy, visual diversity, and absence of unintended visible branding before delivering PNG/PDF/SVG/PPTX outputs.

For visual grammar, read [references/style-guide.md](references/style-guide.md). For diagram selection, read [references/pattern-library.md](references/pattern-library.md). For storyboard structure, read [references/storyboard-schema.md](references/storyboard-schema.md). For text accuracy rules, read [references/text-accuracy.md](references/text-accuracy.md).

## Workflow

### 1. Read For Logic

Extract meaning before designing. Produce a compact logic map:

- `thesis`: the one sentence the image set must make obvious.
- `before_after`: old model, new model, and what changed.
- `entities`: people, roles, teams, systems, concepts, products, data sources.
- `relationships`: cause, dependency, sequence, feedback loop, ownership, conflict, hierarchy.
- `evidence`: source sentences or sections supporting each claim.
- `terms`: exact Chinese, English, numbers, acronyms, and named concepts that must not be paraphrased.

If the source is unclear, mark uncertainty in the storyboard rather than inventing a clean-looking but unsupported logic.

### 2. Pick The Visual Pattern

Match logic to a repeatable visual pattern. Load [references/pattern-library.md](references/pattern-library.md) for the full catalog.

- `transformation`: past -> present, old model -> new model, problem -> solution.
- `timeline`: time boxes, version path, meeting agenda, history, rollout, or incident sequence.
- `comparison`: two or three columns showing roles, responsibilities, metrics, or tradeoffs.
- `layer-stack`: levels, maturity stages, audience tiers, or capability layers.
- `cycle`: operating loop, flywheel, feedback mechanism, or iterative process.
- `arrow-flow`: ordered workflow with arrows, checkpoints, handoffs, and decisions.
- `matrix`: categories crossed with evidence, owners, impact, or decision directions.
- `map`: roles, owners, responsibilities, interfaces, and shared goals.
- `pyramid`: hierarchy, priority, maturity, dependency, or strategic ladder.
- `funnel`: filtering from broad evidence to selected cases, decisions, or actions.
- `radial`: central thesis with surrounding drivers, consequences, or outputs.
- `principles`: distilled rules, conclusions, or decision criteria.
- `hybrid`: dense executive summary combining two forms; use sparingly.

Prefer one dominant visual metaphor per image. If an image needs three unrelated metaphors, split it.

Visual diversity rule: for `3+` images, use at least `3` distinct primary patterns. Do not produce a sequence where every image is a card grid, even when each grid looks clean.

### 3. Decide Card Count

Use image count as an editorial decision:

- Start with one anchor image that states the thesis.
- Add one image per major logic branch only when the branch needs its own visual structure.
- Merge images when they repeat the same visual form and only change wording.
- End with a conclusion image or bottom conclusion band when the user needs presentation-ready takeaways.

Every card should answer: "What can the audience now explain in 20 seconds?"

### 4. Design The Card

Use the house style:

- white or very pale background;
- dark navy title, large and centered;
- restrained primary blue with green, orange, and purple semantic accents;
- rounded rectangular modules with thin borders and soft shadows;
- icon-first section anchors;
- numbered circles for steps and layers;
- arrows, dotted connectors, and bottom conclusion bands;
- dense but breathable spacing, suitable for slides and internal strategy documents.

Respect custom palettes by mapping user colors into semantic roles: `primary`, `accent_success`, `accent_warning`, `accent_explore`, `neutral`, `background`, and `conclusion_band`. Keep contrast high.

Composition gate before rendering:

- Name the primary pattern for each image.
- Confirm the pattern matches the source logic.
- Use cards only as local containers inside a larger diagram.
- Include visible structural marks where appropriate: arrows, axes, ladders, timelines, swimlanes, loops, brackets, connectors, badges, scales, or funnels.
- Remove any visible `PicTalk` label, watermark, skill name, internal source path, or renderer label.

### 5. Render Text Deterministically

Do not ask an image model to draw final text. Acceptable renderers include:

- HTML/CSS captured to PNG/PDF;
- SVG with real `<text>` elements;
- PPTX/Keynote/Google Slides-style shapes and text boxes;
- Canvas only if text is drawn from exact strings and source artifacts remain editable or auditable.

Use icon libraries, simple SVG icons, or generated icon assets without embedded text. If image generation is used, render blank visual assets first, then overlay text deterministically.

### 6. Validate And Deliver

Before final delivery:

- Run `scripts/validate_storyboard.py <storyboard.json>` when a storyboard JSON exists.
- Compare every rendered text string against the storyboard text ledger.
- Check that Chinese punctuation, English capitalization, acronyms, percentages, dates, names, and numbers are exact.
- Confirm the card count matches the source logic and user brief.
- Confirm visual patterns are varied and not only card grids.
- Confirm final images do not contain `PicTalk` unless explicitly requested by the user.
- Export the final images plus the storyboard/source-notes file when useful.

## Output Contract

For a complete PicTalk run, deliver:

- final image files in the requested aspect ratio;
- a short explanation of what each image covers and which visual pattern it uses;
- the storyboard JSON or markdown outline when the user may iterate;
- notes on any source ambiguity or unsupported claims;
- text validation status.

If the user asks only for prompts, provide a storyboard and renderer-ready prompts, but still warn that final text should be overlaid deterministically.
