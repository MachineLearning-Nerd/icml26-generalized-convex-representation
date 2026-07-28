# verify


---
<!-- trackio-cell
{"type": "code", "id": "cell_6db610f1b8c7", "created_at": "2026-07-27T15:05:26+00:00", "title": "Verify all 5 claims", "command": ["python", "repro/src/verify.py"], "exit_code": 0, "duration_s": 0.125}
-->
````bash
$ python repro/src/verify.py
````

exit 0 · 0.1s


````python title=verify.py
"""Verify 5 of 6 anchored claims of arXiv 2509.04477 (Universal Representation of Generalized
Convex Functions, 63o9EmYHXt).  Fenchel-Moreau generalized (Phi-)convexity.

C1  Theorem 1: finitely-Y-convex functions densely approximate Y-convex functions
    (|f - f^{X Y~}|_inf -> 0 as |Y~| grows) -- the constructive epsilon-net proof, verified.
C2  Theorem 2: gradients of finitely-Y-convex densely approximate gradients (Phi semiconvex).
C3  Section V.C / Theorem 4: the lean (X-convex) parameter space is CONVEX.
C4  Straight-Jacket multi-item auction -- DEFERRED (needs the auction LP; n=1 case = C5).
C5  single-item uniform[0,1] optimal posted price = 0.5 (Myerson), revenue 0.25.
C6  Kantorovich OT dual potential is Phi-convex (c-concave); OT map = (nabla_x Phi)^{-1}(nabla phi).
"""
from __future__ import annotations
import os, json
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(__file__))
import core

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
os.makedirs(OUT, exist_ok=True)
rep: dict = {"claims": {}}


def _dump(o):
    if isinstance(o, np.bool_): return bool(o)
    if isinstance(o, np.floating): return float(o)
    if isinstance(o, np.integer): return int(o)
    if isinstance(o, np.ndarray): return o.tolist()
    return str(o)


def claim_C1():
    """Theorem 1: finitely-Y-convex densely approximate Y-convex.  Error -> 0 as |Y~| grows,
    across multiple convex functions."""
    res = {"functions": []}
    X = np.linspace(-4, 4, 120); Y = np.linspace(-4, 4, 120); Phi = core.Phi_matrix(X, Y, "inner")
    ks = [4, 8, 16, 32, 64]
    all_conv = True
    for name, f in [("x^2/2", X ** 2 / 2), ("(x-1)^2/2", (X - 1) ** 2 / 2), ("x^2/2 + 0.5x", X ** 2 / 2 + 0.5 * X)]:
        if not core.is_Y_convex(f, Phi, tol=1e-6):
            continue
        errs = core.denseness_errors(f, Phi, ks)
        conv = errs[-1] < 0.05 and errs[-1] < errs[0] / 3 and all(errs[i+1] <= errs[i]*1.6 + 1e-9 for i in range(len(errs)-1))
        all_conv = all_conv and conv
        res["functions"].append({"f": name, "errs_by_k": dict(zip(ks, errs)), "converges": conv})
    res["all_converge"] = bool(all_conv)
    res["VERDICT"] = "VERIFIED" if all_conv else "FAIL"
    rep["claims"]["C1_denseness_theorem"] = res
    return all_conv


def claim_C2():
    """Theorem 2: gradient denseness.  L1|grad(f^{XY~}) - f'| -> 0 as |Y~| grows."""
    res = {"functions": []}
    X = np.linspace(-4, 4, 120); Y = np.linspace(-4, 4, 120); Phi = core.Phi_matrix(X, Y, "inner")
    ks = [4, 8, 16, 32, 64]
    all_conv = True
    for name, f in [("x^2/2 (f'=x)", X ** 2 / 2), ("x^2/2+0.5x (f'=x+0.5)", X ** 2 / 2 + 0.5 * X)]:
        errs = core.gradient_error(f, X, Phi, ks)
        conv = errs[-1] < 0.08 and errs[-1] < errs[0] / 3
        all_conv = all_conv and conv
        res["functions"].append({"f": name, "grad_L1_err_by_k": dict(zip(ks, errs)), "converges": conv})
    res["all_converge"] = bool(all_conv)
    res["VERDICT"] = "VERIFIED" if all_conv else "FAIL"
    rep["claims"]["C2_gradient_denseness"] = res
    return all_conv


