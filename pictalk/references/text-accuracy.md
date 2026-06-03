# Text Accuracy Rules

PicTalk images often contain Chinese, English, acronyms, numbers, percentages, arrows, and punctuation. Treat text accuracy as part of the deliverable.

## Core Rule

Never rely on an image generation model to create final human-language text. Use deterministic text layers.

Acceptable:

- HTML/CSS text captured to PNG.
- SVG `<text>` elements.
- PPTX text boxes.
- Canvas text drawn from exact strings.
- Design-tool text layers exported to image.

Not acceptable for final output:

- A prompt such as "draw this Chinese title in the image".
- Raster text embedded in a generated background.
- Manual retyping during final export without checking against the storyboard.

## Text Ledger Workflow

1. Build `text_ledger` in the storyboard.
2. Render visible text only from exact ledger strings or exact duplicate fields.
3. After rendering, extract text from the source artifact when possible:
   - HTML/SVG: inspect DOM or file text.
   - PPTX: inspect slide text.
   - PDF/PNG: use OCR as a secondary check if available.
4. Compare extracted text to `text_ledger`.
5. Manually inspect final PNGs for line breaks, cropped characters, punctuation, and numeric values.

## High-Risk Tokens

Check these manually:

- Chinese proper nouns and names.
- English acronyms: `AI`, `DRI`, `NPS`, `ABO`, `NSR`.
- Percentages and decimals.
- Dates and version numbers.
- Formula-like lines using `=`, `->`, `→`, `/`, `×`.
- Full-width and half-width punctuation.
- Quotation marks around key concepts.

## Prompting Pattern When Image Generation Is Needed

Use image generation only for non-text elements:

```text
Generate a clean, white-background business infographic illustration asset with blue rounded modules, arrow motifs, and empty space reserved for text. Do not include any readable text, letters, numbers, symbols, pseudo-text, or logos.
```

Then overlay all text with a deterministic renderer.

## Final QA Checklist

- Every visible string appears in `text_ledger`.
- No generated pseudo-text remains in the image.
- Text is not cropped or hidden by icons, arrows, or cards.
- Chinese line breaks do not split terms awkwardly.
- Contrast remains readable on light fills and saturated conclusion bars.
- The final image can be explained verbally in 20 seconds.
