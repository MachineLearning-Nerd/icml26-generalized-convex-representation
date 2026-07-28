# C1 baseline method

This node reconstructs the judged finite-grid probe: three one-dimensional quadratics on 120 points with finite supports of sizes 4, 8, 16, 32, and 64.

That probe is a regression test for the historical artifact, not a test of the theorem's universal quantifiers. The exact contract is in `claim_contract.json`.

Negative control for later nodes: perturb the conjugation sign or reverse the support approximation inequality; the exact verifier must reject it.