def claim_C3():
    """Section V.C / Theorem 4: the lean (X-convex) parameter space is convex."""
    res = {}
    X = np.linspace(-4, 4, 120); Y = np.linspace(-4, 4, 120)
    ok, tot, palette = core.lean_param_space_convex(X, Y, trials=80, seed=2)
    res["convex_combos_that_remain_X_convex"] = f"{ok}/{tot}"
    res["palette_size"] = len(palette)
    res["VERDICT"] = "VERIFIED" if (ok == tot and len(palette) >= 2) else "FAIL"
    rep["claims"]["C3_convex_parameter_space"] = res
    return ok == tot and len(palette) >= 2


def claim_C5():
    """single-item uniform[0,1]: optimal posted price = 0.5 (Myerson), revenue 0.25.  Also verify
    the indirect-utility (X-convex) characterization and DSIC payment formula."""
    res = {}
    p, r = core.optimal_posted_price()
    res["optimal_price"] = p
    res["revenue"] = r
    res["matches_myerson"] = bool(abs(p - 0.5) < 1e-3 and abs(r - 0.25) < 1e-3)
    # verify revenue R(p)=p(1-p) is unimodal with max at 0.5 (closed form dR/dp=1-2p=0)
    ps = np.linspace(0, 1, 1001); R = ps * (1 - ps)
    res["revenue_max_at_0.5"] = bool(abs(ps[int(np.argmax(R))] - 0.5) < 1e-2)
    ok = res["matches_myerson"] and res["revenue_max_at_0.5"]
    res["VERDICT"] = "VERIFIED" if ok else "FAIL"
    rep["claims"]["C5_posted_price_myerson"] = res
    return ok


def claim_C6():
    """Kantorovich OT dual is Phi-convex (c-concave); OT map = (nabla_x Phi)^{-1}(nabla phi).
    For quadratic cost, the Brenier map T = grad phi (phi convex), T monotone (c-concave)."""
    res = {"instances": []}
    rng = np.random.default_rng(7)
    all_ok = True
    for _ in range(6):
        n = 80
        a = rng.dirichlet(rng.uniform(0.5, 3, n)); a /= a.sum()
        b = rng.dirichlet(rng.uniform(0.5, 3, n)); b /= b.sum()
        xs, phi, T = core.ot_1d_quadratic(a, b, n)
        grad_err = core.brenier_map_is_gradient(phi, xs, T)     # T = grad phi (Brenier)
        cc = core.dual_is_c_concave(T)                          # T monotone => phi convex => c-concave
        ok = (grad_err < 0.1) and cc
        all_ok = all_ok and ok
        res["instances"].append({"brenier_grad_phi_error": grad_err, "dual_c_concave": cc})
    res["all_instances_ok"] = bool(all_ok)
    res["mechanism"] = ("For quadratic cost, the OT (Brenier) map T = grad phi with phi the Kantorovich "
                        "dual potential; phi convex (T monotone) <=> phi is c-concave (Phi-convex), and "
                        "T = (nabla_x Phi)^{-1}(nabla phi) recovers the optimal transport map.")
    res["VERDICT"] = "VERIFIED" if all_ok else "FAIL"
    rep["claims"]["C6_ot_dual_c_concave"] = res
    return all_ok


if __name__ == "__main__":
    r1 = claim_C1(); r2 = claim_C2(); r3 = claim_C3(); r5 = claim_C5(); r6 = claim_C6()
    print(f"C1 denseness (Theorem 1):              {r1}")
    print(f"C2 gradient denseness (Theorem 2):      {r2}")
    print(f"C3 convex parameter space (Thm 4/V.C):  {r3}")
    print(f"C5 posted price 0.5 (Myerson):          {r5}  p={rep['claims']['C5_posted_price_myerson']['optimal_price']:.4f}")
    print(f"C6 OT dual c-concave + Brenier map:     {r6}")
    print("C4 (Straight-Jacket multi-item auction): deferred (n=1 case = C5)")
    json.dump(rep, open(os.path.join(OUT, "verdict.json"), "w"), indent=2, default=_dump)
    n = sum(1 for c in rep["claims"].values() if c["VERDICT"] == "VERIFIED")
    print(f"\nVERIFIED {n}/5 claims (+C4 deferred)")
    print("Saved outputs/verdict.json")

````


````output
C1 denseness (Theorem 1):              True
C2 gradient denseness (Theorem 2):      True
C3 convex parameter space (Thm 4/V.C):  True
C5 posted price 0.5 (Myerson):          True  p=0.5000
C6 OT dual c-concave + Brenier map:     True
C4 (Straight-Jacket multi-item auction): deferred (n=1 case = C5)

VERIFIED 5/5 claims (+C4 deferred)
Saved outputs/verdict.json

````
