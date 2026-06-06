# Image Prompt Modes

Use image generation only when the environment actually has an image-capable model. PicTalk's default production path is deterministic HTML/CSS rendering through `scripts/render_storyboard.py`.

## Default: deterministic-text mode

Use this mode for final Chinese/English text-heavy infographics.

Goal:

1. Build the storyboard.
2. Render exact text with the locked HTML/CSS renderer.
3. Optionally generate no-text visual assets or decorative backgrounds.
4. Overlay or composite exact text deterministically.

Prompt pattern for no-text visual assets:

```text
Create a clean business infographic base with a white to very pale blue background, dark navy and primary blue visual hierarchy, rounded modules, thin blue borders, soft shadows, icon wells, arrows, and empty reserved spaces for text. Do not include any readable text, letters, numbers, symbols, pseudo-text, logos, watermarks, headers, footers, or captions. The composition should support this layout: [cycle / layer-stack / transformation / arrow-flow / timeline / matrix]. Ratio: [3:4 or 16:9].
```

Use this only as a background or visual reference. Final visible language still comes from `text_ledger`.

## Optional: image-text draft mode

Use this only when the user explicitly wants a model-generated draft image or when short labels are acceptable. This mode is useful for exploring style but risky for final Chinese text accuracy.

The prompt has four layers:

```text
[Style System] + [Locked Layout] + [Exact Text Content] + [Quality Constraints]
```

### 1. Style System

```text
Style: premium Chinese business infographic, white to very pale blue background, dark navy (#071B49) extra-bold title, primary blue (#0757D8) structural arrows and badges, semantic green (#128348), orange (#E77800), and purple (#5A2BAE) accents. Rounded rectangular modules with thin blue borders and soft shadows. Icon-first hierarchy, numbered circles, connector arrows, bottom conclusion band. Dense but breathable presentation quality. No photo background, no 3D, no cartoon, no neon, no generic SaaS dashboard.
```

### 2. Locked Layout

Choose one renderer-supported layout from `references/layouts.md`.

#### Premium Hierarchy Diffusion

```text
Layout: vertical 3:4 reference-grade Chinese business infographic. Large centered navy title and subtitle. Left side has a tall upward gradient blue arrow with the hierarchy axis label. Middle area has exactly four dense stacked layer modules; each layer has a numbered badge, icon block, title, type pill, three compact fact rows for typical behavior / core blocker / matched audience, and a blue essence pill. Right side has exactly three audience tier cards. Curved arrows connect the layer stack to the tier cards. Bottom area has a three-card mechanism chain, two summary cards, and a saturated conclusion band.
```

#### Premium Cycle System

```text
Layout: vertical 3:4 reference-grade loop infographic. Top compact process strip with three to five icon labels. Center has a large blue circular mechanism statement. Five to six numbered loop nodes surround the circle with curved arrows. Bottom has three to five output cards and a saturated conclusion band. The image should read as a system loop, not a card grid.
```

#### Premium Transformation Logic

```text
Layout: vertical 3:4 reference-grade transformation infographic. Three tall vertical zones: old state, emphasized middle mechanism, new state. Labeled arrows sit between the zones. Each zone has a badge label, icon, large heading, two to four bullets, and an essence pill. Bottom has metric cards and a saturated conclusion band.
```

#### Cycle

```text
Layout: vertical 3:4 infographic. Large centered blue circle with the core thesis. Four to six numbered rounded nodes around it in a clockwise loop. Curved thick arrows connect the nodes. Optional compact top process strip. Bottom output row and saturated blue conclusion band.
```

#### Layer Stack

```text
Layout: vertical 3:4 hierarchy infographic. Left side has a tall upward blue arrow naming the upgrade direction. Middle area has three to five stacked layer cards from low to high, each with a numbered badge, icon, heading, bullets, and a blue essence pill. Right side has two or three user/audience tier cards connected back to the layers. Bottom row explains diffusion or output mechanisms, followed by a saturated conclusion band.
```

#### Transformation

```text
Layout: two or three large zones connected left-to-right by thick arrows. Muted past/old state on the left, emphasized blue transition in the middle, final/shared state on the right. Bottom metric row and conclusion band.
```

#### Arrow Flow

```text
Layout: three to six ordered steps with visible arrows, number badges, icon wells, checkpoints, and a bottom output or conclusion band.
```

#### Timeline

```text
Layout: visible horizontal time axis with milestone dots, phase cards tied to the axis, output markers, and a bottom conclusion band.
```

#### Matrix

```text
Layout: visible grid with row and column headers. Cells contain compact text, with row color accents and one highlighted decision area. Bottom conclusion band.
```

### 3. Exact Text Content

Insert exact storyboard strings. Do not ask the model to invent labels.

```text
Title: {card.title}
Subtitle: {card.subtitle}
Top strip: {top_flow labels}
Sections:
  1. {section.heading}: {section.body joined by semicolons}. Essence: {section.footer}
  2. ...
Side tiers: {side_sections if present}
Outputs: {metrics labels and values}
Conclusion: {card.conclusion}
```

### 4. Quality Constraints

```text
Requirements: [1086x1448 vertical 3:4 / 1536x1024 wide 16:9]. Text must be legible and match the provided strings exactly; no pseudo-text, no missing Chinese strokes, no changed punctuation, no extra labels. Do not include PicTalk, internal file paths, watermarks, signatures, or renderer labels.
```

## Prompting Anti-Patterns

Avoid:

- "make it professional" without a locked layout;
- asking the image model to summarize the source;
- long paragraphs inside cards;
- unsupported layouts;
- mixing unrelated diagrams in one image;
- relying on image-text draft mode for final Chinese delivery without validation.

## If A Model Cannot Generate Images

Use the deterministic renderer:

```bash
python scripts/validate_storyboard.py storyboard.json
python scripts/render_storyboard.py storyboard.json --output-dir output --keep-html
```
