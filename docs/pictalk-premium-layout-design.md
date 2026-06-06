# PicTalk Premium Layout System Design

## Goal

Upgrade PicTalk from "clear structural drafts" to "one polished infographic explains one thing." The system should let weaker models produce better outputs by filling strict layouts instead of inventing information design from scratch.

Implementation status: the four premium layouts in this document are implemented in `pictalk/scripts/render_storyboard.py`, styled in `pictalk/assets/template-infographic.html`, validated in `pictalk/scripts/validate_storyboard.py`, and demonstrated by `docs/images/storyboard.json` and `docs/images/meal-flow-storyboard.json`.

Target quality reference:

- vertical 3:4 Chinese business infographic;
- one dominant logic structure per image;
- high information density without cramped text;
- strong title, subtitle, semantic modules, connectors, layer indicators, output mechanisms, and conclusion band;
- deterministic Chinese text rendering.

## Diagnosis

Current PicTalk solved text accuracy and basic layout stability, but not premium information design.

Observed gaps:

- `sections.heading + body + footer` is too coarse for rich layered diagrams.
- Layouts are generic (`cycle`, `layer-stack`, `transformation`) instead of reference-grade compositions.
- The renderer has too few semantic slots: it cannot distinguish signal, blocker, related tier, essence, evidence, mechanism, and conclusion.
- The validator checks structure and ledger coverage, but not layout-specific quality rules such as density, required connectors, emphasis pills, module counts, and bottom mechanism rows.
- The template has a house style, but not enough local components: essence pills, left gradient rails, content-specific visual motifs, cross-links, curved arrows, output mechanism chains, dense section metadata.

Guizang works better because it uses:

- registered layouts instead of open-ended design;
- content-shape-to-layout rules;
- a template as the source of style truth;
- preflight checks;
- visual QA checklist;
- validators that block known bad structures.

PicTalk should adopt the same low-freedom philosophy, but for single-image explanation graphics.

## Design Principles

1. **Premium layouts, not generic layouts.** Keep the current generic layouts as fallback, but introduce premium layouts for flagship outputs.
2. **Semantic slots before prose.** Each layout should know what a field means: behavior, blocker, tier, essence, output, relation.
3. **No silent degradation.** If a required slot is missing, validation fails.
4. **Source-grounded compression.** The agent may compress source language, but every visible string must enter `text_ledger`.
5. **Visual constraints are part of the contract.** Layout ratio, module count, connector count, and density are validated.
6. **Reference matching beats creative freedom.** When user asks for "one image explains it," default to a premium layout.
7. **Low-freedom structure, high-freedom local motifs.** Layout geometry should be stable; icons, motif combinations, and local graphics should be chosen from the article semantics so outputs do not all look identical.

## Premium Layouts

### PTP01 `premium-cycle-system`

Use for one core mechanism with surrounding operating loop.

Reference shape:

- top logic strip;
- clean central circular thesis;
- 5-6 surrounding nodes attached to segmented circular arrows;
- directional curved arrows with feedback semantics;
- output row;
- saturated conclusion band.

Required schema:

```json
{
  "layout_type": "premium-cycle-system",
  "center": {
    "main": "感知经验 → 理知结构",
    "lines": ["新的协同场域", "自我认知迭代"]
  },
  "top_flow": [
    { "label": "图谱定义业务世界", "icon": "network" }
  ],
  "loop_nodes": [
    {
      "no": "1",
      "title": "知识结构化",
      "subtitle": "构建实体、关系、规则与场景方案图谱",
      "icon": "network",
      "tone": "blue"
    }
  ],
  "outputs": [
    { "title": "业务知识图谱", "icon": "network", "tone": "blue" }
  ],
  "conclusion": "核心结论：..."
}
```

Validation:

