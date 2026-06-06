# Locked Layouts

Use these renderer-supported layouts before rendering. They are intentionally lower-freedom than the conceptual pattern library: each layout maps to a concrete HTML skeleton in `scripts/render_storyboard.py` and `assets/template-infographic.html`.

## Selection Rule

Choose the layout from the argument shape, not from decoration.

For "有质感", "一张图说清楚", "层级指示", "reference-grade", or article hero images, choose a premium layout first. Generic layouts are fallback layouts for simpler cards or secondary images.

For 3+ cards, use at least 3 distinct `layout_type` values. If a card cannot fit a supported layout, split the idea or revise the storyboard. Do not use unsupported layout names and hope the renderer adapts.

## Shared Fields

Every card needs:

- `id`
- `title`
- `subtitle`
- `layout_type`
- `primary_pattern`
- `thesis`
- `composition`
- `canvas`
- `sections`
- `text_ledger`

Recommended canvas:

- `1086x1448` for vertical one-image explanations.
- `1536x1024` for wide slide cards.

Optional shared fields:

- `top_flow`: compact top process strip. Items: `{ "label": "...", "icon": "..." }`.
- `metrics`: bottom output or mechanism cards. Items: `{ "label": "...", "value": "...", "color": "#0757D8" }`.
- `conclusion`: saturated bottom band.
- `conclusion_style`: `blue`, `green`, `purple`, or `orange`.
- `center_text`: only for `cycle`.
- `outputs_title`: heading above metric/output row.
- `side_sections`: only for `layer-stack` with right-side related levels.

All visible strings in these fields must appear exactly in `text_ledger`.

## Premium Layout Contract

Premium layouts are low-freedom templates. They should be filled through their semantic slots, not through generic `sections`.

Every premium card needs:

- `layout_family`: `premium`
- `quality_target`: `presentation` or `reference-grade`
- `density`: `medium` or `dense`
- `canvas`: usually `{ "width": 1086, "height": 1448 }`
- `composition.not_card_grid`: `true`

### PTP01 Premium Hierarchy Diffusion

Use for hierarchy, maturity ladders, capability stacks, layered signals, structural diffusion, or a layered article argument.

Required:

- `layout_type`: `premium-hierarchy-diffusion`
- `axis.label`: the upward meaning of the hierarchy
- `layers`: exactly 4 objects, each with `no`, `title`, `type`, content-specific `icon`, `tone`, `typical_behavior`, `core_blocker`, `matched_audience`, `essence`
- `tiers`: exactly 3 objects, each with `id`, `label`, `headline`, `body`, `tone`, and a content-specific `icon`
- optional `visual_style`: `single`, `stack`, `constellation`, `shield`, `bridge`, or `pyramid`; this changes the geometric background only
- optional `motif_icons`: 1-3 primary-icon candidates; the renderer uses one semantic icon and must not overlap multiple SVG icons inside one motif
- optional `tier_callout`: `{ "text": "...", "icon": "trophy", "tone": "orange" }` for a right-panel emphasis box
- `connectors`: at least 3 relations using `from_layer` and `to_tier`
- `mechanisms`: exactly 3 mechanism cards; add `icon` when possible
- `summary_cards`: 2-3 cards; add `icon` and `tone` when possible
- `conclusion`

Best visual shape:

- large title and subtitle;
- left upward gradient arrow;
- four dense stacked layer modules;
- right-side tier cards;
- a compact right-side callout and a visually emphasized top tier when one tier drives the rest;
- curved layer-to-tier connectors;
- icon-led bottom mechanism chain, summary cards, and conclusion band.

Guardrail:

- Do not hard-code the same tier graphic across topics. Use distinct `icon` values and `visual_style` to make the visual anchor match the article concept. Avoid repeated generic icons such as `network`, `target`, and `layers` when the article suggests more specific symbols.

### PTP02 Premium Cycle System

Use for operating loops, feedback loops, learning loops, flywheels, and "one mechanism keeps producing outputs."

Required:

- `layout_type`: `premium-cycle-system`
- `center.main` and `center.lines`
- `top_flow`: 3-5 compact items
- `loop_nodes`: 5-6 nodes, each with `no`, `title`, `subtitle`, `icon`, `tone`
- `outputs`: 3-5 output cards
- `conclusion`

Best visual shape:

- top logic strip;
- clean central circular thesis;
- surrounding loop nodes attached to segmented circular arrows;
- directional curved arrows that read as a feedback path;
- output row and conclusion band.

Guardrail:

- Step badges sit centered on the top edge of every loop card. Do not move some badges to the left or right side by slot.

### PTP03 Premium Transformation Logic

Use for old state -> mechanism -> new state, confusion -> boundary -> shared language, or before / bridge / after.

Required:

- `layout_type`: `premium-transformation-logic`
- `zones`: exactly 3 zones with `id`, `label`, `title`, `icon`, `tone`, `bullets`, `insight`, and `essence`
- the middle zone must be `tone: "blue"` or `emphasis: true`
- `relations`: exactly 2 labeled arrows connecting zone ids
- `metrics`: 2-4 bottom metric cards
- `conversion_artifact`: final reusable asset/package band with `title`, `subtitle`, and 2-5 item chips
- `conclusion`

