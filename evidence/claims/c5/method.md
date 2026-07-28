# C5 method

The four allocation-price branches are `(0,0;0)`, `(1,0;p1)`,
`(0,1;p1)`, and `(1,1;p2)`. Their maximum utility is exactly a finite
generalized-convex function with the paper's linear kernel.

The verifier analytically integrates the continuous uniform type domain,
optimizes over the full symmetric mixed-menu parameter region with three
seeds, and compares the recovered prices only after optimization. An
independent midpoint quadrature at 200², 400², and 800² cells recomputes
revenue directly from buyer choices.

Pure separate selling and the globally optimized pure bundle are negative
controls; each must lose at least 0.003 total revenue to the mixed menu.
