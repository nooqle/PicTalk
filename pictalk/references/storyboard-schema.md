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
- For each card: `id`, `title`, `layout_type`, `primary_pattern`, `composition`, `thesis`, `canvas`, `text_ledger`
- For generic layouts: `sections`
- For premium layouts: the matching premium semantic slots, such as `layers`, `loop_nodes`, `zones`, `stages`, `stream`, and `checkpoints`
- For each section: `id`, `heading`, `body`

## Renderer-Supported Layout Types

Use one of:

- `premium-hierarchy-diffusion`
- `premium-cycle-system`
- `premium-transformation-logic`
- `premium-process-flow`
- `transformation`
- `comparison`
- `cycle`
- `arrow-flow`
- `timeline`
- `layer-stack`
- `matrix`

`primary_pattern` should use the same vocabulary as `layout_type`, plus optional precise variants such as `hierarchy-map`, `demand-ladder`, `diffusion-map`, `scorecard-plus-diagram`, or `timeline-plus-map`.

Conceptual patterns such as funnel, pyramid, radial, swimlane, principles, and hybrid are useful during analysis, but the locked renderer does not accept those as `layout_type`. Bind them to the closest supported renderer layout before validation.

For reference-grade or "one image explains it" outputs, choose a premium layout before generic layouts. Premium layouts require premium-specific semantic fields and should not be filled only with `sections`.

## Layout-Specific Fields

### `premium-hierarchy-diffusion`

Use for a 4-level hierarchy with related tiers and diffusion mechanisms.

- `layout_family`: `premium`
- `quality_target`: `presentation` or `reference-grade`
- `density`: `medium` or `dense`
- `canvas`: `{ "width": 1086, "height": 1448 }` unless `allow_custom_canvas` is true
- `axis`: `{ "label": "...", "direction": "up" }`
- `layers`: exactly 4 objects; each requires `no`, `title`, `type`, `icon`, `tone`, `typical_behavior`, `core_blocker`, `matched_audience`, `essence`
- `tiers`: exactly 3 objects; each requires `id`, `label`, `headline`, `body`, `tone`; `reference-grade` cards also require `icon`
- `visual_style`: optional motif style for `layers` and `tiers`; one of `single`, `stack`, `constellation`, `shield`, `bridge`, `pyramid`; it changes geometric decoration only
- `motif_icons`: optional list of 1-3 primary-icon candidates. The final rendered motif uses exactly one semantic SVG icon; never compose a motif by overlapping multiple icons.
- `tier_callout`: optional object with `text`, `icon`, and `tone`; use it for the right-side emphasis box in benchmark-like hierarchy images
- `connectors`: at least 3 objects; each references a layer with `from_layer` and a tier with `to_tier`
- `mechanisms`: exactly 3 objects; each requires `no`, `title`, `body`, `tone`; optional `icon`
- `summary_cards`: 2-3 objects; each requires `title` and `body`; optional `icon` and `tone`
- `conclusion`

### `premium-cycle-system`

Use for a central mechanism with a loop and explicit outputs.

- `layout_family`: `premium`
- `quality_target`: `presentation` or `reference-grade`
- `center`: `{ "main": "...", "lines": ["..."] }`
- `top_flow`: 3-5 items
- `top_flow`: 3-5 compact labels for the strip above the loop; keep the cycle center clean
- `loop_nodes`: 5-6 nodes; each requires `no`, `title`, `subtitle`, `icon`, `tone`
- `outputs`: 3-5 cards; each requires `title`, `body`, `icon`, `tone`
- `outputs_title`
- `conclusion`

### `premium-transformation-logic`

Use for old state -> mechanism -> new state.

- `layout_family`: `premium`
- `quality_target`: `presentation` or `reference-grade`
- `zones`: exactly 3 zones; each requires `id`, `label`, `title`, `icon`, `tone`, `bullets`, `essence`; `insight` is required for `reference-grade`
- middle zone must be `tone: "blue"` or `emphasis: true`
- `relations`: exactly 2 labeled arrows using zone ids in `from` and `to`
- `metrics`: 2-4 cards
- `conversion_artifact`: required for `reference-grade`; object with `title`, `subtitle`, `items`, optional `icon`, and optional `tone`
- `conclusion`

### `premium-process-flow`

Use for a four-step operation flow, product workflow, AI pipeline, or "input -> process -> stream output" workflow.

- `layout_family`: `premium`
- `quality_target`: `presentation` or `reference-grade`
- `density`: `medium` or `dense`
- `canvas`: `{ "width": 1536, "height": 1024 }` unless `allow_custom_canvas` is true
- `stages`: exactly 4 objects; each requires `no`, `title`, `subtitle`, `icon`, `tone`, and `body`; `body` contains 1-3 short items
- `stream`: required output band object with `title`, `subtitle`, `icon`, `tone`, and `items`; `items` contains 2-5 streaming or output states
- `checkpoints`: 2-3 checkpoint cards; each requires `title`, `body`, `icon`, and `tone`
- `conclusion`

Best for:

- "用户登录 -> 上传 / 拍照 -> AI 识别过程 -> Markdown 流式输出"
- "素材输入 -> 模型处理 -> 人工复核 -> 结构化交付"
- "采集 -> 清洗 -> 分析 -> 报告流式生成"

### `cycle`

- `sections`: 4-6 loop nodes.
- `center_text`: short center thesis.
- Optional `top_flow`, `metrics`, `outputs_title`, and `conclusion`.

### `layer-stack`

- `sections`: 3-5 stacked layers.
- Optional `side_sections`: 2-3 related tiers, roles, or audience levels.
- Optional `metrics`: bottom diffusion mechanisms or outputs.

### `transformation` / `comparison`

- `sections`: 2-3 zones.
- Optional `footer` on each section for essence labels.

### `arrow-flow`

- `sections`: 3-6 ordered steps.

### `timeline`

- `sections`: 3-6 milestones.
- Optional `badge` on each section for dates or phase numbers.

### `matrix`

- `matrix.columns`: 2-4 column labels.
- `matrix.rows`: 2-5 rows; each row has `label` and `values`.

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

The renderer must render from `text_ledger` strings or from fields that exactly duplicate ledger strings. When constructing optional AI image prompts, include text_ledger entries verbatim only in `image-text` draft mode; in deterministic-text mode, generate no-text visual assets and overlay final text with the renderer.

Default visible-brand rule: do not include `PicTalk` in `text_ledger`, titles, subtitles, footers, watermarks, or visible labels unless `project.allow_visible_pictalk_brand` is explicitly `true`.
