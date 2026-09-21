# Strong dimensional priors: a limit on the benchmark's physical interpretation

This is classical dimensional analysis, not a new result. The relevant historical
reference is E. Buckingham, *On Physically Similar Systems; Illustrations of the
Use of Dimensional Equations*, Physical Review4,345 (1October1914),
https://journals.aps.org/pr/abstract/10.1103/PhysRev.4.345 . The APS publication page
was opened and its bibliographic fields verified on2026-09-21UTC. The full paper was
not required for or claimed as the source of the direct unit-balance derivations below.

Assume the output depends only on the TWO named dimensional inputs, the law is
invariant to units, and there are NO additional dimensional parameters. Reference
scales used for nondimensionalization are not admitted as extra physical constants.
Writing a candidate c*a^p*b^q, match exponents of mass,length,time. The input
dimension matrix has rank2 and no input-only dimensionless combination in A/C/D:

| Task | Inputs and dimensions | Output dimensions | Forced powers(p,q) |
|---|---|---|---|
| A | stiffness(M T^-2),extension(L) | force(M L T^-2) | (1,1) |
| C | speed(L T^-1),radius(L) | acceleration(L T^-2) | (2,-1) |
| D | mass(M),speed(L T^-1) | energy(M L^2 T^-2) | (1,2) |

An unknown dimensionless coefficient remains, including D's factor1/2. Under these
strong assumptions the functional structure is already fixed by dimensional
information; a symbolic-discovery comparison is unnecessary for those structures.
The exact linear systems were solved with SymPy; reports/audit/dimensional-prior-algebra.json
contains matrices/ranks/exponents. These are derivations under stated assumptions,
not empirical measurements or newly discovered laws.

The primary benchmark intentionally supplies generic dimensionless numerical
columns, domains, noise, and expression limits instead of this full dimensional
structure. It tests a data-geometry/algorithm question. It must NOT imply that
physicists armed with complete dimensional knowledge need these extra queries.
For E/F, the two inputs and output share capacitance units, so dimensional
homogeneity requires degree1 but permits arbitrary dependence on their ratio.
Symmetry and absence of extra scales still do not alone distinguish all such laws.
This helps explain why the nonlinear series-capacitance case is more informative
than monomial recovery alone. The B origin/parity control addresses another form of
strong prior information, with a different restricted function class.
