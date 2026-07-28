# C3 evaluator contract

Mark **FALSIFIED** only if:

- the SMT search returns a concrete witness;
- both endpoint parameter vectors are lean under exact score comparisons;
- their midpoint loses one support strictly at every point of `X`;
- finite compactness, attained suprema, and a finite Lipschitz bound are
  recorded;
- the identity negative control is `unsat`; and
- the cumulative process exits nonzero if any check fails.

The result is scoped to the exact v1 quantifiers. It need not show failure for
every economically structured surplus; one admissible counterexample is
enough to falsify the universal theorem.
