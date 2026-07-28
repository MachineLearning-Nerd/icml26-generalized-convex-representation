# C4 source audit

The hashed v1 Table I (`#S7.T1`) displays:

| n | learned mean profit/item | SJa revenue/item | exact at displayed precision |
| ---: | ---: | ---: | :---: |
| 1 | 0.250 | 0.250 | yes |
| 2 | 0.274 | 0.274 | yes |
| 5 | 0.314 | 0.315 | **no** |
| 10 | 0.346 | 0.347 | **no** |
| 20 | 0.377 | unavailable | not comparable |

The surrounding paper text says “virtually identical,” not “exactly.” The live
judge claim uses “matches ... exactly.” This verifier tests that literal live
claim without tolerance and therefore finds a direct source-level
contradiction at `n=5` and `n=10`.

The source URL, retrieval time, User-Agent, and SHA-256 are recorded in the
protected source audit.
