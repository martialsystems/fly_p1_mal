# Agent notes: fly_p1_mal

MIT for original code. FlyWire and MaleCNS remain under their published licenses (typically CC BY 4.0).

Question: Does hop-1 GABA from annotated mAL onto the same 88 cells pull the cVA term through W_crit ≈ -1.54, and only then does HD-on / cVA-off become necessary and sufficient?

Parent `fly_p1_sign` `@45aa064` is closed. Do not restamp its hop-1 DA1 = +62 ACh finding as this tree's weight. Do not reopen `p1_sign_s1.json`. Do not replay `@45aa064`. Unfreeze stays stubbed. Hop-3 stays unasked. LH crowds stay unasked. `--n 1000` and `--female-brain-icarus` stay stubbed.

W is hop-1 GABA from type `mAL*` onto the same 88 pC1 coexpress cells, folded into `W[P1, DA1]` on the parent LC10a scale (606 to 1.8). DA1 hop-1 stays +62 in the extract. Motor scaffolding is schema. Not a 166,691-cell LIF.

If `through_wcrit` is false, stop. Do not add hop-3, unfreeze, or a second inhibitory class.

Pin is `malforge/`. Hop-1 extract is required. Unique reconstruction is refused. Verify-before-done is the finish gate.

## Verify

`python3 ~/agent_laws_verify_before_done/vbd_gate.py check --app-root . --claim-done`

Do not use stock `/usr/bin/python3 -m pytest`.
