# C2 source and topology audit

The hashed v1 source states Proposition 3 at `#Thmproposition3`: uniform
convergence of functions sharing one semiconvexity constant implies gradient
convergence “uniformly where the gradients exist.” Theorem 2 at
`#Thmtheorem2` uses that proposition to claim density of the gradient class.

The paper cites Chaudhari, Pranav, and Moura, *Gradient Networks*,
arXiv:2404.07361. Its Lemma 2, in turn citing Rockafellar Theorem 25.7,
requires an **open convex** domain and finite **C1 convex** functions. It gives
pointwise gradient convergence on the open domain and uniform convergence only
on each compact subset of that domain. Those conditions are absent from the
v1 Proposition 3 and Theorem 2.

This is a proof and topology gap, not automatically a falsification of the
existential density conclusion.
