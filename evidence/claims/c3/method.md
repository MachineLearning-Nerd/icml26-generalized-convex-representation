# C3 exact counterexample method

The verifier encodes the paper's leanness definition directly. For every
support index, a lean vector must have at least one row where its branch is
maximal (ties count). A nonlean midpoint must have one support index that is
strictly dominated by another branch at every row.

Z3 searches bounded integer surplus matrices and two integer parameter
vectors. Any model is then checked independently using exact
`fractions.Fraction` arithmetic. Finite `X` and `Y` are compact Euclidean
subsets, every supremum is attained, and any real-valued function on their
finite product is Lipschitz.

Negative control: additionally require the two endpoint vectors to be
identical. A lean vector's midpoint with itself is the same lean vector, so
the counterexample constraints must be unsatisfiable.
