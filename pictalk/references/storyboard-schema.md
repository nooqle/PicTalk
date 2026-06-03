# Storyboard Schema

Create a storyboard before rendering. It is the source of truth for text accuracy, layout choice, and source grounding.

## Recommended JSON Shape

```json
{
  "project": {
    "title": "Project title",
    "source_language": "zh-CN",
    "output_language": "zh-CN",
    "audience": "internal strategy presentation",
    "aspect_ratio": "3:4",
    "card_count_rationale": "Four branches in the article require four cards.",
    "allow_visible_pictalk_brand": false
  },
  "palette": {
    "title_navy": "#071B49",
    "primary_blue": "#0757D8",
    "green": "#128348",
    "orange": "#E77800",
    "purple": "#5A2BAE",
    "background": "#FFFFFF"
  },
  "source_notes": [
    {
      "id": "S1",
      "quote_or_summary": "Source-backed point.",
      "location": "section title, paragraph, timestamp, or page"
    }
  ],
  "cards": [
    {
      "id": "card-01",
      "title": "Exact rendered title",
      "subtitle": "Exact rendered subtitle",
      "layout_type": "transformation",
      "primary_pattern": "transformation",
      "supporting_patterns": ["arrow-flow", "conclusion-band"],
      "thesis": "The point this card must make in 20 seconds.",
      "composition": {
        "dominant_structure": "Two zones connected by a large arrow.",
        "not_card_grid": true,
        "visible_marks": ["large arrow", "two zones", "bottom conclusion band"]
      },
      "canvas": {
        "width": 1536,
        "height": 1024
      },
      "sections": [
        {
          "id": "past",
          "heading": "过去：职能导向",
          "icon": "file-text",
          "body": [
            "内容 = 生产即价值",
            "运营 = 执行动作"
          ],
          "source_ids": ["S1"]
        }
      ],
      "connectors": [
        {
          "from": "past",
          "to": "present",
          "kind": "arrow",
          "label": "从内容分发，升级为知识交付"
        }
      ],
      "conclusion": "核心定位：知识运营负责经营 AI 可用的业务知识供给",
      "text_ledger": [
        "Exact rendered title",
        "Exact rendered subtitle",
        "过去：职能导向",
        "内容 = 生产即价值",
        "运营 = 执行动作",
        "从内容分发，升级为知识交付",
        "核心定位：知识运营负责经营 AI 可用的业务知识供给"
      ]
    }
  ]
}
```

## Required Fields

- `project.title`
- `project.output_language`
- `project.aspect_ratio`
- `project.card_count_rationale`
- `project.allow_visible_pictalk_brand` unless the skill name is intentionally part of the final visible content
- `palette`
- `source_notes`
- `cards`
- For each card: `id`, `title`, `layout_type`, `primary_pattern`, `composition`, `thesis`, `canvas`, `sections`, `text_ledger`
- For each section: `id`, `heading`, `body`

## Layout Types

Use one of:

- `transformation`
- `timeline`
- `comparison`
- `layer-stack`
- `cycle`
- `arrow-flow`
- `matrix`
- `map`
- `pyramid`
- `funnel`
- `radial`
- `swimlane`
- `principles`
- `hybrid`

`primary_pattern` should use the same vocabulary as `layout_type`, plus optional precise variants such as `responsibility-map`, `scorecard-plus-diagram`, or `timeline-plus-map`.

## Composition

Every card must name its dominant visual structure:

```json
{
  "dominant_structure": "Vertical timeline with six milestone ticks.",
  "not_card_grid": true,
  "visible_marks": ["timeline axis", "milestone ticks", "handoff arrows", "output band"]
}
```

`not_card_grid` means the image is not merely a mosaic of same-sized cards. It may still contain local cards, but the overall visual logic must be a timeline, flow, matrix, map, hierarchy, loop, funnel, or another named structure.

## Text Ledger

Every visible text string must appear in `text_ledger`, including:

- titles and subtitles;
- labels and badges;
- section headings;
- bullet text;
- connector labels;
- metric names and values;
- footnotes and source labels;
- conclusion text.

The renderer must render from `text_ledger` strings or from fields that exactly duplicate ledger strings. Do not write new visible text directly inside a prompt to an image model.

Default visible-brand rule: do not include `PicTalk` in `text_ledger`, titles, subtitles, footers, watermarks, or visible labels unless `project.allow_visible_pictalk_brand` is explicitly `true`.
