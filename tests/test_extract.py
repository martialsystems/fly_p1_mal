# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PARENT_W_CRIT = -1.539


def test_mal_gaba_folded_into_cva_term_on_parent_scale() -> None:
    ext = json.loads((REPO / "data" / "templates" / "extract.json").read_text())
    assert ext["kind"] == "hop1_mal_gaba_folded_onto_pC1_coexpress"
    assert ext["n_P1"] == 88
    assert ext["mAL_definition"] == "type startswith mAL"
    assert ext["named_signed_onto_P1"]["DA1"] == 62
    assert ext["named_signed_onto_P1"]["LC10a"] == 606
    assert ext["named_signed_onto_P1"]["ppk23"] == 0
    assert ext["named_signed_onto_P1"]["mAL_GABA"] == -8810
    assert ext["scale_divisor"] == 336.6666666666667
    assert ext["scale_setter"] == "LC10a_parent"
    cva = ext["cva_term"]
    assert cva["combined_signed"] == 62 + (-8810)
    assert cva["W"] == -25.9842
    assert cva["parent_w_crit"] == PARENT_W_CRIT
    assert cva["through_wcrit"] is True
    assert cva["da1_to_mal_m"]["weight"] == 0
    assert cva["da1_to_mal"]["weight"] == 96
    spec = json.loads((REPO / "data" / "templates" / "male_p1.json").read_text())
    assert spec["W"][6][2] == -25.9842
    assert spec["W"][6][5] == 1.8
    assert spec["W"][6][3] == 0.0
    assert spec["default_w_p1_da1"] == -25.9842
    assert spec["parent_n"] == 166691
    assert spec["kind"] == "hop1_mal_gaba_folded_onto_pC1_coexpress"


def test_extract_does_not_open_hop3() -> None:
    ext = json.loads((REPO / "data" / "templates" / "extract.json").read_text())
    hops = ext["hops"]
    assert "hop3" not in json.dumps(ext)
    assert "mAL_GABA_to_P1" in hops
    assert "DA1_PN_to_mAL" in hops