- `loop_nodes` count must be 5-6.
- Each node must have `no`, `title`, `subtitle`, `icon`, and `tone`.
- `top_flow` count must be 3-5.
- The center should stay clean; path mechanics belong in `top_flow`, `loop_nodes`, and the visible arrow order.
- `outputs` count must be 3-5.
- `center.main` must be <= 16 Chinese characters or split into `lines`.

### PTP02 `premium-hierarchy-diffusion`

Use for layered arguments, maturity ladders, structural diffusion, related tiers, or capability levels.

Reference shape:

- large title and subtitle;
- left upward gradient arrow;
- middle 4 stacked layer modules;
- each layer has icon block, title, type, signal, constraint, context, essence pill;
- right related-tier hierarchy with a compact callout, emphasized top tier, and connected arrows;
- bottom "three diffusion mechanisms" row;
- final conclusion band.

Required schema:

```json
{
  "layout_type": "premium-hierarchy-diffusion",
  "axis": {
    "label": "结构层级逐级升级",
    "direction": "up"
  },
  "layers": [
    {
      "no": "4",
      "title": "系统能力",
      "type": "跨场景整合层",
      "icon": "network",
      "tone": "blue",
      "typical_behavior": "多个场景开始复用同一套方法",
      "core_blocker": "经验分散，缺少可迁移结构",
      "matched_audience": "复杂项目 / 跨团队协作 / 方法沉淀",
      "essence": "可复用系统能力"
    }
  ],
  "tiers": [
    {
      "label": "C 复用层",
      "headline": "稳定结构决定后续协作的复用上限",
      "body": ["跨场景复用", "标准化表达", "持续写回"],
      "tone": "green"
    }
  ],
  "tier_callout": {
    "text": "稳定结构决定协作复用的上限",
    "icon": "trophy",
    "tone": "orange"
  },
  "connectors": [
    { "from_layer": "4", "to_tier": "C", "tone": "green", "kind": "curved-arrow" }
  ],
  "mechanisms": [
    {
      "no": "1",
      "title": "结构带动执行",
      "body": "清晰结构→更稳定行动→协作者更容易复用",
      "icon": "clipboard",
      "tone": "blue"
    }
  ],
  "summary_cards": [
    { "title": "高阶结构可以带动低阶执行", "body": "优先打磨可复用结构...", "icon": "trophy", "tone": "blue" }
  ],
  "conclusion": "核心结论：..."
}
```

Validation:

- `layers` count must be exactly 4 for this layout.
- `tiers` count must be exactly 3.
- `mechanisms` count must be exactly 3.
- `connectors` must cover at least 3 layer-to-tier relations.
- Each layer must have `typical_behavior`, `core_blocker`, `matched_audience`, and `essence`.
- Each essence string must be <= 18 Chinese characters.
- `conclusion` must fit one or two lines.

### PTP03 `premium-transformation-logic`

Use for before / mechanism / after.

Reference shape:

- 3 role-specific zones: input material, calibration gates, output structure;
- middle zone visually emphasized;
- arrows between zones;
- each zone has a state judgment `insight`, role-specific bullet modules, and an essence pill;
- conversion artifact/package band;
- bottom metric row and conclusion band.

Required schema:

```json
{
  "layout_type": "premium-transformation-logic",
  "zones": [
    {
      "label": "旧状态",
      "title": "混乱前进",
      "icon": "book-open",
      "insight": "材料是散的，只有人能凭经验判断。",
      "bullets": ["说出来像是理解了"],
      "essence": "经验维持",
      "tone": "gray"
    }
  ],
  "relations": [
    { "from": "old", "to": "mechanism", "label": "压缩", "tone": "blue" }
  ],
  "metrics": [
    { "label": "边界", "value": "语言 ≠ 行动" }
  ],
  "conversion_artifact": {
    "title": "协同资产包",
    "subtitle": "边界、验证和行动被打包成下一轮调用结构。",
    "items": ["边界词汇", "验证规则", "行动闭环"]
  },
  "conclusion": "核心结论：..."
}
```

