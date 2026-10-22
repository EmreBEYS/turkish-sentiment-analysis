"""Dataset validation, deduplication, splitting, and compact EDA helpers."""

from __future__ import annotations

import csv
import hashlib
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

LABEL_MAP = {"Negative": "negative", "Notr": "neutral", "Positive": "positive"}
RAW_FIELDS = ("text", "label", "dataset")
PROCESSED_FIELDS = ("id", "text", "label", "source")


@dataclass(frozen=True)
class Record:
    """One normalized sentiment example."""

    text: str
    label: str
    source: str

    @property
    def key(self) -> str:
        return normalize_text(self.text).casefold()

    @property
    def row_id(self) -> str:
        return hashlib.sha256(self.key.encode("utf-8")).hexdigest()[:16]


def normalize_text(text: str) -> str:
    """Collapse whitespace without stripping Turkish characters or punctuation."""

    return re.sub(r"\s+", " ", text).strip()


def read_source_csv(path: Path) -> Iterator[Record]:
    """Read and validate a source CSV from the selected Hugging Face dataset."""

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != RAW_FIELDS:
            raise ValueError(f"Unexpected schema in {path}: {reader.fieldnames}")
        for line_number, row in enumerate(reader, start=2):
            text = normalize_text(row["text"])
            raw_label = row["label"].strip()
            source = row["dataset"].strip() or "unknown"
            if not text:
                continue
            if raw_label not in LABEL_MAP:
                raise ValueError(f"Unknown label {raw_label!r} at {path}:{line_number}")
            yield Record(text=text, label=LABEL_MAP[raw_label], source=source)


def deduplicate(records: Iterable[Record]) -> tuple[list[Record], dict[str, int]]:
    """Remove exact normalized duplicates and all label-conflicting texts."""

    by_key: dict[str, Record] = {}
    key_counts: Counter[str] = Counter()
    conflicts: set[str] = set()
    total = 0
    duplicates = 0
    for record in records:
        total += 1
        key_counts[record.key] += 1
        previous = by_key.get(record.key)
        if previous is None:
            by_key[record.key] = record
        elif previous.label == record.label:
            duplicates += 1
        else:
            conflicts.add(record.key)
    for key in conflicts:
        by_key.pop(key, None)
    return list(by_key.values()), {
        "input_rows": total,
        "same_label_duplicate_rows_removed": duplicates,
        "conflicting_texts_removed": len(conflicts),
        "conflicting_rows_removed": sum(key_counts[key] for key in conflicts),
        "clean_rows": len(by_key),
    }


def stratified_split(
    records: Sequence[Record], seed: int = 42, train_ratio: float = 0.8, val_ratio: float = 0.1
) -> dict[str, list[Record]]:
    """Create deterministic train/validation/test splits stratified by label and source."""

    if not 0 < train_ratio < 1 or not 0 < val_ratio < 1 or train_ratio + val_ratio >= 1:
        raise ValueError("Ratios must be positive and sum to less than 1")
    strata: dict[tuple[str, str], list[Record]] = defaultdict(list)
    for record in records:
        strata[(record.label, record.source)].append(record)

    splits = {"train": [], "validation": [], "test": []}
    for stratum in sorted(strata):
        group = sorted(strata[stratum], key=lambda item: item.key)
        random.Random(f"{seed}:{stratum[0]}:{stratum[1]}").shuffle(group)
        size = len(group)
        n_train = int(size * train_ratio)
        n_val = int(size * val_ratio)
        splits["train"].extend(group[:n_train])
        splits["validation"].extend(group[n_train : n_train + n_val])
        splits["test"].extend(group[n_train + n_val :])

    for name, rows in splits.items():
        random.Random(f"{seed}:{name}").shuffle(rows)
    return splits


def write_split(path: Path, records: Sequence[Record]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PROCESSED_FIELDS)
        writer.writeheader()
        for record in records:
            writer.writerow(
                {"id": record.row_id, "text": record.text, "label": record.label, "source": record.source}
            )


def counts(records: Iterable[Record], attribute: str) -> dict[str, int]:
    return dict(sorted(Counter(getattr(record, attribute) for record in records).items()))


def percentile(values: Sequence[int], fraction: float) -> int:
    ordered = sorted(values)
    if not ordered:
        return 0
    index = round((len(ordered) - 1) * fraction)
    return ordered[index]


def summarize(records: Sequence[Record]) -> dict[str, object]:
    word_lengths = [len(record.text.split()) for record in records]
    char_lengths = [len(record.text) for record in records]
    return {
        "rows": len(records),
        "labels": counts(records, "label"),
        "sources": counts(records, "source"),
        "word_length": {
            "min": min(word_lengths, default=0),
            "median": percentile(word_lengths, 0.5),
            "p95": percentile(word_lengths, 0.95),
            "max": max(word_lengths, default=0),
        },
        "character_length": {
            "min": min(char_lengths, default=0),
            "median": percentile(char_lengths, 0.5),
            "p95": percentile(char_lengths, 0.95),
            "max": max(char_lengths, default=0),
        },
    }


def assert_disjoint(splits: Mapping[str, Sequence[Record]]) -> None:
    seen: set[str] = set()
    for name in ("train", "validation", "test"):
        keys = {record.key for record in splits[name]}
        if seen.intersection(keys):
            raise ValueError(f"Text leakage detected in {name} split")
        seen.update(keys)

