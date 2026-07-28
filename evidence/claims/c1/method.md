# C1 current method

Current verifier: `repro/src/c1_proof.py` on the C1 child revision.

The proof is reconstructed from the exact hashed source. Compactness gives a
finite `epsilon/(4 lambda)`-net of `Y`. The `lambda`-Lipschitz bounds for `Phi`
and the transform contribute at most `epsilon/4` each, so every full-support
branch is at most `epsilon/2` above a selected finite-support branch. Taking
suprema preserves the inequality, while support inclusion gives `g <= f`.
Thus `||f-g||_infinity <= epsilon/2 < epsilon`. The zero-Lipschitz case is
handled separately by any singleton support.

Z3 checks the arbitrary-branch inequality symbolically. A separate
`fractions.Fraction` enumeration checks 867 boundary/interior assignments
without SMT. The negative control changes the radius to
`3 epsilon/(4 lambda)`; both checkers find that its `1.5 epsilon` admissible
error can violate the target.

The historical 1D grid remains available only as **Historical rejected
baseline** evidence. It is not part of the VERIFIED result.
