#!/usr/bin/env python3
"""Deconstruct rendered infographic PNGs into coarse alignment bands.

The script is intentionally lightweight: it does not try to understand text.
It measures where visible content lives so sparse, off-axis, or mis-banded
layouts can be compared against a benchmark.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

from PIL import Image


@dataclass
class Segment:
    start: int
    end: int
    size: int
    peak_density: float
    mean_density: float


@dataclass
class LayoutAnalysis:
    path: str
    width: int
    height: int
    bbox: tuple[int, int, int, int]
    gaps: dict[str, int]
    content_coverage: float
    horizontal_bands: list[Segment]
    vertical_columns: list[Segment]
    row_density_peaks: list[int]
    column_density_peaks: list[int]


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


def moving_average(values: list[float], radius: int) -> list[float]:
    if not values:
        return []
    result: list[float] = []
    total = 0.0
    queue: list[float] = []
    window = radius * 2 + 1
    padded = [values[0]] * radius + values + [values[-1]] * radius
    for value in padded:
        queue.append(value)
        total += value
        if len(queue) > window:
            total -= queue.pop(0)
        if len(queue) == window:
            result.append(total / window)
    return result


def segments_from_density(values: list[float], threshold: float, min_size: int, merge_gap: int) -> list[Segment]:
    raw: list[tuple[int, int]] = []
    start: int | None = None
    for index, value in enumerate(values):
        if value >= threshold and start is None:
            start = index
        elif value < threshold and start is not None:
            raw.append((start, index - 1))
            start = None
    if start is not None:
        raw.append((start, len(values) - 1))

    merged: list[tuple[int, int]] = []
    for seg_start, seg_end in raw:
        if not merged or seg_start - merged[-1][1] > merge_gap:
            merged.append((seg_start, seg_end))
        else:
            merged[-1] = (merged[-1][0], seg_end)

    result = []
    for seg_start, seg_end in merged:
        if seg_end - seg_start + 1 < min_size:
            continue
        segment_values = values[seg_start : seg_end + 1]
        result.append(
            Segment(
                start=seg_start,
                end=seg_end,
                size=seg_end - seg_start + 1,
                peak_density=max(segment_values),
                mean_density=sum(segment_values) / len(segment_values),
            )
        )
    return result


def top_peaks(values: list[float], count: int = 5, min_distance: int = 72) -> list[int]:
    order = sorted(range(len(values)), key=lambda i: values[i], reverse=True)
    peaks: list[int] = []
    for index in order:
        if all(abs(index - peak) >= min_distance for peak in peaks):
            peaks.append(index)
        if len(peaks) >= count:
            break
    return sorted(peaks)


def analyze(path: Path) -> LayoutAnalysis:
    img = Image.open(path).convert("RGB")
    width, height = img.size
    bg = estimate_background(img)
    pixels = img.load()

    row_counts = [0] * height
    col_counts = [0] * width
    left, top, right, bottom = width, height, 0, 0

    for y in range(height):
        for x in range(width):
            rgb = pixels[x, y]
            is_content = color_distance(rgb, bg) > 24 and not (rgb[0] > 246 and rgb[1] > 246 and rgb[2] > 246)
            if not is_content:
                continue
            row_counts[y] += 1
            col_counts[x] += 1
            left = min(left, x)
            top = min(top, y)
            right = max(right, x)
            bottom = max(bottom, y)

    if right <= left or bottom <= top:
        bbox = (0, 0, 0, 0)
        gaps = {"left": width, "top": height, "right": width, "bottom": height}
        coverage = 0.0
    else:
        bbox = (left, top, right, bottom)
        gaps = {"left": left, "top": top, "right": width - right - 1, "bottom": height - bottom - 1}
        coverage = ((right - left + 1) * (bottom - top + 1)) / (width * height)

    row_density = moving_average([count / width for count in row_counts], radius=9)
    col_density = moving_average([count / height for count in col_counts], radius=9)

    return LayoutAnalysis(
        path=str(path),
        width=width,
        height=height,
        bbox=bbox,
        gaps=gaps,
        content_coverage=coverage,
        horizontal_bands=segments_from_density(row_density, threshold=0.02, min_size=24, merge_gap=18),
        vertical_columns=segments_from_density(col_density, threshold=0.015, min_size=24, merge_gap=18),
        row_density_peaks=top_peaks(row_density),
        column_density_peaks=top_peaks(col_density),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze alignment and content bands in rendered infographic PNGs")
    parser.add_argument("images", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of readable text")
    args = parser.parse_args()

    analyses = []
    for image_path in args.images:
        if not image_path.exists():
            raise SystemExit(f"File not found: {image_path}")
        analyses.append(analyze(image_path))

    if args.json:
        print(json.dumps([asdict(item) for item in analyses], ensure_ascii=False, indent=2))
        return 0

    for item in analyses:
        print(f"\n{item.path}")
        print(f"- size: {item.width}x{item.height}")
        print(f"- bbox: {item.bbox}")
        print(f"- gaps: {item.gaps}")
        print(f"- coverage: {item.content_coverage:.3f}")
        print("- horizontal bands:")
        for band in item.horizontal_bands:
            print(f"  {band.start:4d}-{band.end:<4d} size={band.size:<4d} mean={band.mean_density:.3f} peak={band.peak_density:.3f}")
        print("- vertical columns:")
        for column in item.vertical_columns:
            print(f"  {column.start:4d}-{column.end:<4d} size={column.size:<4d} mean={column.mean_density:.3f} peak={column.peak_density:.3f}")
        print(f"- row peaks: {item.row_density_peaks}")
        print(f"- column peaks: {item.column_density_peaks}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
