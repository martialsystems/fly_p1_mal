# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

from fly_p1_mal.claims import scan_text

REPO = Path(__file__).resolve().parents[1]
LOCK = REPO / "logs" / "p1_mal_s1.json"
QUESTION = (
    "Does hop-1 GABA from annotated mAL onto the same 88 cells pull the "
    "cVA term through W_crit ≈ -1.54, and only then does HD-on / cVA-off "
    "become necessary and sufficient?"
)


def test_readme_question_first() -> None:
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert text.startswith("# fly_p1_mal\n")
    body = text.split("\n", 1)[1].lstrip()
    assert body.startswith(QUESTION)
    assert "What it is not" not in text
    assert "—" not in text
    assert scan_text(text) == []
    assert "139,255" in text
    assert "166,691" in text
    assert ".venv/bin/python -m pytest" in text
    assert "malforge/" in text
    assert "https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178" in text
    assert "@45aa064" in text
    assert "12835f747d6360781f3cc7f91f243178" in text
    desc = (REPO / "description.txt").read_text(encoding="utf-8")
    assert QUESTION in desc
    assert "—" not in desc
    assert scan_text(desc) == []


def test_lock_numbers_in_readme() -> None:
    data = json.loads(LOCK.read_text(encoding="utf-8"))
    text = (REPO / "README.md").read_text(encoding="utf-8")
    assert data["question"] == QUESTION
    ns = data["hd_cva_ns"]
    assert ns["hd_on_cva_off_ns"] is True
    assert data["cva_term"]["through_wcrit"] is True
    rows = {str(r["condition"]): r for r in data["conditions"]}
    assert str(rows["3"]["p1_mean"]) in text
    assert str(rows["3b"]["p1_mean"]) in text
    assert str(rows["3d"]["p1_mean"]) in text
    assert "-25.9842" in text
    assert "-8810" in text
    dose = json.loads((REPO / "logs" / "p1_da1_dose_s1.json").read_text())
    assert str(dose["critical_weight"]["w_p1_da1"]) in text
    assert str(dose["default_w_p1_da1"]) in text
    footer = "[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)"
    assert footer in text
