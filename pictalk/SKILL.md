---
name: pictalk
description: Create PicTalk-style presentation-ready infographics from articles, reports, transcripts, notes, or other long-form content. Use when the user wants "one image that explains it", visual logic summaries, Chinese/English text-heavy infographic slides, article-to-image storytelling, custom palette information graphics, or a repeatable workflow that reads content, extracts the argument structure, chooses varied diagram forms such as timelines, layer maps, arrows, loops, matrices, funnels, and responsibility maps, decides the number of images, and renders accurate human-language text into images.
---

# PicTalk

Turn source material into a small set of clean, talk-ready infographics that explain the core logic at a glance.

PicTalk is the workflow name, not a visible watermark. Do not place `PicTalk`, skill names, internal file names, or process labels inside final images unless the user explicitly requests branding.

The outputs are text-accurate information graphics, not decorative AI posters. All visible text must originate from the storyboard `text_ledger` and should be rendered with deterministic HTML/SVG/PPTX text layers by default. Image generation may be used as an optional visual-polish path, but do not depend on raster-generated text for Chinese, numbers, formulas, labels, or final delivery when a deterministic renderer is available.

When the user asks for "one image that explains it", "有质感", "层级指示", "逻辑好的一张图", or a reference-grade article image, prefer a **premium locked layout** before any generic layout. Premium layouts use semantic slots such as layer behavior, blocker, audience, essence, relation, mechanism, output, and conclusion; do not reduce them to generic `sections`.

## Quick Start

1. Ingest the source: article, URL, PDF, transcript, notes, or pasted text.
2. Extract the argument: main thesis, supporting claims, causal chain, phases, actors, metrics, tensions, and conclusion.
3. Choose the card count:
   - `1 card`: one central idea, comparison, or transformation.
   - `2-3 cards`: one thesis with two or three major logic branches.
   - `4-7 cards`: a dense article with multiple frameworks, phases, roles, or workflows.
   - More than `7 cards`: ask whether to split into chapters unless the user explicitly wants a long deck.
4. Select a visual pattern per image. For reference-grade outputs, try premium layouts first: `premium-hierarchy-diffusion`, `premium-cycle-system`, `premium-transformation-logic`, or `premium-process-flow`. Use generic timelines, arrows, matrices, or layer stacks only when the premium layouts do not match the logic.
5. Draft a storyboard JSON before rendering. Include exact text strings, primary visual pattern, layout type, visual hierarchy, icon ideas, palette roles, and the evidence each image is based on.
6. Render images using the locked renderer first:
   - **Primary**: HTML/CSS rendering via `scripts/render_storyboard.py`, using one of the supported locked layouts.
   - **Optional polish**: if an image-capable model is available, construct prompts from [references/image-prompts.md](references/image-prompts.md), but keep final text deterministic unless the user explicitly accepts raster text risk.
7. Validate text accuracy, visual diversity, and absence of unintended visible branding before delivering PNG/PDF/SVG/PPTX outputs.

For visual grammar, read [references/style-guide.md](references/style-guide.md). For locked layout selection, read [references/layouts.md](references/layouts.md). For diagram selection, read [references/pattern-library.md](references/pattern-library.md). For storyboard structure, read [references/storyboard-schema.md](references/storyboard-schema.md). For text accuracy rules, read [references/text-accuracy.md](references/text-accuracy.md). For optional image prompt construction, read [references/image-prompts.md](references/image-prompts.md).

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

Match logic to a repeatable visual pattern, then bind that pattern to a renderer-supported locked layout. Load [references/layouts.md](references/layouts.md) before writing the storyboard.

- `premium-hierarchy-diffusion`: 4-level hierarchy, right-side tiers, layer-to-tier connectors, mechanism row, summary cards, and conclusion band.
- `premium-cycle-system`: top logic strip, central mechanism, 5-6 loop nodes, output row, and conclusion band.
- `premium-transformation-logic`: old state -> mechanism -> new state with labeled relation arrows, metrics, and conclusion band.
- `premium-process-flow`: 4-stage user or system workflow with a stage spine, directional arrows, stream/output band, checkpoint row, and conclusion band.
- `transformation`: past -> present, old model -> new model, problem -> solution.
- `timeline`: time boxes, version path, meeting agenda, history, rollout, or incident sequence.
- `comparison`: two or three columns showing roles, responsibilities, metrics, or tradeoffs.
- `layer-stack`: levels, maturity stages, audience tiers, or capability layers.
- `cycle`: operating loop, flywheel, feedback mechanism, or iterative process.
- `arrow-flow`: ordered workflow with arrows, checkpoints, handoffs, and decisions.
- `matrix`: categories crossed with evidence, owners, impact, or decision directions.
- `map`: roles, owners, responsibilities, interfaces, and shared goals.
- `layer-stack`: hierarchy, priority, maturity, dependency, or strategic ladder.