Validation:

- `zones` count must be exactly 3.
- middle zone must have `tone: blue` or `emphasis: true`.
- each zone must have 2-4 bullets, one `insight`, and one `essence` for reference-grade cards.
- relation labels must be visible in `text_ledger`.
- reference-grade cards must include `conversion_artifact`.

### PTP04 `premium-process-flow`

Use for product operation flows, AI pipelines, and any four-step process where progressive output must be visible.

Reference shape:

- 1536x1024 wide canvas;
- four top-stage cards connected by directional arrows;
- a large stream/output band below the stage spine;
- 2-3 checkpoint cards for input/process/output assurances;
- saturated conclusion band.

Required schema:

```json
{
  "layout_type": "premium-process-flow",
  "layout_family": "premium",
  "quality_target": "reference-grade",
  "stages": [
    {
      "no": "01",
      "title": "AI 独立入口",
      "subtitle": "登录后进入餐食识别入口",
      "icon": "log-in",
      "tone": "blue",
      "body": ["完成登录与身份确认", "点击 AI 图片识别"]
    }
  ],
  "stream": {
    "title": "报告以 Markdown 流式输出",
    "subtitle": "后端逐段返回 Markdown，前端边接收边渲染。",
    "icon": "stream",
    "tone": "green",
    "items": ["识别食物类别", "估算克重与营养", "持续追加报告段落"]
  },
  "checkpoints": [
    {
      "title": "过程可见",
      "body": "识别食物、估算克重、计算营养结构的过程需要被用户看见。",
      "icon": "check",
      "tone": "green"
    }
  ],
  "conclusion": "核心结论：..."
}
```

Validation:

- `stages` count must be exactly 4.
- each stage must have `no`, `title`, `subtitle`, `icon`, `tone`, and 1-3 body items.
- `stream` must have `title`, `subtitle`, `icon`, `tone`, and 2-5 items.
- `checkpoints` count must be 2-3.
- default canvas must be 1536x1024.

## Schema Strategy

Keep existing `sections` for generic layouts, but add premium layout fields.

New top-level card fields:

- `layout_family`: `generic` or `premium`.
- `quality_target`: `draft`, `presentation`, or `reference-grade`.
- `density`: `light`, `medium`, `dense`.
- `visual_reference`: optional reference image label or local path.

Premium cards should not rely on generic `sections` except as fallback. The renderer should read premium-specific fields first.

## Renderer Design

Add four renderer functions:

- `render_premium_cycle_system(card)`
- `render_premium_hierarchy_diffusion(card)`
- `render_premium_transformation_logic(card)`
- `render_premium_process_flow(card)`

Add CSS components:

- `.premium-title`
- `.logic-strip`
- `.essence-pill`
- `.layer-rail`
- `.layer-module`
- `.visual-motif`
- `.connector-svg`
- `.mechanism-chain`
- `.summary-card-row`
- `.process-spine`
- `.process-stream`
- `.process-checkpoint-row`
- `.conclusion-hero`

Do not over-abstract. Premium layouts should be explicit, even if some code repeats.

## Validator Design

Add `validate_premium_card(card)` with per-layout rules.

Checks:

- required fields by premium layout;
- exact counts;
- maximum text lengths;
- all visible strings in `text_ledger`;
- connector endpoints exist;
- tones are from allowed semantic palette;
- no unsupported icons;
- no `PicTalk` visible branding;
- `canvas` must be `1086x1448` unless explicitly overridden.

Visual QA checks:

- screenshot dimensions match canvas;
- no rendered text extends outside the viewport;
- benchmark comparison checks edge gaps, bottom gap, and content coverage when a reference image is provided;
- conclusion band is present and above bottom margin;
- connector SVG exists for layouts that require connectors.
- premium cycle requires loop nodes, segmented arc paths, a clean center, and output cards;
- premium transformation requires exactly three zones, one insight per zone, and a conversion artifact band.
- premium process flow requires four stages, three arrows, a stream band, and checkpoint cards.

