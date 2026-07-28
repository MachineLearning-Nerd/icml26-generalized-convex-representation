# C1 evaluator contract

Verdict: **VERIFIED** if and only if the cumulative verifier reports all of:

- source hash and anchors match the protected audit;
- the checked proof DAG matches `proof_certificate.json`;
- the negated symbolic local bound is `unsat`;
- the independent exact-rational checker passes;
- the corrupted-radius control is `sat` with a witness; and
- the process exits nonzero if any item fails.

This proof-level route discharges the theorem's universal quantifiers under the
paper's compactness and Lipschitz assumptions. It does not infer universality
from finite samples. The standard finite-subcover theorem for compact metric
spaces is a trusted mathematical primitive and is stated as the limitation.

The earlier grid page is retained only as **Historical rejected baseline** and
is superseded by this verifier.
