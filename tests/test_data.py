from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from turkish_sentiment.data import (  # noqa: E402
    Record,
    assert_disjoint,
    deduplicate,
    normalize_text,
    stratified_split,
)


class DataPipelineTests(unittest.TestCase):
    def test_normalize_text_preserves_turkish_characters(self) -> None:
        self.assertEqual(normalize_text("  Ürün\nçok\tiyi  "), "Ürün çok iyi")

    def test_deduplicate_drops_conflicting_labels(self) -> None:
        rows = [
            Record("Harika ürün", "positive", "reviews"),
            Record(" harika   ürün ", "positive", "reviews"),
            Record("Harika ürün", "negative", "reviews"),
            Record("Normal", "neutral", "wiki"),
        ]
        clean, audit = deduplicate(rows)
        self.assertEqual(clean, [Record("Normal", "neutral", "wiki")])
        self.assertEqual(audit["same_label_duplicate_rows_removed"], 1)
        self.assertEqual(audit["conflicting_texts_removed"], 1)
        self.assertEqual(audit["conflicting_rows_removed"], 3)

    def test_split_is_deterministic_and_leakage_free(self) -> None:
        rows = [
            Record(f"metin {label} {index}", label, "source")
            for label in ("negative", "neutral", "positive")
            for index in range(30)
        ]
        first = stratified_split(rows, seed=42)
        second = stratified_split(rows, seed=42)
        self.assertEqual(
            {name: [row.row_id for row in values] for name, values in first.items()},
            {name: [row.row_id for row in values] for name, values in second.items()},
        )
        self.assertEqual({name: len(values) for name, values in first.items()}, {"train": 72, "validation": 9, "test": 9})
        assert_disjoint(first)


if __name__ == "__main__":
    unittest.main()

