# Known-method equivalence audit

For a two-member committee f(x) ± αq(x), equal-weight mean is f and population
prediction variance is α²q(x)². This is an elementary identity, not a new theorem.
For linear features φ(x), information M = ΦᵀΦ + λI, the matrix determinant lemma
makes the one-point D-optimal gain log(1 + φᵀM⁻¹φ). Ranking by the leverage score
φᵀM⁻¹φ is therefore exactly greedy regularized D-optimal design.

With M = Σ_j μ_j v_j v_jᵀ, leverage equals Σ_j (φᵀv_j)²/μ_j. If a single weakly
observed mode dominates and q is proportional to φᵀv_min, its leading ranking
matches squared-witness disagreement. Exact equality needs all other contributions
to be constant over the pool, or the limiting rank-one inverse-information form.
Several weak directions, coefficient/admissibility bounds, uneven alternative
weights, and an existing nontrivial committee can change the ranking. We must
measure actual choices, not infer equality from a small eigenvalue.

The witness search solves small Gram eigenproblems equivalent to right-singular
vectors of 2/3-column submatrices. Squaring conditioning can lose precision near
machine zero; observed residuals are re-evaluated directly before acceptance.
A direction alone does not establish an alternative inside a sparse model class.
We require both bounded fitted expressions to pass observed/calibration and
acquired-point residual checks. Failure to find one does not prove uniqueness.

Acceptance evidence: tests/test_science.py::test_design_equivalence_and_determinant
checks both identities numerically. The supplied circle identity is separately
proved symbolically by test_circle_symbolic_and_prior. Actual first-query agreement
and full query sequences will be summarized from the paired saved run artifacts.
