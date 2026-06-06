# PicTalk · Articles to Infographics

![License](https://img.shields.io/github/license/nooqle/PicTalk?style=flat-square) ![Skill](https://img.shields.io/badge/Skill-Agent-111111?style=flat-square) ![Storyboard Validated](https://img.shields.io/badge/Storyboard-Validated-128348?style=flat-square) ![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square) ![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square) ![Cursor](https://img.shields.io/badge/Cursor-Available-00B4D8?style=flat-square)

> 🌏 **中文版：[README.md](./README.md)**

An Agent skill compatible with Claude Code, Codex, Cursor, and other Agent environments for turning long-form content into **logically clear, text-accurate visual infographics**.

Core workflow: read source material → extract argument structure → prefer premium locked layouts (hierarchy diffusion, cycle system, transformation logic, process flow) → build a storyboard → render text deterministically → validate and deliver.

It does not ask an image model to draw final text. All Chinese, English, numbers, formulas, and labels are rendered through deterministic text layers, guaranteeing zero text errors.

## Example Gallery

**Hierarchy diffusion pattern** — How shared language grows

![PicTalk infographic showcase - Hierarchy diffusion pattern](./docs/images/card-01.png)

**Cycle pattern** — Tacit knowledge collaborative translation loop

![PicTalk infographic showcase - Cycle pattern](./docs/images/card-02.png)

**Transformation logic pattern** — Collaborative transformation from signal to holophrase

![PicTalk infographic showcase - Transformation logic pattern](./docs/images/card-03.png)

**Premium process flow pattern** — Meal AI recognition report journey

![PicTalk infographic showcase - User operation flow pattern](./docs/images/meal-flow.png)

Example assets are committed under `docs/images/card-01.png`, `docs/images/card-02.png`, `docs/images/card-03.png`, and `docs/images/meal-flow.png`. Their storyboard sources are `docs/images/storyboard.json` and `docs/images/meal-flow-storyboard.json`.

## 30-Second Start

**Claude Code users:**

```bash
# Copy pictalk/ into the Claude Code skills directory
cp -r pictalk ~/.claude/skills/pictalk
```

Or send this message to any AI Agent with shell access:

```text
Install the PicTalk skill for me. Clone https://github.com/nooqle/PicTalk locally, then copy the pictalk/ directory to ~/.claude/skills/pictalk. After installation, verify that SKILL.md, references/, and assets/ exist.
```

**Codex users:**

```text
Use $pictalk to turn this article into a concise set of presentation-ready infographics with varied diagram forms.
```

After installation, tell your Agent:

```text
Turn this article into 3-5 infographics, using timelines and arrow flows to show the core logic.
```

Or try these prompts:

```text
Turn this report into visual infographics, Chinese output, blue-green palette.
Make 4 infographics from these meeting notes — one matrix, one funnel.
Create a set of infographics from this document, ensuring all numbers and proper nouns are exact.
```

## Features

- 📐 **Premium locked layouts**: `premium-hierarchy-diffusion`, `premium-cycle-system`, `premium-transformation-logic`, and `premium-process-flow` for "one image explains it" outputs
- 🧭 **Generic fallback layouts**: Transformation, Timeline, Arrow Flow, Layer Stack, Matrix, Cycle, and more for simpler secondary cards
- ✍️ **Deterministic text rendering**: All final text rendered through HTML/SVG/PPTX text layers — never by image models
- 🎨 **Semantic color system**: 12-color semantic palette assigned by meaning, not decoration, with custom palette mapping
- 📋 **Storyboard before rendering**: Build a JSON storyboard (with text ledger, pattern selection, evidence grounding) before entering the render phase
- 🔍 **Auto validation**: Python script validates storyboard structure, required fields, layout types, and brand protection rules
- 🌐 **Chinese/English bilingual**: Optimized for mixed CJK/Latin content with built-in CJK typography rules
- 🚫 **Zero accidental branding**: PicTalk does not appear in final images unless explicitly requested

## Suitable / Not Suitable

**✅ Good for**: Strategy report infographics / Article logic visualization / Chinese-heavy infographics / Product comparison diagrams / Meeting notes visualization / Presentation visual aids

**❌ Not good for**: Large tabular data (use Excel) / Photorealistic imagery / Interactive data dashboards

## Common Use Cases

| Task | Recommended approach |
|------|---------------------|
| Long article to infographics | Extract argument structure first, then generate 3-5 cards at a measured pace |
| Product/solution comparison | Use transformation or matrix pattern to highlight old/new differences |
| Process/timeline visualization | Use arrow flow or timeline pattern, preserving step order and output nodes |
| Org/responsibility mapping | Use responsibility map or swimlane pattern to clarify ownership and collaboration |
| Strategy/hierarchy expression | Use layer stack or pyramid pattern for priority and maturity levels |
| Meeting notes visualization | Filter to core conclusions first, then choose 2-3 patterns along the argument chain |

## Why Deterministic Text Rendering

Most "article to image" tools fail in two places: they over-summarize before understanding the source, and they let image models invent or corrupt text. PicTalk fixes this with a stricter loop:

```text
Read source → extract argument → choose diagram pattern → build storyboard (with text ledger) → locked-layout HTML rendering → validate and deliver
```

- The storyboard `text_ledger` is the single source of truth for all visible text — renderers draw from it verbatim, never paraphrase
- Locked HTML/CSS layouts are the default final renderer, so weaker models do not have to invent layout systems on the fly
- After rendering, compare every visible string against the text_ledger; high-risk tokens (proper nouns, acronyms, percentages, dates) require manual verification
- Image-capable models may generate no-text visual bases or exploratory drafts, but final delivery should prefer deterministic text layers

## Platform Support

| Platform | Status | Notes |
|----------|--------|-------|
| Claude Code | Supported | Native Skill workflow; copy to `~/.claude/skills/` |
| Codex | Supported | Adapted via `agents/openai.yaml`, triggered with `$pictalk` |
| Cursor / other local Agents | Available | Requires file read/write and shell command execution |
| Plain chatbot | Not recommended | Without a file system, stable storyboard generation and output validation are difficult |

## Installation

### Option 1: Claude Code (recommended)

```bash
# Clone the repo and copy the skill directory
git clone https://github.com/nooqle/PicTalk.git /tmp/pictalk-repo
cp -r /tmp/pictalk-repo/pictalk ~/.claude/skills/pictalk
```

### Option 2: Send this message to your AI Agent

> Install the `PicTalk` Agent skill for me. Follow these steps:
>
> 1. Make sure `~/.claude/skills/` directory exists (create it if not)
> 2. Run `git clone https://github.com/nooqle/PicTalk.git /tmp/pictalk-repo`
> 3. Run `cp -r /tmp/pictalk-repo/pictalk ~/.claude/skills/pictalk`
> 4. Verify: `ls ~/.claude/skills/pictalk/` should show `SKILL.md`, `references/`, and `assets/`
> 5. Tell me it's installed — saying "make infographics" will trigger this skill

### Option 3: Codex

Place the `pictalk/` directory into your Codex skills directory and use the `$pictalk` trigger syntax.

### Trigger Phrases

Once installed, the Agent will auto-discover and invoke this skill. Trigger keywords:

- "turn this article into infographics"
- "create a set of presentation-ready visual cards"
- "visualize this timeline process"
- "帮我做一组信息图"
- "生成可视化信息图"

## Workflow

The skill is a structured workflow; the Agent guides you step by step:

1. **Ingest source** — Article, PDF, meeting notes, transcript, or pasted text
2. **Extract argument** — Main thesis, supporting claims, causal chain, phases, actors, metrics, tensions, conclusion
3. **Decide card count** — 1 card for a central idea, 2-3 for major branches, 4-7 for dense material, 7+ suggest splitting
4. **Select diagram pattern** — Prefer premium locked layouts for reference-grade outputs; use generic layouts as fallback
5. **Build storyboard** — Record exact visible text, layout type, premium semantic slots, evidence source, palette roles, text ledger
6. **Render images** — Use locked HTML/CSS layouts as the primary deterministic path; use image models only as optional visual bases or exploratory drafts
7. **Validate and deliver** — Check text accuracy, visual pattern diversity, source grounding, brand protection

Full details in [`SKILL.md`](./pictalk/SKILL.md).

## Visual Patterns

PicTalk includes 4 premium locked layouts plus generic fallback patterns. Prefer premium layouts when the user asks for a polished one-image explanation.

| Premium Layout | Best for |
|----------------|----------|
| `premium-hierarchy-diffusion` | Hierarchies, maturity ladders, user tiers, capability stacks, high-to-low diffusion |
| `premium-cycle-system` | Feedback loops, operating flywheels, translation cycles, continuous improvement; inner phase chips plus a double-ring feedback path |
| `premium-transformation-logic` | input fragments → calibration gates → output structure; zone insights plus a conversion artifact band |
| `premium-process-flow` | User journeys, product operation flows, AI pipelines; four-stage spine plus stream output band and checkpoints |

Generic fallback patterns:

| Pattern | Best for |
|---------|----------|
| Transformation | before/after, old/new model, problem/solution |
| Timeline | agendas, version paths, incident sequences, phases |
| Arrow Flow | processes, value chains, task handoffs, decision paths |
| Layer Stack | maturity, user tiers, capability levels, demand layers |
| Matrix | categories crossed with evidence, owners, decisions, or impact |
| Responsibility Map | owners, DRIs, workgroups, interfaces, shared metrics |
| Cycle / Flywheel | feedback loops, operating rhythms, continuous improvement |
| Funnel | filtering from broad signals to selected cases or decisions |
| Pyramid | priority, foundations, strategic ladders, dependency order |
| Radial Map | central thesis with surrounding drivers or consequences |
| Swimlane | cross-team workflows, role splits, handoffs |
| Scorecard Plus | high-level diagram + 3-5 key metrics or principles panel |

Selection rules and anti-patterns in [`pattern-library.md`](./pictalk/references/pattern-library.md).

## Color System

Default 12-color semantic palette, assigned by meaning:

| Role | Hex | Use |
|------|-----|-----|
| `title_navy` | `#071B49` | Main headings and strongest text |
| `primary_blue` | `#0757D8` | Main arrows, badges, conclusion bars |
| `blue_light` | `#EAF2FF` | Blue module fills and icon wells |
| `green` | `#128348` | User, behavior, success, governance |
| `green_light` | `#EAF7EF` | Green module fills |
| `orange` | `#E77800` | Knowledge, warning, middle-layer emphasis |
| `orange_light` | `#FFF1DE` | Orange module fills |
| `purple` | `#5A2BAE` | Exploration, innovation, advanced topics |
| `purple_light` | `#F1EAFB` | Purple module fills |
| `gray` | `#6B7280` | Past state, secondary labels |
| `border` | `#BFD2F5` | Thin module borders |
| `text` | `#111827` | Body text |

Customization rule: preserve contrast and assign colors by meaning, not decoration. When users supply a palette, map it into the semantic roles above.

Typography rules in [`style-guide.md`](./pictalk/references/style-guide.md).

## Storyboard Format

Every output starts with a storyboard JSON. A minimal card entry:

```json
{
  "id": "card-01",
  "title": "Cognitive Shift: From Old Model to New Model",
  "layout_type": "transformation",
  "primary_pattern": "transformation",
  "composition": {
    "dominant_structure": "Two zones connected by a large arrow, closed by a conclusion band at the bottom.",
    "not_card_grid": true,
    "visible_marks": ["left-right zones", "large arrow", "number badges", "bottom conclusion band"]
  },
  "text_ledger": [
    "Cognitive Shift: From Old Model to New Model",
    "Past: Old Model",
    "Action-first approach",
    "Value hard to consolidate",
    "Key insight: Clarify the value path before aligning action."
  ]
}
```

Validate a storyboard:

```bash
python pictalk/scripts/validate_storyboard.py pictalk/assets/storyboard-template.json
```

Render storyboard to PNG in one command:

```bash
python pictalk/scripts/render_storyboard.py storyboard.json --template pictalk/assets/template-infographic.html --output-dir output/
```

Keep HTML and run basic visual QA:

```bash
python pictalk/scripts/render_storyboard.py storyboard.json --output-dir output/ --keep-html
python pictalk/scripts/qa_rendered_html.py output/card-01.html
```

When a visual benchmark exists, compare layout density, edge gaps, and bottom whitespace against it:

```bash
python pictalk/scripts/qa_benchmark_image.py benchmark.png output/card-01.png
```

The default gate checks size, top/left/right gaps, bottom whitespace, and content coverage. If it fails, revise the layout or switch to a better premium layout before delivery.

Full storyboard schema in [`storyboard-schema.md`](./pictalk/references/storyboard-schema.md), text accuracy rules in [`text-accuracy.md`](./pictalk/references/text-accuracy.md).

## Example Prompts

Copy any of these into your Agent, then attach your article, Markdown, or source file:

```text
Turn this article into 3-5 infographics, using timelines and arrow flows to show the core logic, blue palette.
```

```text
Make this product comparison document into visual infographics, using a matrix pattern to highlight differences. Ensure all data is exact.
```

```text
Create 4 infographics from these meeting notes — use a different diagram pattern for each, Chinese output.
```

```text
Turn this report into 5 presentation-ready infographics. Use varied diagram forms. Ensure all numbers and acronyms are exact.
```

## Project Structure

```
pictalk/
├── SKILL.md                      ← Main skill file: workflow, principles, validation rules
├── agents/
│   ├── openai.yaml               ← Codex adapter config
│   └── generic.yaml              ← Generic Agent adapter config
├── assets/
│   ├── storyboard-template.json  ← Valid premium storyboard JSON template
│   └── template-infographic.html ← Locked HTML/CSS rendering template
├── references/
│   ├── layouts.md                ← Premium + generic locked layout contract
│   ├── pattern-library.md        ← 12 patterns + combos + anti-patterns
│   ├── storyboard-schema.md      ← Full storyboard JSON schema docs
│   ├── style-guide.md            ← Canvas sizes, 12-color palette, typography, components, layout families
│   ├── text-accuracy.md          ← Text accuracy rules, text_ledger workflow, high-risk tokens
│   └── image-prompts.md          ← Optional image prompt modes: no-text base / image-text draft
└── scripts/
    ├── validate_storyboard.py    ← Validates structure, required fields, layout types, brand protection
    ├── render_storyboard.py      ← Storyboard JSON → PNG one-command rendering
    ├── qa_rendered_html.py       ← Checks rendered HTML for viewport overflow and clipped text
    ├── qa_benchmark_image.py     ← Compares size, whitespace, and content coverage against a benchmark
    └── analyze_layout_alignment.py ← Decomposes sample content bounds, gaps, coverage, and density peaks
docs/
└── images/                       ← Example infographic screenshots
    ├── card-01.png
    ├── card-02.png
    ├── card-03.png
    └── meal-flow.png
```

## Core Design Principles

1. **Evidence before visuals** — Source grounding matters more than visual polish
2. **Logic before reading** — The reader should see the structure before finishing the text
3. **Cards are containers, not compositions** — Cards are local containers; every image needs a dominant diagram structure
4. **Every visible string comes from the storyboard ledger** — Rendering only draws from `text_ledger` strings
5. **No generated pseudo-text in final images** — Image models never draw final text
6. **Show ambiguity instead of inventing certainty** — When the source is unclear, mark it rather than fabricating a clean-looking argument
7. **Pattern diversity** — For 3+ images, use at least 3 distinct primary patterns
8. **Consistent terminology** — Skills are Skills; no mixed Chinese-English translation

## Roadmap

- Add real case studies and openable infographic examples
- Add more premium locked layouts and visual QA checks
- Improve multilingual text QA workflow
- Add more palette presets
- Add adapter configs for Cursor, Windsurf, and other platforms
- Support reading articles directly from URLs

## FAQ

**How is PicTalk different from typical "article to image" tools?**

The key difference is deterministic text rendering. PicTalk never lets image models draw text — instead, it renders through HTML/SVG/PPTX text layers precisely. It also extracts argument structure before choosing a diagram pattern, rather than simply arranging text into cards.

**What output formats are supported?**

HTML/CSS exported to PNG/PDF, SVG, PPTX/Keynote/Google Slides. The core requirement is deterministic text rendering; the specific format depends on the rendering environment.

**Can I customize colors?**

Yes. User-supplied palettes are mapped to semantic roles (primary, accent_success, accent_warning, etc.), preserving contrast and readability.

**Is the storyboard JSON required?**

Recommended. The storyboard is the foundation for text accuracy and makes iteration easier. But for quick outputs, you can skip the full storyboard and generate directly.

**How do I update to the latest version?**

Re-run the install command, or run `git pull` in your local skill directory.

## Contributing

Bugs, pattern requests, renderer templates, validation improvements — Issues and PRs welcome. Prioritize:

- New patterns go in `references/pattern-library.md` with applicable scenarios
- New renderer templates provide corresponding `assets/` files
- Validation rule updates sync to `scripts/validate_storyboard.py`
- Text accuracy rule updates sync to `references/text-accuracy.md`
- Storyboard schema updates sync to `references/storyboard-schema.md`

## License

MIT. See [LICENSE](./LICENSE).
