# PicTalk

PicTalk is a Codex skill for turning long-form content into presentation-ready information graphics: one image, or a small image set, that explains the source logic clearly.

The skill is designed for text-heavy Chinese/English business, strategy, product, and internal decision materials. It emphasizes:

- source-first reading and logic extraction;
- choosing varied diagram forms instead of defaulting to card grids;
- custom palette mapping;
- deterministic text rendering for accurate Chinese, English, numbers, acronyms, and punctuation;
- storyboard validation before final image export.

## Skill Contents

- `pictalk/SKILL.md`: main workflow instructions.
- `pictalk/references/pattern-library.md`: visual pattern library covering timelines, arrow flows, matrices, funnels, layer maps, swimlanes, cycles, and more.
- `pictalk/references/style-guide.md`: visual style guide.
- `pictalk/references/storyboard-schema.md`: storyboard shape and text ledger rules.
- `pictalk/references/text-accuracy.md`: text accuracy rules.
- `pictalk/scripts/validate_storyboard.py`: storyboard validator.
- `pictalk/assets/storyboard-template.json`: starter storyboard template.

## Use

Copy the `pictalk/` folder into your Codex skills directory, or keep it inside a workspace and invoke it explicitly:

```text
Use $pictalk to turn this article into a concise set of presentation-ready infographics with varied diagram forms.
```

PicTalk is the workflow name. It should not appear as visible branding in final images unless explicitly requested.