Best visual shape:

- input / gate / output zones, not empty columns;
- middle mechanism visually emphasized as calibration gates;
- labeled arrows between zones;
- conversion artifact/package band before the final judgment;
- bottom metric cards and conclusion band.

### PTP04 Premium Process Flow

Use for operation flows, product workflows, AI pipelines, or any process where a four-step path must end in a visible output stream.

Required:

- `layout_type`: `premium-process-flow`
- `stages`: exactly 4 stage cards, each with `no`, `title`, `subtitle`, `icon`, `tone`, and `body`
- `stream`: one output band with `title`, `subtitle`, `icon`, `tone`, and 2-5 `items`
- `checkpoints`: 2-3 cards for quality gates, reader-visible assurances, or system guarantees
- `conclusion`

Best visual shape:

- wide `1536x1024` canvas;
- four top-stage modules connected by directional arrows;
- a large stream/output band beneath the stage spine;
- checkpoint row for input, process, and output quality;
- saturated conclusion band.

Good for:

- "AI 独立入口 -> 上传 / 拍照 -> AI 识别过程 -> Markdown 流式输出";
- "登录 -> 上传材料 -> 自动分析 -> 流式报告";
- product walkthroughs where users need to understand what happens after each action.

Avoid:

- using it for loops or feedback mechanisms; use `premium-cycle-system`;
- more than four main steps; merge minor steps into `body`, `stream.items`, or split into a timeline;
- decorative arrows that do not point from one real stage to another.

## PT01 Cycle

Use for an operating loop, feedback loop, learning loop, or "one center thesis with surrounding steps."

Required:

- `layout_type`: `cycle`
- `sections`: 4-6 nodes
- `center_text`: short central thesis, 2-4 lines

Best visual shape:

- large centered circle;
- numbered surrounding nodes;
- curved arrows;
- optional top flow strip;
- output metric row and conclusion band.

Good for:

- "知识运营的核心工作逻辑";
- "默会知识的协同转译循环";
- "评测归因与图谱迭代".

Avoid:

- more than 6 nodes;
- long paragraph body in nodes;
- using the cycle when the logic is a one-way process.

## PT02 Layer Stack

Use for hierarchy, maturity ladders, layered signals, related tiers, capability levels, or diffusion logic.

Required:

- `layout_type`: `layer-stack`
- `sections`: 3-5 layers, ordered bottom-to-top or low-to-high

Optional:

- `side_sections`: 2-3 related tiers, roles, or audiences on the right side.

Best visual shape:

- left vertical upgrade arrow;
- stacked layer cards with numbered badges;
- optional right related tiers;
- bottom mechanisms and conclusion band.

Good for:

- "从基础信号到系统能力";
- "从局部经验到可复用结构";
- "从基础层到带动层".

Avoid:

- flat lists with no upgrade relation;
- side tiers that repeat the same text as the layers.

## PT03 Transformation / Comparison

Use for old -> new, before -> after, problem -> solution, or two/three mode comparison.

Required:

- `layout_type`: `transformation` or `comparison`
- `sections`: 2-3 zones

Best visual shape:

- two or three large zones;
- arrows between zones;
- middle or final state visually emphasized;
- conclusion band.

Good for:

- "从原始信号到共同语言";
- "从经验纠偏到公共结构";
- "旧协作方式 vs 新协作方式".

Avoid:

- four or more stages; use `arrow-flow` or `timeline` instead.

## PT04 Arrow Flow

Use for a directional workflow, task chain, handoff, or production pipeline.

Required:

- `layout_type`: `arrow-flow`
- `sections`: 3-6 steps

Best visual shape:

- numbered step cards;
- clear arrows;
- checkpoint or output labels;
- metric/output row if useful.

Good for:

- "感受 -> 命名 -> 共享 -> 验证 -> 写回";
- "读取素材 -> 提取论证 -> 构建分镜 -> 渲染校验".

Avoid:

- cyclic logic; use `cycle`.

## PT05 Timeline

Use for time, phases, agenda, version path, incident history, rollout, or maturity over time.

Required:

- `layout_type`: `timeline`
- `sections`: 3-6 milestones

Best visual shape:

- visible horizontal axis;
- milestone dots;
- cards tied to the axis;
- conclusion band.

Avoid:

- non-temporal conceptual groupings; use `layer-stack`, `matrix`, or `arrow-flow`.

## PT06 Matrix

Use when rows and columns are both meaningful: categories crossed with segment type, evidence status, owner, priority, or decision direction.

Required:

- `layout_type`: `matrix`
- `matrix.columns`: 2-4 columns
- `matrix.rows`: 2-5 rows; each row has `label` and `values`

Best visual shape:

- visible row and column grid;
- row labels;
- compact cells;
- optional conclusion band.

Avoid:

- six independent cards with no row/column relationship.

## Validation

Before rendering:

```bash
python pictalk/scripts/validate_storyboard.py storyboard.json
```

After rendering:

```bash
python pictalk/scripts/render_storyboard.py storyboard.json --output-dir output --keep-html
```

If validation fails, fix the storyboard instead of bypassing the validator.
