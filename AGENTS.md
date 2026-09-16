# Agent notes: fly_p1_mal

MIT for original code. FlyWire and MaleCNS remain under their published licenses (typically CC BY 4.0).

Question: Does hop-1 GABA from annotated mAL onto the same 88 cells pull the cVA term through W_crit ≈ -1.54, and only then does HD-on / cVA-off become necessary and sufficient?

Allowed public sentence: Hop-1 mAL GABA onto these 88 cells is large enough to pass W_crit if it is assigned to cVA. DA1 hop-1 onto mAL_m* is 0; onto two mALB1 cells it is 96 ACh.

`@e16856c` stays closed as a conditional: mAL can be the brake if it rides cVA. `hd_on_cva_off_ns=true` is the fold succeeding. Do not reopen the Icarus battery. Do not treat W=-25.9842 as a map proof of the house rule. Do not restamp `logs/p1_mal_s1.json`. Parent `fly_p1_sign` `@45aa064` stays frozen.

W is hop-1 GABA from type `mAL*` onto the same 88 pC1 coexpress cells, folded into `W[P1, DA1]` on the parent LC10a scale (606 to 1.8). DA1 hop-1 stays +62 in the extract. Motor scaffolding is schema.

`--n 1000`, `--unfreeze`, and `--female-brain-icarus` stay stubbed. Hop-3 stays unasked. LH crowds stay unasked.

Pin is `malforge/`. Hop-1 extract is required. Unique reconstruction is refused. Verify-before-done is the finish gate.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

Do not use stock `/usr/bin/python3 -m pytest`.
