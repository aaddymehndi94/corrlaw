# Related work and source-verification ledger

Prepared on 2026-09-21. This is a checked seed reading list, NOT an exhaustive novelty
review. The lead must read the relevant methods and update exact publication/version
metadata before making a paper claim. Do not treat search snippets as a full-method
review. Keep a note of what was actually inspected and any inaccessible material.

## Scientific sources

### R1 — SRSD
Matsubara et al., *Rethinking Symbolic Regression Datasets and Benchmarks for
Scientific Discovery*.
https://arxiv.org/abs/2206.10540
https://github.com/omron-sinicx/srsd-benchmark
The arXiv record identifies a 2024 DMLR publication and describes redesigned physical
sampling ranges and equation-recovery evaluation. Changing benchmark sampling alone
is not new. Record inspected version and any reused data/code separately.
Verification in kit preparation: title, authors, abstract, version/publication fields.

### R2 — Physically constrained active learning
*Active Learning in Symbolic Regression with Physical Constraints*.
https://arxiv.org/abs/2305.10379
https://arxiv.org/html/2305.10379
Relevant prior work on candidate-equation disagreement for experiment selection.
Do not claim to invent symbolic-regression active learning. Read the revised methods
for a fair implementation comparison; record the precise criterion being adapted.
Verification in kit preparation: paper identity and accessible HTML/abstract.

### R3 — Ensemble-SINDy
Fasel, Kutz, B. W. Brunton and S. L. Brunton, *Ensemble-SINDy: Robust sparse model
discovery in the low-data, high-noise limit, with active learning and control*.
https://arxiv.org/abs/2111.10992
https://doi.org/10.1098/rspa.2021.0904
Relevant prior work on bagged sparse-model discovery and ensemble-guided acquisition.
Do not describe a finite-library bootstrap baseline as an entirely new method.
Verification in kit preparation: title/authors/abstract and linked publication DOI.

### R4 — Ensemble overconfidence and feature dropout
Nair, Foppa and Scheffler, *Materials-Discovery Workflows Guided by Symbolic
Regression: Identifying Acid-Stable Oxides for Electrocatalysis*.
https://arxiv.org/abs/2412.05947
https://arxiv.org/html/2412.05947
The accessible methods discuss SISSO ensembles, bagging and feature dropout, and
explicitly address ensemble overconfidence. Our small synthetic benchmark does not
reproduce its materials calculations. Feature/library dropout is a serious existing
safeguard to compare, not new to this project.
Verification in kit preparation: title, abstract and ensemble-method section.

### R5 — Model-discriminating experimental design
Strouwen and Micluta-Campeanu, *Experimental Design for Missing Physics*.
https://arxiv.org/abs/2604.01231
https://doi.org/10.1016/j.ifacol.2025.07.192
The arXiv abstract describes sequential designs that discriminate plausible symbolic
structures. Its record also lists an IFAC-PapersOnLine journal/proceedings reference;
verify the linked publication before calling this only an unpublished 2026 preprint.
This corrects the oversimplified publication label in the earlier prompt.
Verification in kit preparation: title, abstract and displayed publication link.

### R6 — Geometry and identifiability
Gallo, Anselmi and Lazzari, *Attractor Geometry Determines the Identifiability Limits
of System Discovery*; arXiv record submitted 20 July 2026.
https://arxiv.org/abs/2607.18490
The abstract studies geometry/feature-moment conditioning and equation identification.
Treat it as a preprint unless a reviewed version is verified. Read assumptions before
transferring its identifiability assertions to a sparse algebraic benchmark; singular
feature covariance by itself does not establish every model-class-specific claim.
Verification in kit preparation: title, authors, abstract and submission metadata.

### R7 — PySR implementation
https://github.com/astroautomata/PySR
https://ai.damtp.cam.ac.uk/pysr/
Use the actual installed API and a real smoke test. Archive candidate equations and
record Python/Julia/package versions. Do not simulate a PySR result with a substitute.
Verification in kit preparation: official repository and its Python/Julia description.

## Framework references

### F1 — Codex project instructions
https://developers.openai.com/codex/guides/agents-md/
Official documentation describes repository AGENTS.md discovery and layered guidance.
This kit keeps the root instructions small and places detailed research state in
explicitly linked files. Do not change global configuration to make the kit work.

### F2 — Repository-local knowledge
https://openai.com/index/harness-engineering/
OpenAI describes a short instruction index pointing to versioned repository knowledge.
This motivated the file layout, not a measured success guarantee for this research.

### F3 — Long-horizon work
https://developers.openai.com/blog/run-long-horizon-tasks-with-codex
The documented loop combines execution, verification, repair and durable progress.
The kit adopts that pattern without claiming uninterrupted ten-hour execution.

## Lead-agent audit to complete
For every research novelty claim, record the closest source, actual method overlap,
assumptions that differ, baseline implemented, missing comparison and status.
Specifically test equivalence to classical regularized optimal design/leverage.
If the proposed method is already known, keep a useful scoped replication or
failure benchmark; do not rename it and claim a discovery.

## Lead audit — 2026-09-21 (T03)
Accessed primary arXiv records and HTML. This is a targeted method comparison,
not an exhaustive novelty determination. No code/data from these papers is copied.

- R1: v5 (5 March 2024), DMLR 2024 according to the arXiv record. Inspected record
  and HTML benchmark discussion. Physical domains and equation-level evaluation
  motivate our bounded, dimensionless suite; our six toy systems are not SRSD.
- R2: revised v3 (9 August 2024), HTML sections 2.2–4.2. Pareto-front equations
  drive QBC; CV and IBMD normalize disagreement differently. We implement a finite
  sparse-library adaptation with fixed-output-scale variance, not their PySR method
  or a direct replication of its reported scores.
- R3: v1 (22 November 2021), HTML section 3, algorithms 2–3 and active learning.
  Bootstrap rows and sample library terms without replacement. Our diversified
  baseline borrows this established library-bagging idea, with greedy sparse fits
  rather than derivative-based STLSQ. Related publication DOI is
  https://doi.org/10.1098/rspa.2021.0904 (arXiv metadata; publisher not re-reviewed).
- R4: HTML ensemble-method paragraphs, inspected 21 September 2026. Bagging plus
  Monte Carlo primary-feature dropout addresses overconfidence in SISSO; their
  acquisition uses probability of feasibility. Ours subsamples dictionary columns
  and uses variance. No materials-discovery performance claim transfers to our suite.
- R5: v1; HTML sections 3–7 and source publication footnote. ArXiv lists
  IFAC-PapersOnLine 59(6), 481–486 (2025), DOI 10.1016/j.ifacol.2025.07.192.
  The DOI destination failed to load in this session; HTML independently states
  acceptance at IFAC. Thus publication metadata is corroborated by author text,
  but the publisher version was not inspected. Model-discriminating sequential
  design is prior work, not a contribution of CorrLaw.
- R6: v1 (20 July 2026), preprint; inspected geometry/mechanistic discussion and
  supplementary exact-collinearity propositions. Near-null feature directions and
  sparse identifiability are closely related prior topics. We do not rely on its
  stronger target-specific claims: our numerical claim requires an explicit
  alternative satisfying our own bounded model class and measurement tolerances.
- R7: PySR 2.5.0 actually installed; inspected local sr.py constructor and Julia
  import setup. A real bounded import/fit attempt is recorded as pysr-smoke-001.

Narrow possible value: a reproducible comparison with saved, admissible sparse
alternative equations and preparation controls. Neither QBC augmentation alone nor
small singular values establish novelty. See EQUIVALENCE.md for exact overlap.