## Prompt Design

`image-prompts.md` should include prompt families for premium layouts, but still mark image-text as risky.

Prompt modes:

- `deterministic-text`: generate no-text base or visual style study.
- `premium-layout-draft`: image model draws the complete draft for exploration only.
- `html-render-final`: renderer produces final PNG.

For weaker models, the prompt should be generated from premium schema, not from raw article text.

## Workflow

1. Read source.
2. Extract `logic_map`.
3. Decide if the output is one-image or multi-image.
4. If one-image, choose a premium layout first.
5. Fill premium schema slots.
6. Validate storyboard.
7. Render HTML and PNG.
8. Run visual QA checklist.
9. If quality is below target, revise schema density or layout, not just colors.

## Implementation Plan

Status: implemented and benchmark-calibrated as a first complete pass. Future work should add more premium layouts only after these four remain stable on real articles and product flows.

### Phase 1: Premium Hierarchy

Build `premium-hierarchy-diffusion` first because it matches the strongest reference image.

Tasks:

- add schema docs;
- add validator rules;
- add renderer function;
- add CSS;
- create one sample storyboard from the provided demand-level image;
- render and compare visually.

Acceptance:

- left arrow, four layers, three related tiers, three mechanisms, summary cards, and conclusion band all render;
- right tier callout, emphasized top tier, icon-led mechanisms, and summary icons render;
- layer cards are dense but readable;
- no large empty middle areas;
- all visible text is in ledger.

### Phase 2: Premium Cycle

Improve the existing cycle layout into a reference-grade layout.

Tasks:

- replace generic node cards with fixed radial slots;
- add top strip icon sizing rules;
- add output cards with icon wells;
- tune center circle and arrow geometry;
- tune clean center, segmented arrows, and node spacing;
- add visual QA for loop maturity.

Acceptance:

- no node overlap;
- cycle arrows feel intentional;
- the center stays clean while arrows and node order make the path mechanics explicit;
- visual weight is close to the GPT reference.

### Phase 3: Premium Transformation

Build a tighter transformation layout for before / mechanism / after.

Tasks:

- make middle zone more visually dominant;
- reduce empty vertical space;
- add zone insight sentences and role-specific bullet modules;
- add conversion artifact/package band;
- add relation labels on arrows;
- add essence pills and metric cards.

Acceptance:

- 3 columns fill the canvas naturally;
- middle mechanism reads as the key;
- columns no longer read as empty cards;
- artifact band shows what reusable structure the transformation produces;
- bottom conclusion is clear.

### Phase 4: Premium Process Flow

Build a tighter process layout for product walkthroughs and AI operation chains.

Tasks:

- add `premium-process-flow` schema docs;
- add validator rules for stages, stream output, checkpoints, and wide canvas;
- add renderer function and process-specific CSS;
- create one sample storyboard from the meal recognition flow screenshot;
- run HTML QA and layout alignment analysis.

Acceptance:

- four stage cards align without text overflow;
- arrows are subtle and connected to real adjacent stages;
- stream output band is visually separate from the stage spine;
- checkpoints explain trust and output visibility rather than adding noisy extra steps;
- final image reads as a workflow, not a generic card grid.

## Quality Bar

A PicTalk premium output is acceptable only when:

- logic can be understood before reading all body text;
- every major visual block has a semantic role;
- no card exists only to fill space;
- arrows connect actual concepts, not decoration;
- text is exact and readable;
- the image feels presentation-ready at first glance;
- the layout could be reused by another model without creative invention.

## Non-Goals

- Do not make PicTalk a general design tool.
- Do not rely on arbitrary image generation for final text.
- Do not copy guizang's deck system directly; reuse its low-freedom methodology.
- Do not add many generic layouts before the premium three are reference-grade.
