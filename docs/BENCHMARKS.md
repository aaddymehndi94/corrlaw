# Physical and statistical contract

All variables are dimensionless numerical columns at the learning interface.
The evaluator alone knows the physical names and reference formulas below.
These are idealized algebraic systems, not claims about real laboratory accuracy.
Reference scales can be any positive SI values; the implementation tests nonunit
scales. B uses one common length scale; E/F one common capacitance scale.

| Task | Dimensional ideal equation | Inputs (u,v) | Output reference | Dimensionless y |
|---|---|---|---|---|
| A | F = k Δx | k/k₀, Δx/ℓ₀ | k₀ℓ₀ | uv |
| B | U = (k x² + 2k z²)/2 | x/ℓ₀, z/ℓ₀ | kℓ₀²/2 | u²+2v² |
| C | a = V²/R | V/V₀, R/R₀ | V₀²/R₀ | u²/v |
| D | E = m V²/2 | m/m₀, V/V₀ | m₀V₀²/2 | uv² |
| E | C_parallel = C₁+C₂ | C₁/C₀, C₂/C₀ | C₀ | u+v |
| F | C_series = C₁C₂/(C₁+C₂) | C₁/C₀, C₂/C₀ | C₀ | uv/(u+v) |

A assumes Hooke's linear regime with independently set positive stiffness and
extension. B is an ideal anisotropic harmonic potential with evaluator zero at the
origin. C allows independent speed and positive radius, and evaluates centripetal
acceleration rather than treating it as a control. D allows mass and nonrelativistic
speed controls. E/F are ideal linear capacitors with independently chosen positive
capacitances; topology is fixed per task. Absorbed factors of 1/2 are shown above.
The numerical toy domains are chosen as valid regimes by assumption; no dimensional
empirical parameter ranges are inferred from these experiments.

A/C/D/F: each input [0.5,1.5]. B: each coordinate [-1.5,1.5]. E: u in [0.6,1.4],
v in [0.3,2]. All reciprocal features avoid zero on positive-variable domains.
Initial positive-task u is uniform within its interval and v=u+ε, except E uses
v=u²+ε. ε is independent Uniform[-w,w]; pairs outside bounds are rejected and
redrawn, with w ∈ {0,0.01,0.05}. B uses uniform angle and radius 1+ε. Width is not
output noise. Labels are recomputed at every perturbed/shuffled coordinate, then
independent Gaussian output noise with σ ∈ {0,0.01} is added in output-reference
units. Hidden errors use noiseless references to measure function error.

Controls: independent uniform inputs; shuffled v on the initial exact preparation
(preserves the realized marginal samples); query pool on the exact initial surface.
Controls run at w=0 for both noise levels. Same-preparation tests use the control's
sampling distribution; off-preparation tests always use independent uniforms in the
same declared box. This can change both dependence and observed marginal coverage
(e.g. ring versus square); it is not proof of pure dependence-shift robustness.
Shuffled controls retain marginals, but finite-sample permutations need not produce
perfect empirical independence.

Primary prior setting: generic dimensionless regression; only domains, operator
class, coefficient/complexity limits and noise scale are supplied. No positivity,
symmetry or known origin boundary is imposed on any learner. In B the known extra
prior U(0,0)=0 would exclude g=1+v²; this is explicitly tested, not withheld from
some policies. A full prior-aware experimental sweep is outside the pilot.

Generic dictionary: monomials x0^a x1^b with |a|+|b|≤3, a,b≥0 on signed domains;
on strictly positive domains also allow a,b=-1. The rule does not select by task.
A–E have exact representations; F does not (the reciprocal of a sum is missing).
F is the prespecified misspecification diagnostic. All domains share degree,
term-count and coefficient restrictions; positivity alone determines whether
Laurent features are safe. Feature RMS uses 512 independent public unlabeled box
probes, not labels or hidden tests, without centering the constant. Broad probes
remain permitted for computation even when actual measurements are surface-limited.

## Overnight PySR and prior-control extension

The distributions, reference scales and anonymous numerical interfaces above apply
to both engines. The representability statements about A–E and missing F concern
the finite LINEAR span of the feature dictionary. The PySR extension composes those
same generic feature terminals with arithmetic, including division, and can represent
F. This does not guarantee its search will find F. See METHOD_PYSR.md and the current
protocol for the common arithmetic cap, search budgets and exact confirmation grid.

The original pilot's primary priors remain incomplete. The separate B follow-up
supplies known origin/parity restrictions equally to every policy in each tier;
its results concern the restricted degree<=3 polynomial class. Positivity checks
on saved primary witnesses are descriptive finite-probe analyses, not a changed
primary acquisition experiment. Full dimensional priors and analytical class
counterexamples are discussed separately from algorithm-generated witnesses.
