# C5 source audit

The v1 paper's Figures 2–3 claim recovery of:

- one item: posted price `1/2`, revenue `1/4`;
- two items: a menu that is neither separate selling nor pure bundling and is
  similar to the Straight-Jacket auction.

Primary reference arXiv:1404.2329 derives the two-item SJA prices:

- each singleton: `p1 = 2/3`;
- both items: `p2 = (4-sqrt(2))/3`.

The verifier uses those formulas only as held-out benchmarks. It searches the
full symmetric mixed-menu region `0 <= p1 <= 1`, `p1 <= p2 <= 2 p1` through
the noncircular coordinates `p1` and `q/p1`, with three deterministic seeds.
