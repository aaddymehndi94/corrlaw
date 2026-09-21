# Complexity fairness revision — before overnight confirmation

The first PySR implementation searched native trees of maximum size10 but accepted
augmented expressions up to31 SymPy nodes. Those are different complexity measures
and the larger alternative cap could favor augmentation. No new C/D/E/F PySR
confirmation had started. Development001 was deliberately interrupted at 224
of360 completed policy units after this review; all saved artifacts and the
interrupted runner record remain intact. It had 0 execution failures before
interruption. Its numbers are exploratory and superseded for the fair comparison.

The revised search and ALL accepted expressions use a15-node arithmetic tree budget
with terminals, numeric constants, and binary+,-,*,/. Integer powers count as repeated
multiplication, reciprocal factors as division, and negative additive terms as
subtraction rather than an artificial extra multiplication by-1. Canonical algebra
may simplify an expression, but the accepted expression can be encoded in this same
native arithmetic grammar within15 nodes. Coefficient/number cap20 remains shared.
Configuration validation rejects unequal search and final caps. Focused tests cover
powers, subtraction, division, and mismatched configuration rejection.

Revised smoke: configs/pysr-fair-smoke.json, A/B seed204, all5 policies.
Revised complete development: configs/pysr-development-v2.json,360 units, same full
A/B grid and seeds201–203. Seed-first ordering covers both tasks before advancing
to another seed; it changes scheduling, not the learner or measurement streams.
Reproduction under the superseded code is not claimed for the revised algorithm.

Other prepared changes installed only AFTER development001 stopped: exploratory
search/prior/positivity diagnostics and tests; saved-witness viewer; typed CLI;
figure engine labels; strict earlier-deadline overlay; inactivity-based watchdog.
Pytest initially picked up duplicate test drafts under ignored work/, causing two
collection errors. testpaths now explicitly points to the actual tests/ suite;
drafts and all real tests are retained, not deleted or suppressed.
