# fly_p1_mal

Does hop-1 GABA from annotated mAL onto the same 88 cells pull the cVA term through W_crit ≈ -1.54, and only then does HD-on / cVA-off become necessary and sufficient?

Yes. Hop-1 GABA from type-mAL onto the 88 pC1 coexpress cells is -8810. Folded with hop-1 DA1 +62 on the parent LC10a scale (606 to 1.8), `W[P1, DA1] = -25.9842`, which is through parent `W_crit = -1.539`. Then HD-on / cVA-off is necessary and sufficient. `hd_on_cva_off_ns` is true. Seed 1, 2,000 steps, `logs/p1_mal_s1.json`.

Parent [fly_p1_sign](https://github.com/martialsystems/fly_p1_sign) `@45aa064` put MaleCNS hop-1 signed counts on this row and cVA could not reject (`W[P1, DA1] = +0.1842`). Grandparent [fly_icarus](https://github.com/martialsystems/fly_icarus) `@2cf5fd6` used a published-sign -1.8 DA1 brake. This tree keeps the same 88 cells and the same battery. It folds annotated mAL GABA into the cVA slot.

Hop-1 onto 88 pC1 coexpress cells, parent LC10a scale:

| pre class | signed weight | scaled W onto P1 |
|-----------|--------------:|-----------------:|
| LC10a | +606 | 1.8 |
| DA1_lPN/vPN | +62 (acetylcholine) | 0.1842 before fold |
| mAL GABA | -8810 | folded into DA1 |
| cVA term (DA1 + mAL GABA) | -8748 | -25.9842 |
| VA1v PNs (HD path) | -3 | -0.0089 |
| putative_ppk23 | 0 | 0 |

DA1_lPN hop-1 onto annotated mAL is 96 ACh onto 2 mALB1 cells. Hop-1 onto `mAL_m*` is 0. The fold is the compressed object: mAL GABA rides the cVA channel. n_mAL = 159. n_P1 = 88.

## Locked metrics

Copied from `logs/p1_mal_s1.json`.

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

3 tracks 1 (`d31 = 0.0`) because both have cVA off. 3b tracks 2: cVA is on and the folded term rejects. `through_wcrit` is true. `hd_on_cva_off_ns` is true. 3c equals 3d: ppk23 hop-1 is still 0. Seeds 2 and 3 match.

DA1 dose on the 3d pin (`logs/p1_da1_dose_s1.json`): extract default `W[P1, DA1] = -25.9842`, P1 = -0.9986. P1 crosses zero at `W[P1, DA1] = -1.539`, the same crossing as `@45aa064`. The folded default sits on the reject side of that crossing.

`--n 1000`, `--unfreeze`, and `--female-brain-icarus` stay stubbed. Hop-3 is unasked.

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
| `NEXT.md` | Closed. DA1 drive onto mAL_m* unasked. |
| `THIRD_PARTY.md` | Connectome attribution |

[Fly research index](https://gist.github.com/martialsystems/12835f747d6360781f3cc7f91f243178)
