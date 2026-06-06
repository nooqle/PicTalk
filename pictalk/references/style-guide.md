# PicTalk Style Guide

Use this guide to recreate the style of the sample images: clean Chinese/English business infographics that are dense enough for strategy discussion and polished enough for presentation slides.

The workflow name must not appear in final images as a visible label, watermark, eyebrow, footer, or title unless the user explicitly requests branding.

## Canvas

- Default slide: `1536x1024` or `16:9`.
- Vertical card: `1086x1448` or `3:4`.
- Wide summary: `1693x929` or close to `16:9`.
- Keep 48-72 px outer margins on 1536-wide canvases; scale proportionally.
- Use a white to very pale blue background. Avoid photographic backgrounds.

## Palette

Default semantic palette:

| Role | Hex | Use |
| --- | --- | --- |
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

Customization rule: preserve contrast and assign colors by meaning, not decoration. If the user supplies a palette, map it into the semantic roles above. Keep one dark text color and one high-contrast conclusion-band color.

## Typography

- Use real text rendered with a CJK-capable sans font: PingFang SC, Noto Sans CJK, Source Han Sans, Microsoft YaHei, or a similar system font.
- Main title: extra-bold, centered, 58-82 px on a 1536-wide canvas.
- Subtitle: medium weight, 26-36 px, muted navy or gray.
- Card headings: bold, 28-42 px.
- Body text: 22-30 px. Avoid long paragraphs.
- Label pills: bold, 22-30 px, white text on strong color or dark text on pale fill.
- Do not use negative letter spacing. Do not use decorative or handwritten fonts.

## Components

- Title block: large centered title with selective color emphasis on 1-3 key words.
- Subtitle line: short explanatory sentence below title, sometimes flanked by thin horizontal rules.
- Modules: rounded rectangles with 8-18 px radius, thin colored border, white or pale fill, subtle shadow.
- Icon wells: circular or rounded squares, usually pale fill with a bold monochrome icon.
- Number badges: filled circles near the top-left or top-center of sections.
- Arrows: thick blue arrows for primary direction; thin dotted arrows for mapping or feedback.
- Conclusion band: full-width saturated blue bar near the bottom with a shield/target/rocket icon and one strong takeaway.
- Mini-metric row: 3-5 compact boxes under a conclusion band when the card needs measurable outputs.
- Structural marks: timelines, arrows, ladders, matrices, swimlanes, funnels, loops, brackets, axes, and connectors.
- Premium hierarchy components: left gradient upgrade rail, four semantic layer modules, right tier panel with callout and emphasized top tier, curved connectors, icon-led mechanism chain, summary card row.
- Premium transformation components: three tall zones, emphasized middle mechanism, vertical relation labels, essence pills, bottom metric row.

Cards are local containers. They are not the default composition. Every image needs a primary diagram structure that makes the logic visible before the reader finishes reading the text.

## Layout Families

### Premium Hierarchy Diffusion

Use when a single image must explain hierarchy, maturity, demand levels, capability stacks, or "high brings low" logic.

- 3:4 canvas at `1086x1448`.
- Left gradient rail must name the upward axis.
- Middle stack must have exactly four semantic layers.
- Right side must have exactly three related tiers.
- Add a short `tier_callout` when the right side needs a benchmark-like "why this tier matters" emphasis.
- Bottom must include three mechanisms, 2-3 summary cards, and a conclusion band.

### Premium Cycle System

Use for a reference-grade loop or flywheel.

- Top flow strip with 3-5 icon labels.
- Large center circle with a short mechanism phrase.
- Double-ring path with 5-6 nodes attached to the loop.
- Inner phase chips around the center for naming, validating, compressing, or writing back.
- Bottom output row and conclusion band.

### Premium Transformation Logic

Use for old state -> mechanism -> new state.

- Three tall zones, with the middle mechanism visually emphasized.
- Each zone must include an `insight` sentence so it reads as a state judgment, not an empty card.
- Relation labels must be visible on the arrows.
- Each zone needs an essence pill.
- Reference-grade cards need a `conversion_artifact` band that shows what reusable asset the flow produces.
- Bottom metric row and conclusion band close the argument.

### Transformation

Use for old model -> new model.

- Left module in gray or muted color for `past`.
- Right module in blue for `present`.
- Large arrow between them.
- Bottom conclusion band explaining the changed value path.

### Comparison Columns

Use for role split, responsibility split, or three operating layers.

- Two or three tall modules.
- Each module has icon, heading, label pill, responsibility sentence, metric bullets, and bottom essence box.
- Use green/orange/purple for distinct columns.

### Layer Stack

Use for maturity, user tiers, demand levels, or capability levels.

- Vertical ladder on one side with increasing intensity.
- Each layer has number badge, icon, title, bullets, and a short "essence" strip.
- Use arrows from layers to corresponding audience tiers when useful.

### Cycle/Flywheel

Use for operating loops and repeated learning.

- Central circular thesis.
- 5-6 surrounding cards with numbered badges.
- Curved arrows around the loop.
- Bottom row for key outputs.

### Responsibility Map

Use for owners, DRIs, and shared metrics.

- Left and right owner columns.
- Center thin column for shared interfaces or mapping steps.
- Bottom shared-goal band with metric cards.

### Timeline

Use for agendas, version sequences, incident histories, and delivery plans.

- Make the axis visible.
- Use tick labels and milestone nodes.
- Show outputs at the end of each time box.
- Use arrows to show progression.

### Premium Process Flow

Use for product journeys or AI workflows where the reader must see what the user does, what the system does, and how the output arrives.

- Keep the top spine to exactly four main stages.
- Arrows should sit between stage cards and point to real next actions.
- Put streaming or progressive output in a dedicated band, not as a fourth-row paragraph.
- Use checkpoints for trust, visibility, and output quality rather than extra steps.
- Avoid wrapping long mixed English/Chinese labels inside narrow cards; shorten the local label or use the subtitle.

### Matrix

Use for categories crossed with boundaries, decisions, evidence status, owners, or priorities.

- Rows and columns must be visually apparent.
- Use color accents by row or group.
- Highlight disagreements, gaps, or priority cells.

### Funnel

Use for evidence filtering, case qualification, or narrowing many issues into a few decisions.

- Wide input at top or left.
- Gates for criteria.
- Narrow output bucket for selected cases or actions.

### Swimlane

Use for cross-team workflows, owner splits, or handoffs.

- One lane per actor or workgroup.
- Arrows crossing lanes.
- Decision gates or escalation points.

## Density Rules

- A dense card is acceptable if hierarchy is obvious.
- Every section needs a visual anchor: icon, number, or colored heading.
- Use bullets for scan speed. Limit one bullet to one thought.
- Keep the strongest takeaway in a bottom band or large central node.
- Remove any text that does not help the audience retell the logic.
- For a multi-image set, do not repeat the same primary layout across all images.
- If the image title implies time, hierarchy, flow, ownership, or filtering, the visible structure must show that relation.

## Avoid

- AI-generated gibberish text.
- Overly decorative gradients, bokeh, or stock imagery.
- Long prose blocks.
- Many unrelated colors.
- Thin low-contrast text.
- 3D icons, cartoon mascots, or heavy illustration styles unless the user explicitly asks.
- Visible `PicTalk`, skill names, renderer labels, internal source paths, or process labels.
- Pure card mosaics when the logic requires a timeline, hierarchy, flow, map, matrix, or loop.
