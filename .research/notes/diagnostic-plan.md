# T16 follow-up study plan, written before new diagnostic outcomes

These diagnostics follow a negative pilot and are EXPLORATORY. They must not be
presented as fresh held-out confirmation on the reused pilot seeds.

1. Generic exhaustive-support search on archived finite-library observations.
Use the SAME anonymous observations and feature library as the original unit.
Enumerate supports of sizes1,2,3; fit coefficients by lstsq rcond1e-10 with the
same scaled coefficient cap20; score using the original train/calibration/acquired
errors +1e-8 term count. Retain all observationally admissible supports. No target
formula enters the enumeration, score or choice. Evaluate the selected expression
only afterward. This tests whether the greedy pursuit missed a much simpler
available explanation; it does not repair the original acquisition trajectories.
Use all original C/D/E/F seeds92001–92005, constrained widths0/.01, noises0/.01,
all five policies, budgets0/2/8. Group paired observations and cache exact duplicate
inputs to avoid counting repeated initial fits as distinct experiments. Save every
selected support/equation and all model-fit/held-out numbers. Record F explicitly,
since no three-feature linear support makes its true reciprocal-of-sum representable.

2. Numerical physical-prior control on development B.
Individually even coordinates and a known zero potential at the origin are extra
physical priors. In the signed polynomial dictionary of degree<=3 these restrict
allowed columns to u^2 and v^2. This is a strong class restriction (homogeneous
quadratics under this dictionary), not proof that the single zero-origin boundary
alone establishes uniqueness in larger nonlinear classes. Compare no prior,
zero-origin only (remove constant), and origin+evenness (remove odd exponent terms),
with identical prior delivery to every candidate/policy and witness. The supplied
circle rival1+v^2 is excluded by the zero-origin prior; other odd cubic aliases can
remain unless parity is also known. Report this distinction rather than overclaiming.

Run B seeds301–305, widths0/.01, noises0/.01, all5 policies, budget0–8; base library
restrictions applied before fitting, D-optimal and witness search. Counts of columns
and all observable-fit checks must be saved. This is a separate finite-library
study with known stronger physics, not an improvement claim for the prior-free
proposal. Hold ordinary feature normalization and thresholds fixed.

Acceptance: artifact checks, exact replay of one prior-aware noisy run, figures
showing actual error/witness coverage and a precise discussion of what information
was supplied. Do not change the frozen PySR comparison using these outcomes.

Analytical control to verify: the cubic relation u*(u^2+v^2-1) vanishes on the
observed circle AND at the origin. Thus origin knowledge alone does not rule out
all alternatives in the degree3 dictionary. The same is true with v instead of u.
The parity prior eliminates these particular odd cubic witnesses. Positivity has
not been supplied in this control and must not be silently assumed; the resulting
regression class permits signed alternatives despite the potential interpretation.
A positivity prior would be another, stronger experiment and needs its own filter.
