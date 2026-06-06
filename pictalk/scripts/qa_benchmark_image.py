#!/usr/bin/env python3
"""Compare a rendered PicTalk PNG against a visual benchmark with coarse layout metrics."""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class ImageMetrics:
    width: int
    height: int
    bbox: tuple[int, int, int, int]
    content_width: int
    content_height: int
    left_gap: int
    top_gap: int
    right_gap: int
    bottom_gap: int
    area_coverage: float


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def estimate_background(img: Image.Image) -> tuple[int, int, int]:
    width, height = img.size
    points = [
        img.getpixel((0, 0))[:3],
        img.getpixel((width - 1, 0))[:3],
        img.getpixel((0, height - 1))[:3],
        img.getpixel((width - 1, height - 1))[:3],
        img.getpixel((width // 2, height - 1))[:3],
    ]
    return tuple(sorted(channel)[len(channel) // 2] for channel in zip(*points))


def metrics(path: Path) -> ImageMetrics:
    img = Image.open(path).convert("RGB")
    width, height = img.size
    bg = estimate_background(img)
    pixels = img.load()

    left, top, right, bottom = width, height, 0, 0
    for y in range(height):
        for x in range(width):
            rgb = pixels[x, y]
            # Treat strong color, dark text, and visible borders as content.
            if color_distance(rgb, bg) > 24 and not (rgb[0] > 246 and rgb[1] > 246 and rgb[2] > 246):
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)

    if right <= left or bottom <= top:
        bbox = (0, 0, 0, 0)
        content_width = 0
        content_height = 0
    else:
        bbox = (left, top, right, bottom)
        content_width = right - left + 1
        content_height = bottom - top + 1

    return ImageMetrics(
        width=width,
        height=height,
        bbox=bbox,
        content_width=content_width,
        content_height=content_height,
        left_gap=left,
        top_gap=top,
        right_gap=width - right - 1,
        bottom_gap=height - bottom - 1,
        area_coverage=(content_width * content_height) / (width * height),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare candidate PNG against benchmark PNG")
    parser.add_argument("benchmark", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--max-extra-bottom-gap", type=int, default=80)
    parser.add_argument("--max-extra-edge-gap", type=int, default=40)
    parser.add_argument("--min-coverage-ratio", type=float, default=0.94)
    args = parser.parse_args()

    for path in [args.benchmark, args.candidate]:
        if not path.exists():
            print(f"File not found: {path}", file=sys.stderr)
            return 2

    bench = metrics(args.benchmark)
    cand = metrics(args.candidate)
    errors: list[str] = []

    if (cand.width, cand.height) != (bench.width, bench.height):
        errors.append(f"size mismatch: benchmark={bench.width}x{bench.height}, candidate={cand.width}x{cand.height}")

    allowed_bottom_gap = bench.bottom_gap + args.max_extra_bottom_gap
    if cand.bottom_gap > allowed_bottom_gap:
        errors.append(f"bottom whitespace too large: benchmark={bench.bottom_gap}px, candidate={cand.bottom_gap}px, allowed<={allowed_bottom_gap}px")

    for edge in ["left_gap", "top_gap", "right_gap"]:
        bench_gap = getattr(bench, edge)
        cand_gap = getattr(cand, edge)
        allowed_gap = bench_gap + args.max_extra_edge_gap
        if cand_gap > allowed_gap:
            errors.append(f"{edge} too large: benchmark={bench_gap}px, candidate={cand_gap}px, allowed<={allowed_gap}px")

    min_coverage = bench.area_coverage * args.min_coverage_ratio
    if cand.area_coverage < min_coverage:
        errors.append(f"content coverage too low: benchmark={bench.area_coverage:.3f}, candidate={cand.area_coverage:.3f}, required>={min_coverage:.3f}")

    print("Benchmark metrics:")
    print(f"- size: {bench.width}x{bench.height}")
    print(f"- bbox: {bench.bbox}")
    print(f"- gaps: left={bench.left_gap}px, top={bench.top_gap}px, right={bench.right_gap}px, bottom={bench.bottom_gap}px")
    print(f"- bottom_gap: {bench.bottom_gap}px")
    print(f"- area_coverage: {bench.area_coverage:.3f}")
    print("Candidate metrics:")
    print(f"- size: {cand.width}x{cand.height}")
    print(f"- bbox: {cand.bbox}")
    print(f"- gaps: left={cand.left_gap}px, top={cand.top_gap}px, right={cand.right_gap}px, bottom={cand.bottom_gap}px")
    print(f"- bottom_gap: {cand.bottom_gap}px")
    print(f"- area_coverage: {cand.area_coverage:.3f}")

    if errors:
        print("PicTalk benchmark QA failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PicTalk benchmark QA passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
