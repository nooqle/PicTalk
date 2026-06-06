# Text Accuracy Rules

PicTalk images often contain Chinese, English, acronyms, numbers, percentages, arrows, and punctuation. Treat text accuracy as part of the deliverable.

## Core Rule

Every visible text string must originate from the storyboard `text_ledger`. The default final delivery path is deterministic text rendering with HTML/CSS, SVG, PPTX, or another real text layer. Do not rely on raster-generated text for final Chinese, numbers, formulas, labels, or dense infographic copy when a deterministic renderer is available.

## Rendering Paths

### Deterministic Rendering (Primary)

When using `scripts/render_storyboard.py` or another deterministic renderer:

- Text is rendered from storyboard fields that are also listed in `text_ledger`.
- Premium layouts also render their built-in semantic labels, such as `表现线索`, `关键阻碍`, `适配场景`, default row titles such as `扩散机制` / `结构判断`, and numeric badges. Include these strings in `text_ledger` unless you override them through explicit fields such as `field_labels`.
- After rendering, inspect for cropped characters, CSS overflow, font loading failures, line break issues, and low contrast.
- HTML/SVG/PPTX rendering should not produce pseudo-text, but layout issues can hide or overlap content.

### Image Generation (Optional)

When using an image-capable model:

- Prefer `deterministic-text` mode: ask the image model for a no-text visual base, then overlay exact text with the deterministic renderer.
- Use `image-text` mode only for short-label drafts or when the user accepts text risk.
- If an image model draws final text, visually inspect every string against the ledger and use OCR as a secondary check when available.
- If the model corrupts Chinese characters, punctuation, arrows, formulas, or acronyms, switch that card to deterministic text rendering.

## Text Ledger Workflow

1. Build `text_ledger` in the storyboard.
2. Render visible text only from exact ledger strings or exact duplicate fields.
3. After rendering, validate text:
   - HTML/SVG: inspect DOM or file text when possible.
   - PPTX/PDF: inspect extractable text when possible.
   - PNG or image-generated draft: use OCR as a secondary check if available.
4. Compare extracted text to `text_ledger`.
5. Manually inspect final PNGs for line breaks, cropped characters, punctuation, and numeric values.

## High-Risk Tokens

Check these manually regardless of rendering method:

- Chinese proper nouns and names.
- English acronyms: `AI`, `DRI`, `NPS`, `ABO`, `NSR`.
- Percentages and decimals.
- Dates and version numbers.
- Formula-like lines using `=`, `->`, `→`, `/`, `×`.
- Full-width and half-width punctuation.
- Quotation marks around key concepts.

## Prompting Pattern for Optional Image Generation

When generating a visual base, avoid text entirely:

```text
Create a clean business infographic base with blue rounded modules, arrows, icon wells, and empty reserved areas for text. Do not include any readable text, letters, numbers, symbols, pseudo-text, logos, watermarks, captions, or labels.
```

If the user explicitly wants an image-text draft, include exact `text_ledger` entries and validate the result manually. See [image-prompts.md](image-prompts.md) for both modes.

## Final QA Checklist

- Every visible string appears in `text_ledger`.
- No generated pseudo-text or gibberish remains in the image.
- Text is not cropped or hidden by icons, arrows, or cards.
- Chinese line breaks do not split terms awkwardly.
- Contrast remains readable on light fills and saturated conclusion bars.
- The final image can be explained verbally in 20 seconds.
