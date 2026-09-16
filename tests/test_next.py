# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from pathlib import Path

from fly_p1_mal.claims import scan_text
from fly_p1_mal.cli import main

REPO = Path(__file__).resolve().parents[1]


def test_next_closes_this_tree() -> None:
    text = (REPO / "NEXT.md").read_text(encoding="utf-8")
    assert text.startswith("# Next question\n")
    assert "This tree is closed" in text
    assert "Do not hop-3" in text
    assert "unfreeze" in text
    assert "What it is not" not in text
    assert "—" not in text
    assert scan_text(text) == []
    assert "mAL_m*" in text


def test_closed_tree_stubs_unflipped() -> None:
    assert main(["assay", "--n", "1000", "--steps", "10"]) == 2
    assert main(["assay", "--unfreeze", "--steps", "10"]) == 2
    assert main(["assay", "--female-brain-icarus", "--steps", "10"]) == 2
