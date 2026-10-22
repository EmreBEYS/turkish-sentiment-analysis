"""Prepare leakage-safe splits and generate dependency-free EDA artifacts."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from itertools import chain
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from turkish_sentiment.data import (  # noqa: E402
    assert_disjoint,
    counts,
    deduplicate,
    read_source_csv,
    stratified_split,
    summarize,
    write_split,
)


def write_distribution(path: Path, splits: dict[str, list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["split", "label", "count"])
        for split, records in splits.items():
            for label, count in counts(records, "label").items():
                writer.writerow([split, label, count])


def write_svg(path: Path, label_counts: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    colors = {"negative": "#d95f5f", "neutral": "#6d87a8", "positive": "#4b9b70"}
    maximum = max(label_counts.values())
    bars = []
    for index, label in enumerate(("negative", "neutral", "positive")):
        count = label_counts[label]
        height = round(260 * count / maximum)
        x = 85 + index * 170
        y = 330 - height
        bars.append(
            f'<rect x="{x}" y="{y}" width="110" height="{height}" fill="{colors[label]}" rx="5"/>'
            f'<text x="{x + 55}" y="{y - 10}" text-anchor="middle">{count:,}</text>'
            f'<text x="{x + 55}" y="360" text-anchor="middle">{label}</text>'
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">'
        '<rect width="600" height="400" fill="#ffffff"/>'
        '<text x="300" y="35" text-anchor="middle" font-size="20">Sınıf dağılımı (temiz veri)</text>'
        '<line x1="55" y1="330" x2="550" y2="330" stroke="#333"/>'
        '<g font-family="Arial, sans-serif" font-size="14">'
        + "".join(bars)
        + "</g></svg>"
    )
    path.write_text(svg, encoding="utf-8")


def write_markdown(path: Path, report: dict) -> None:
    clean = report["clean_data"]
    audit = report["cleaning"]
    split_rows = report["splits"]
    lines = [
        "# EDA ve veri bölme özeti",
        "",
        "Bu rapor `python scripts/prepare_data.py` ile yeniden üretildi.",
        "",
        "## Temizlik",
        "",
        f"- Ham satır: {audit['input_rows']:,}",
        f"- Aynı etiketli tekrar satırı: {audit['same_label_duplicate_rows_removed']:,}",
        f"- Çelişkili etiketi olan benzersiz metin: {audit['conflicting_texts_removed']:,}",
        f"- Çelişki nedeniyle çıkarılan toplam satır: {audit['conflicting_rows_removed']:,}",
        f"- Temiz benzersiz satır: {audit['clean_rows']:,}",
        "",
        "## Genel dağılım",
        "",
        "| Sınıf | Adet | Oran |",
        "|---|---:|---:|",
    ]
    total = clean["rows"]
    for label, count in clean["labels"].items():
        lines.append(f"| {label} | {count:,} | {count / total:.1%} |")
    lines.extend(
        [
            "",
            "Nötr örneklerin büyük bölümü Wikipedia kaynaklıdır; model karşılaştırmasında kaynak kısayolları ve sınıf dengesizliği ayrıca izlenmelidir.",
            "",
            "## Uzunluk",
            "",
            f"Kelime sayısı medyanı {clean['word_length']['median']}, p95 değeri {clean['word_length']['p95']}, en yüksek değer {clean['word_length']['max']}.",
            "",
            "## Bölmeler",
            "",
            "| Bölme | Satır | negative | neutral | positive |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for name in ("train", "validation", "test"):
        item = split_rows[name]
        labels = item["labels"]
        lines.append(
            f"| {name} | {item['rows']:,} | {labels['negative']:,} | {labels['neutral']:,} | {labels['positive']:,} |"
        )
    lines.extend(
        [
            "",
            "Bölme %80/%10/%10 oranında, sabit tohumla ve `(label, source)` katmanlarına göre yapıldı. Aynı normalize metin iki farklı bölmede bulunamaz.",
            "",
            "![Sınıf dağılımı](figures/class_distribution.svg)",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/processed"))
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    paths = [args.raw_dir / "source_train.csv", args.raw_dir / "source_test.csv"]
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing source files: {', '.join(missing)}")

    records, audit = deduplicate(chain.from_iterable(read_source_csv(path) for path in paths))
    splits = stratified_split(records, seed=args.seed)
    assert_disjoint(splits)
    for name, rows in splits.items():
        write_split(args.output_dir / f"{name}.csv", rows)

    report = {
        "dataset": "winvoker/turkish-sentiment-analysis-dataset",
        "license": "CC BY-SA 4.0",
        "seed": args.seed,
        "cleaning": audit,
        "clean_data": summarize(records),
        "splits": {name: summarize(rows) for name, rows in splits.items()},
    }
    args.reports_dir.mkdir(parents=True, exist_ok=True)
    (args.reports_dir / "eda_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_distribution(args.reports_dir / "class_distribution.csv", splits)
    write_svg(args.reports_dir / "figures" / "class_distribution.svg", report["clean_data"]["labels"])
    write_markdown(Path("docs/eda.md"), report)
    print(json.dumps({"clean_rows": len(records), "splits": {k: len(v) for k, v in splits.items()}}, indent=2))


if __name__ == "__main__":
    main()

