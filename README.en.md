# PicTalk

![License](https://img.shields.io/github/license/nooqle/PicTalk?style=flat-square)
![Skill](https://img.shields.io/badge/Agent-Skill-111111?style=flat-square)
![Codex](https://img.shields.io/badge/Codex-Supported-222222?style=flat-square)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Supported-6B5B95?style=flat-square)

[中文 README](./README.md)

PicTalk is an Agent Skill for turning articles, reports, meeting notes, and product documents into infographics.

It is built for a common presentation need: the document is already written, but the reader needs to see the structure first. PicTalk reads the source, extracts the argument and relationships, chooses a diagram pattern, and renders one or more visual cards for articles, decks, or team memos.

## Quick Start

### Codex

PowerShell:

```powershell
git clone https://github.com/nooqle/PicTalk.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\PicTalk\pictalk" "$env:USERPROFILE\.codex\skills\pictalk"
```

bash:

```bash
git clone https://github.com/nooqle/PicTalk.git
mkdir -p ~/.codex/skills
cp -R PicTalk/pictalk ~/.codex/skills/pictalk
```

Then ask:

```text
Use $pictalk to turn this article into presentation-ready infographics.
```

### Claude Code

PowerShell:

```powershell
git clone https://github.com/nooqle/PicTalk.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\PicTalk\pictalk" "$env:USERPROFILE\.claude\skills\pictalk"
```

bash:

```bash
git clone https://github.com/nooqle/PicTalk.git
mkdir -p ~/.claude/skills
cp -R PicTalk/pictalk ~/.claude/skills/pictalk
```

Then ask:

```text
Use PicTalk to turn this article into 3 Chinese infographics for a presentation.
```

## Examples

### Abstract Methodology To Cycle Diagram

![Tacit knowledge collaboration cycle](./docs/images/hulunyu-02.png)

### Article To Reading Path

![Buddhist Mother reading path](./docs/images/buddhist-mother-20260606-03.png)

### Framework Article To Recognition Map

![Buddhist Mother recognition framework](./docs/images/buddhist-mother-20260606-02.png)

More examples live in [docs/images](./docs/images). Example storyboards include:

- [article-examples-20260606-storyboard.json](./docs/images/article-examples-20260606-storyboard.json)
- [storyboard.json](./docs/images/storyboard.json)
- [buddhist-mother-storyboard.json](./docs/images/buddhist-mother-storyboard.json)
- [meal-flow-storyboard.json](./docs/images/meal-flow-storyboard.json)

## Best For

- Blog posts, newsletter articles, and methodology essays
- Product explainers, feature flows, and AI workflows
- Meeting notes, research material, and project retrospectives
- Report summaries, strategy documents, and training material
- Infographics that need stable Chinese text, numbers, and domain terms

## Prompt Examples

```text
Turn this article into one infographic that explains the main argument.
```

```text
Make 3 visuals from this product brief: one flow, one capability map, one conclusion card.
```

```text
Create a visual summary from these meeting notes. Keep the important numbers and product names.
```

```text
Generate a vertical 3:4 Chinese infographic from this Markdown document.
```

## Workflow

PicTalk follows this workflow:

1. Read the source and identify the topic, claims, phases, actors, relationships, and conclusion.
2. Decide how many images are needed.
3. Pick a diagram pattern and create a storyboard JSON.
4. Render PNG images from the HTML/CSS template.
5. Run QA scripts for structure, size, text, and layout.

For quick work, ask the Agent to run the full flow. For precise edits, modify the storyboard and render again.

## Layouts

### Premium Layouts

| Layout | Best for |
| --- | --- |
| `premium-hierarchy-diffusion` | levels, maturity models, capability stacks, structural upgrades |
| `premium-cycle-system` | feedback loops, operating flywheels, collaboration cycles |
| `premium-transformation-logic` | old state to new state, problem to solution, signal to structure |
| `premium-process-flow` | operation flows, product flows, AI pipelines, streaming output |

### General Layouts

| Layout | Best for |
| --- | --- |
| `arrow-flow` | workflows, operating steps, handoffs |
| `timeline` | phases, versions, event sequences |
| `matrix` | comparison, priority, ownership |
| `layer-stack` | layered structures, capability levels, maturity stages |
| `cycle` | loops and continuous improvement |
| `comparison` / `transformation` | comparisons and solution explanations |

## Design Principles

- Identify the content relationship before choosing a layout.
- Each image should carry one primary structure, such as a hierarchy, flow, cycle, transformation, or matrix.
- Visible text comes from the storyboard. Chinese text, numbers, dates, and domain terms use deterministic text rendering by default.
- Each visual anchor uses one content-specific semantic icon. Geometric decoration can vary, but multiple icons should not be stacked inside one motif.
- Colors carry meaning: blue for the main line, green for outputs or systems, orange for warnings or turns, purple for advanced layers or extensions.
- Images are watermark-free by default, so they can be used directly in articles and presentations.

Default colors:

| Role | Hex |
| --- | --- |
| title navy | `#071B49` |
| primary blue | `#0757D8` |
| green | `#128348` |
| orange | `#E77800` |
| purple | `#5A2BAE` |
| text | `#111827` |
| border | `#BFD2F5` |
| background | `#FFFFFF` |

## Local Rendering

Python and Playwright are required:

```bash
pip install playwright
playwright install chromium
```

Render an example:

```bash
python pictalk/scripts/validate_storyboard.py docs/images/storyboard.json
python pictalk/scripts/render_storyboard.py docs/images/storyboard.json --output-dir docs/images --keep-html
python pictalk/scripts/qa_rendered_html.py docs/images/card-01.html docs/images/card-02.html docs/images/card-03.html
```

## Project Structure

```text
pictalk/
├── SKILL.md
├── assets/
│   ├── storyboard-template.json
│   └── template-infographic.html
├── references/
│   ├── layouts.md
│   ├── pattern-library.md
│   ├── storyboard-schema.md
│   ├── style-guide.md
│   ├── text-accuracy.md
│   └── image-prompts.md
└── scripts/
    ├── validate_storyboard.py
    ├── render_storyboard.py
    ├── qa_rendered_html.py
    ├── qa_benchmark_image.py
    └── analyze_layout_alignment.py

docs/
└── images/
    ├── *.png
    └── *storyboard.json
```

## License

MIT. See [LICENSE](./LICENSE).
