# C5 evaluator contract

Mark **VERIFIED** only if:

- one-item price and revenue recover `0.5` and `0.25`;
- all three two-item seeds recover the primary-reference menu within fixed
  tolerances and have negligible spread;
- independent continuous-domain quadrature agrees with analytic revenue;
- the recovered bundle price is strictly between one and two singleton
  prices, so the menu is genuinely mixed;
- pure separate and pure bundle controls underperform; and
- the cumulative process exits nonzero on any failure.

Confidence is **MEDIUM** because the exact objective and parameterization are
faithful but the clean-room global optimizer is a documented substitution for
the official 100,000-step Torch training loop.
