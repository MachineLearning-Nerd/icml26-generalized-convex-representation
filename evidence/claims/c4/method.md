# C4 exact-decimal method

`repro/src/c4_table.py` parses the source-bound CSV with `Decimal`, compares all
available `n<=10` rows, and independently repeats the check as integer
thousandths. Both routes must identify exactly dimensions 5 and 10.

Negative control: weaken equality to absolute difference at most 0.001. That
corrupted predicate passes every row, demonstrating why tolerance-based
agreement cannot verify the word “exactly.” The verifier requires this false
positive to be exposed and rejected.
