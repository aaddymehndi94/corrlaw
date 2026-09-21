# Development encoding limitation — preserve it as a negative case

During development002, B seed201 exact/noiseless augmented QBC had no accepted
initial witness despite an admissible point model equivalent numerically to1+v².
Its saved feature representation is a product involving the constant feature z0.
The public dictionary defines z0=1, but the current generic-symbol representation
does not substitute that identity before adding the near-null direction.

An evaluator-side check using the supplied circle relation (not pretending it was
learner-discovered) yields alternatives with observed RMSE approximately1.9e-11.
Their encoded arithmetic complexity is19, above the common15-node cap. Substituting
the known z0=1 and expanding produces equivalent9-node expressions on the public
feature domain. The current detector can therefore miss admissible alternatives
because of representation and its limited construction procedure, not uniqueness.

Do not silently change the algorithm or retroactively count these as discovered
witnesses. The current comparison remains a bounded implementation study. Constant-
feature folding or canonicalization across feature identities would be a separate
method revision/ablation; that experiment has NOT been performed. Increasing search
iterations may or may not find a simpler base encoding; the predeclared compute
sensitivity will report actual outcomes without changing this representation rule.

The read-only check was first explored in work/development002-representation-diagnostic.json.
A reproducible script is prepared as examples/representation_diagnostic.py and must
be run through the wrapper after development002 completes, under the new immutable
ID representation-diagnostic-001. It checks source hashes and equivalence on saved
observed/calibration/public inputs. This is a selected development failure analysis,
not held-out confirmation or evidence of a globally complete simplifier.

Zero constructed witnesses does not mean the existing search committee contains
only one function or is overconfident. Record its saved spread separately. This
case diagnoses the added-witness construction, not a claim that ordinary QBC missed
all ambiguity. The reproduction script retains the original initial metric and
ordinary committee size for that distinction.