Prefer one dominant visual metaphor per image. If an image needs three unrelated metaphors, split it.

Visual diversity rule: for `3+` images, use at least `3` distinct renderer-supported layout types. Do not produce a sequence where every image is a card grid, even when each grid looks clean.

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

### 5. Render Images

Render each card from the storyboard using the best available method.

#### Primary Path: Locked HTML/CSS Rendering

Use `scripts/render_storyboard.py` as the default production path:

1. Build a storyboard using only renderer-supported `layout_type` values from [references/layouts.md](references/layouts.md).
2. Run `python scripts/validate_storyboard.py <storyboard.json>`.
3. Run `python scripts/render_storyboard.py <storyboard.json> --output-dir <output-dir> --keep-html`.
4. Run `python scripts/qa_rendered_html.py <output-dir>/<card-id>.html ...` when HTML files are kept.
5. If the user supplied a visual benchmark, run `python scripts/qa_benchmark_image.py <benchmark.png> <output.png>` for the closest matching card. The gate checks size, edge gaps, bottom gap, and content coverage; failing it means the composition is still too sparse or off-frame.
6. Inspect the generated PNG and HTML. Do not call the output final if visible blocks are misaligned, connector lines dominate the image, or large text areas feel like placeholders.

Supported renderer layouts are:

- `premium-hierarchy-diffusion`: reference-grade hierarchy image with 4 semantic layers, 3 user/audience tiers, optional tier callout, 3 icon-led mechanisms, summary cards, cross-connectors, and conclusion band.
- `premium-cycle-system`: reference-grade operating loop with top strip, double-ring path, inner phase chips, 5-6 loop nodes, output cards, and conclusion band.
- `premium-transformation-logic`: reference-grade input/gate/output conversion machine with zone insights, labeled arrows, conversion artifact band, metrics, and conclusion band.
- `premium-process-flow`: reference-grade four-step workflow with fixed stages, arrows, stream output band, checkpoint row, and conclusion band.
- `cycle`: one center thesis with 4-6 surrounding nodes, optional top flow, metric/output row, and conclusion band.
- `layer-stack`: one upgrade ladder or demand hierarchy with 3-5 layers; optional right-side user tiers.
- `transformation` / `comparison`: 2-3 zones connected by arrows.
- `arrow-flow`: 3-6 ordered steps with directional handoff.
- `timeline`: 3-6 milestones on a visible axis.
- `matrix`: 2-4 columns by 2-5 rows with visible grid relationships.

The renderer must fail on unsupported layouts rather than silently falling back to a generic card grid.

Premium layout rule: if `layout_type` starts with `premium-`, fill its premium-specific fields (`layers`, `user_tiers`, `mechanisms`, `loop_nodes`, `zones`, `stages`, `stream`, `checkpoints`, etc.) and set `layout_family: "premium"`. Do not try to satisfy premium layouts with generic `sections`; the validator should reject missing premium slots.

#### Optional Path: Image Prompt Or Polish

When the user explicitly wants AI image generation, or when the environment has a strong image model and the task tolerates raster text risk, follow [references/image-prompts.md](references/image-prompts.md).

Prefer `deterministic-text` mode: generate a no-text or low-text visual base, then overlay exact text with the renderer. Use `image-text` mode only for short labels or exploratory drafts, and validate by visual inspection or OCR.

### 6. Validate And Deliver

Before final delivery:

- Run `scripts/validate_storyboard.py <storyboard.json>` when a storyboard JSON exists.
- Run `scripts/qa_rendered_html.py` on kept HTML outputs when using the HTML renderer.
- Run `scripts/qa_benchmark_image.py <benchmark.png> <candidate.png>` when the user provides a benchmark image. Treat it as a strict layout-density and edge-gap gate, not a replacement for visual review.
- Compare every rendered text string against the storyboard text ledger.
- Check that Chinese punctuation, English capitalization, acronyms, percentages, dates, names, and numbers are exact.
- Confirm the card count matches the source logic and user brief.
- Confirm visual patterns are varied and not only card grids.
- Confirm connector lines are subtle, aligned to real blocks, and do not create oversized arrowheads or accidental wedges.
- Confirm final images do not contain `PicTalk` unless explicitly requested by the user.
- Export the final images plus the storyboard/source-notes file when useful.

## Output Contract

For a complete PicTalk run, deliver:

- final image files in the requested aspect ratio;
- a short explanation of what each image covers and which visual pattern it uses;
- the storyboard JSON or markdown outline when the user may iterate;
- notes on any source ambiguity or unsupported claims;
- text validation status.

If the user asks only for prompts, provide a storyboard and renderer-ready prompts following [references/image-prompts.md](references/image-prompts.md), and state whether the prompt assumes `deterministic-text` or `image-text` mode.
