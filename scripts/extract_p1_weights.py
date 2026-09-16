#!/usr/bin/env python3
# Copyright (c) 2026 Martial Systems LLC
"""Hop-1 GABA from annotated mAL onto the same 88 pC1 coexpress cells.

Fold that signed GABA into W[P1, DA1] on the parent LC10a scale. Same 11-cell
row as fly_p1_sign @45aa064. Not hop-3. Not a crowd of LH inhibitors.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data-raw"
OUT = ROOT / "data" / "templates"
PROV = ROOT / "data" / "templates" / "provenance.lock.json"

EXC = {"acetylcholine", "glutamate", "octopamine", "serotonin"}
INH = {"gaba"}
TARGET_MAX = 1.8
# Parent LC10a signed 606 / 1.8. Do not let mAL steal the scale.
PARENT_SCALE = 336.6666666666667
PARENT_W_CRIT = -1.539
PARENT_SHA = "45aa064"
PARENT_LC10A_SIGNED = 606
PARENT_DA1_SIGNED = 62

LOCK_SHA = {
    "annotations.feather": "2177e246113e4cfbf1e7772ec37c6da1955ff22e8063d0b1f833101f99a9a3b2",
    "neurotransmitters.feather": "95c9289220663abeb3409f3ad9e5a7f8a53f8093f5139d15502cd08da8879621",
    "edges.feather": "5c536423a62a688e59e7b441f9c04d6272c9a1f017e35814cf561f8c275d9e9e",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nt_sign(name: object) -> int:
    if name in EXC:
        return 1
    if name in INH:
        return -1
    return 0


def signed_hop1(
    w: pd.DataFrame,
    nt_s: pd.Series,
    pre: set[int],
    post: set[int],
    *,
    gaba_only: bool = False,
) -> dict:
    h = w[w["body_pre"].isin(pre) & w["body_post"].isin(post)]
    if h.empty:
        return {
            "n_edges": 0,
            "weight": 0,
            "signed": 0,
            "n_pre": 0,
            "n_post": 0,
            "nt": {},
        }
    nt = h["body_pre"].map(nt_s)
    if gaba_only:
        keep = nt.eq("gaba")
        h = h[keep]
        nt = h["body_pre"].map(nt_s)
        if h.empty:
            return {
                "n_edges": 0,
                "weight": 0,
                "signed": 0,
                "n_pre": 0,
                "n_post": 0,
                "nt": {},
            }
    sign = nt.map(nt_sign)
    return {
        "n_edges": int(len(h)),
        "weight": int(h["weight"].sum()),
        "signed": int((h["weight"] * sign).sum()),
        "n_pre": int(h["body_pre"].nunique()),
        "n_post": int(h["body_post"].nunique()),
        "nt": {str(k): int(v) for k, v in h.groupby(nt)["weight"].sum().items()},
    }


def main() -> None:
    for name, expect in LOCK_SHA.items():
        got = sha256(RAW / name)
        if got != expect:
            raise SystemExit(f"{name} sha256 {got} != {expect}")

    ann = pd.read_feather(RAW / "annotations.feather")
    nt = pd.read_feather(RAW / "neurotransmitters.feather").rename(columns={"body": "bodyId"})
    w = pd.read_feather(RAW / "edges.feather")
    type_s = ann["type"].fillna("").astype(str)
    fru = ann["fruDsx"].fillna("").astype(str)
    rt = ann["receptorType"].fillna("").astype(str)
    body = ann["bodyId"].astype("int64")
    sets = {
        "P1_coexpress": set(body[type_s.str.startswith("pC1_") & fru.str.startswith("coexpress")].astype(int)),
        "pC1_all": set(body[type_s.str.startswith("pC1_")].astype(int)),
        "ORN_DA1": set(body[type_s.eq("ORN_DA1")].astype(int)),
        "ORN_VA1v": set(body[type_s.eq("ORN_VA1v")].astype(int)),
        "VA1v_PN": set(body[type_s.isin(["VA1v_adPN", "VA1v_vPN"])].astype(int)),
        "DA1_PN": set(body[type_s.isin(["DA1_lPN", "DA1_vPN"])].astype(int)),
        "LC10a": set(body[type_s.eq("LC10a")].astype(int)),
        "ppk23": set(body[rt.eq("putative_ppk23")].astype(int)),
        "mAL": set(body[type_s.str.startswith("mAL")].astype(int)),
        "mAL_m": set(body[type_s.str.startswith("mAL_m")].astype(int)),
    }
    nt_s = nt.set_index("bodyId")["consensus_nt"]
    P1 = sets["P1_coexpress"]
    if len(P1) != 88:
        raise SystemExit(f"P1_coexpress {len(P1)} != 88")
    hops = {
        "VA1v_PN_to_P1": signed_hop1(w, nt_s, sets["VA1v_PN"], P1),
        "DA1_PN_to_P1": signed_hop1(w, nt_s, sets["DA1_PN"], P1),
        "LC10a_to_P1": signed_hop1(w, nt_s, sets["LC10a"], P1),
        "ppk23_to_P1": signed_hop1(w, nt_s, sets["ppk23"], P1),
        "ORN_VA1v_to_P1": signed_hop1(w, nt_s, sets["ORN_VA1v"], P1),
        "ORN_DA1_to_P1": signed_hop1(w, nt_s, sets["ORN_DA1"], P1),
        "ORN_DA1_to_DA1_PN": signed_hop1(w, nt_s, sets["ORN_DA1"], sets["DA1_PN"]),
        "ORN_VA1v_to_VA1v_PN": signed_hop1(w, nt_s, sets["ORN_VA1v"], sets["VA1v_PN"]),
        "mAL_GABA_to_P1": signed_hop1(w, nt_s, sets["mAL"], P1, gaba_only=True),
        "mAL_signed_to_P1": signed_hop1(w, nt_s, sets["mAL"], P1),
        "mAL_m_GABA_to_P1": signed_hop1(w, nt_s, sets["mAL_m"], P1, gaba_only=True),
        "DA1_PN_to_mAL": signed_hop1(w, nt_s, sets["DA1_PN"], sets["mAL"]),
        "DA1_PN_to_mAL_m": signed_hop1(w, nt_s, sets["DA1_PN"], sets["mAL_m"]),
    }
    if hops["LC10a_to_P1"]["signed"] != PARENT_LC10A_SIGNED:
        raise SystemExit("LC10a signed drifted from fly_p1_sign @45aa064")
    if hops["DA1_PN_to_P1"]["signed"] != PARENT_DA1_SIGNED:
        raise SystemExit("DA1 signed drifted from fly_p1_sign @45aa064")
    named = {
        "ORN_HD": hops["VA1v_PN_to_P1"]["signed"],
        "DA1": hops["DA1_PN_to_P1"]["signed"],
        "LC10a": hops["LC10a_to_P1"]["signed"],
        "ppk23": hops["ppk23_to_P1"]["signed"],
        "mAL_GABA": hops["mAL_GABA_to_P1"]["signed"],
    }
    scale = PARENT_SCALE
    if abs(abs(named["LC10a"]) / TARGET_MAX - scale) > 1e-9:
        raise SystemExit("parent LC10a scale drifted")
    cva_signed = int(named["DA1"] + named["mAL_GABA"])
    w_p1 = {
        "ORN_HD": round(named["ORN_HD"] / scale, 4),
        "DA1": round(cva_signed / scale, 4),
        "LC10a": round(named["LC10a"] / scale, 4),
        "ppk23": round(named["ppk23"] / scale, 4),
    }
    through = bool(w_p1["DA1"] <= PARENT_W_CRIT)
    cva_term = {
        "da1_hop1_signed": named["DA1"],
        "mal_gaba_hop1_signed": named["mAL_GABA"],
        "combined_signed": cva_signed,
        "scale_divisor": scale,
        "W": w_p1["DA1"],
        "parent_w_crit": PARENT_W_CRIT,
        "parent_sha": PARENT_SHA,
        "through_wcrit": through,
        "da1_to_mal": hops["DA1_PN_to_mAL"],
        "da1_to_mal_m": hops["DA1_PN_to_mAL_m"],
    }
    cells = [
        "ORN_HD",
        "ORN_cVA",
        "DA1",
        "ppk23_f",
        "ppk23_m",
        "LC10a",
        "P1",
        "pC1",
        "pIP10",
        "song_CPG",
        "copulation",
    ]
    n = len(cells)
    W = [[0.0] * n for _ in range(n)]
    W[0][0] = 0.15
    W[1][1] = 0.15
    W[2][1] = 1.5
    W[2][2] = 0.10
    W[3][3] = 0.10
    W[4][4] = 0.10
    W[5][5] = 0.15
    # P1 row: parent hop-1 named classes, cVA slot = DA1 hop-1 plus mAL GABA.
    W[6][0] = w_p1["ORN_HD"]
    W[6][2] = w_p1["DA1"]
    W[6][3] = w_p1["ppk23"]
    W[6][4] = w_p1["ppk23"]
    W[6][5] = w_p1["LC10a"]
    W[6][6] = 0.35
    W[7][6] = 1.00
    W[7][7] = 0.20
    W[8][6] = 1.10
    W[8][7] = 0.30
    W[8][8] = 0.15
    W[9][8] = 1.20
    W[9][9] = 0.20
    W[10][6] = 0.70
    W[10][7] = 0.20
    W[10][10] = 0.10
    extract = {
        "dataset": "male-cns:v1.0",
        "weights": "significant-only",
        "kind": "hop1_mal_gaba_folded_onto_pC1_coexpress",
        "P1_definition": "type pC1_* and fruDsx coexpress_*",
        "mAL_definition": "type startswith mAL",
        "mAL_gaba": "pre consensus_nt gaba",
        "n_P1": len(P1),
        "n_pC1": len(sets["pC1_all"]),
        "n_mAL": len(sets["mAL"]),
        "n_mAL_m": len(sets["mAL_m"]),
        "class_n": {k: len(v) for k, v in sets.items()},
        "hops": hops,
        "named_signed_onto_P1": named,
        "scale_divisor": scale,
        "target_max_abs": TARGET_MAX,
        "scale_setter": "LC10a_parent",
        "W_P1_named": w_p1,
        "cva_term": cva_term,
        "holes": {
            "ppk23_hop1_onto_P1": hops["ppk23_to_P1"]["weight"] == 0,
            "ORN_HD_direct_onto_P1": hops["ORN_VA1v_to_P1"]["weight"] == 0,
            "DA1_hop1_sign": "acetylcholine_positive",
            "da1_to_mal_m_hop1": hops["DA1_PN_to_mAL_m"]["weight"] == 0,
            "ppk23_f_m_split": "absent_in_map",
        },
    }
    spec = {
        "name": "malecns_p1_mal_gaba",
        "sex": "male",
        "parent_map": "malecns_male",
        "parent_n": 166691,
        "female_parent_n": 139255,
        "kind": "hop1_mal_gaba_folded_onto_pC1_coexpress",
        "citation": (
            "Berg et al., Cell 2026. Hop-1 GABA from annotated mAL folded into "
            "W[P1, DA1] on the fly_p1_sign @45aa064 LC10a scale. Not a 166,691-cell LIF."
        ),
        "cells": cells,
        "sensors": ["ORN_HD", "ORN_cVA", "ppk23_f", "ppk23_m", "LC10a"],
        "readouts": {
            "P1": ["P1"],
            "orient": ["P1", "pC1"],
            "song": ["song_CPG"],
            "attempt": ["copulation"],
        },
        "W": W,
        "default_w_p1_da1": w_p1["DA1"],
        "cva_term": cva_term,
        "parent_w_crit": PARENT_W_CRIT,
        "parent_sha": PARENT_SHA,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "extract.json").write_text(json.dumps(extract, indent=2) + "\n", encoding="utf-8")
    (OUT / "male_p1.json").write_text(json.dumps(spec, indent=2) + "\n", encoding="utf-8")
    PROV.write_text(
        json.dumps(
            {
                "kind": "hop1_mal_gaba_folded_onto_pC1_coexpress",
                "parent_male": {"map": "MaleCNS v1", "n": 166691, "citation": "Berg et al., Cell 2026"},
                "parent_tree": {"repo": "fly_p1_sign", "sha": PARENT_SHA, "w_crit": PARENT_W_CRIT},
                "sha256": LOCK_SHA,
                "extract": True,
                "note": (
                    "Hop-1 GABA from type-mAL onto pC1 coexpress, folded into the "
                    "cVA slot. Motor rows are schema. Scale locked to parent LC10a."
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print("W_P1", w_p1, "cva_signed", cva_signed, "through_wcrit", through)
    print("wrote", OUT / "male_p1.json")


if __name__ == "__main__":
    main()
