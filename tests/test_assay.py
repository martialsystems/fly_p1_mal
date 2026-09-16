# Copyright (c) 2026 Martial Systems LLC
from __future__ import annotations

from fly_p1_mal.assay import AssayConfig, run_assay
from fly_p1_mal.cli import main


def test_n_1000_and_unfreeze_stubbed() -> None:
    assert main(["assay", "--n", "1000", "--steps", "10"]) == 2
    assert main(["assay", "--unfreeze", "--steps", "10"]) == 2
    assert main(["assay", "--female-brain-icarus", "--steps", "10"]) == 2
    assert main(["da1-dose", "--n", "1000", "--steps", "10"]) == 2


def test_folded_mal_battery_runs() -> None:
    result = run_assay(AssayConfig(seed=1, steps=400))
    rows = {str(r["condition"]): r for r in result["conditions"]}
    assert "3d" in rows and "3b" in rows
    assert result["engine"] == "hop1_mal_gaba_folded_onto_pC1_coexpress"
    assert result["p1_term_weights"]["DA1"] == -25.9842
    assert result["p1_term_weights"]["LC10a"] == 1.8
    cva = result["cva_term"]
    assert cva["through_wcrit"] is True
    ns = result["hd_cva_ns"]
    assert ns["present"] is True
    # Fold succeeding: a -26 cVA slot rejects. Public finding is the hop-1 table.
    assert rows["3b"]["p1_mean"] < 0.0
    assert ns["cva_rejects"] is True
    assert ns["hd_on_cva_off_ns"] is True
    assert result["cva_term"]["da1_to_mal_m"]["weight"] == 0
    assert result["cva_term"]["da1_to_mal"]["weight"] == 96
