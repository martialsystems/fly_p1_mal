# fly_p1_mal

Does hop-1 GABA from annotated mAL onto the same 88 cells pull the cVA term through W_crit ≈ -1.54, and only then does HD-on / cVA-off become necessary and sufficient?

Hop-1 mAL GABA onto these 88 cells is large enough to pass W_crit if it is assigned to cVA. DA1 hop-1 onto mAL_m* is 0; onto two mALB1 cells it is 96 ACh. Extract `@e16856c`, `logs/p1_mal_s1.json`.

Parent [fly_p1_sign](https://github.com/martialsystems/fly_p1_sign) `@45aa064`: hop-1 DA1 onto the same 88 is +62 ACh (scaled W=0.1842). Grandparent [fly_icarus](https://github.com/martialsystems/fly_icarus) `@2cf5fd6`: published-sign `W[P1, DA1] = -1.8`. This tree measures hop-1 onto those 88 cells, then assigns mAL GABA to the cVA slot by hand.

Hop-1 onto 88 pC1 coexpress cells, parent LC10a scale (606 to 1.8):

| pre class | signed weight | note |
|-----------|--------------:|------|
| LC10a | +606 | scale setter |
| DA1_lPN/vPN | +62 | acetylcholine |
| mAL GABA | -8810 | giant term on this row |
| VA1v PNs (HD path) | -3 | |
| putative_ppk23 | 0 | |

Drive onto the mAL cells that account for the -8810:

| hop-1 | signed | n_post |
|-------|-------:|-------:|
| DA1 PN → mAL_m* | 0 | 0 |
| DA1 PN → annotated mAL | +96 ACh | 2 mALB1 |

Assigned to cVA, the folded term is `W[P1, DA1] = -25.9842` versus parent `W_crit = -1.539`. That is a channel assignment on this row. n_mAL = 159. n_P1 = 88.

## Fold on the same battery

Copied from `logs/p1_mal_s1.json`. `hd_on_cva_off_ns` is true because the cVA slot was given -25.9842. 3c equals 3d: ppk23 hop-1 is 0.

| condition | P1 mean | DA1 term | LC10a term | song |
|-----------|--------:|---------:|-----------:|-----:|
| 1 flying female | 0.9207 | 0.0 | 1.2878 | 0.983 |
| 2 flying male | -0.9989 | -10.3838 | 0.345 | 0.0 |
| 3 Icarus, HD | 0.9207 | 0.0 | 1.2874 | 0.983 |
| 3b Icarus, cVA | -0.9987 | -10.383 | 0.7841 | 0.0 |
| 4 body only | 0.9219 | 0.0 | 1.2885 | 0.983 |
| 5 odor only | 0.7093 | 0.0 | 0.6479 | 0.973 |
| 6 Icarus female tag | 0.9207 | 0.0 | 1.2876 | 0.983 |
| 3c pin male cuticle | -0.9986 | -21.7797 | 1.2902 | 0.0005 |
| 3d pin female cuticle | -0.9986 | -21.7797 | 1.2902 | 0.0005 |
| copresent HD+cVA | -0.9987 | -10.3817 | 0.784 | 0.0 |

DA1 dose on the 3d pin (`logs/p1_da1_dose_s1.json`): default `-25.9842`, P1 = -0.9986. Crossing remains `W[P1, DA1] = -1.539`. Seeds 2 and 3 match.

`--n 1000`, `--unfreeze`, and `--female-brain-icarus` stay stubbed. This tree stays closed as a conditional: mAL can be the brake if it rides cVA. Do not reopen the Icarus battery here.

Female template count: FlyWire 139,255. Male template count: MaleCNS 166,691.

## How to run

```
.venv/bin/python -m pytest
.venv/bin/python -m fly_p1_mal assay --seed 1 --steps 2000 --out logs/p1_mal_s1.json
.venv/bin/python -m fly_p1_mal da1-dose --seed 1 --steps 2000 --out logs/p1_da1_dose_s1.json
```

Rebuild W from feathers (optional):

```
.venv/bin/python scripts/extract_p1_weights.py
```

Do not overwrite `logs/p1_mal_s1.json`.

## Files

| Path | Role |
|------|------|
| `src/fly_p1_mal/` | Assay, folded cVA W, Icarus flag |
| `data/templates/extract.json` | Raw signed hop-1 sums plus mAL GABA |
| `data/templates/male_p1.json` | Scaled 11-cell W, cVA slot folded |
| `logs/p1_mal_s1.json` | Locked seed-1 battery |
| `logs/p1_da1_dose_s1.json` | 3d-pin DA1 sweep |
| `malforge/` | GraphForge pin |
| `AGENTS.md` | Project rules and VBD |
| `NEXT.md` | Drive check. This tree closed. |
| `THIRD_PARTY.md` | Connectome attribution |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
