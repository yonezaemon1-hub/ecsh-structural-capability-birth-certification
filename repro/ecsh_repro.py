#!/usr/bin/env python3
import argparse, json, math, random, hashlib, os, statistics, time
from functools import lru_cache
from pathlib import Path

VERSION = "NAGI_ECSH_REPRO_V1_0_0"


def clamp(x, lo=0.01, hi=0.99):
    return max(lo, min(hi, x))


@lru_cache(maxsize=None)
def binom_tail_ge(k, n, p=0.5):
    """Exact one-sided Binomial(n,p) tail P[X>=k], stdlib only."""
    if n <= 0:
        return 1.0
    # stable enough for n<=60
    s = 0.0
    for x in range(k, n + 1):
        s += math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x))
    return min(1.0, s)


def mcnemar_one_sided(a, b):
    """a,b are 0/1 lists on paired cases. Tests a>b using discordant pairs."""
    wins = sum(1 for x, y in zip(a, b) if x == 1 and y == 0)
    losses = sum(1 for x, y in zip(a, b) if x == 0 and y == 1)
    n = wins + losses
    return binom_tail_ge(wins, n, 0.5), wins, losses


def make_old_class(rng, kind, k=16):
    base = rng.uniform(0.30, 0.50)
    if kind == "TUNING":
        parent = clamp(base)
        target_best = clamp(base + rng.uniform(0.25, 0.35), hi=0.88)
        vals = [clamp(target_best - abs(rng.gauss(0.0, 0.035)), hi=0.90) for _ in range(k-1)]
        vals.append(target_best)
        child = clamp(target_best - rng.uniform(0.0, 0.01), hi=0.90)
    elif kind == "STRUCTURE":
        parent = clamp(base)
        target_best = clamp(base + rng.uniform(0.00, 0.03), hi=0.60)
        vals = [clamp(target_best - abs(rng.gauss(0.0, 0.02)), hi=0.80) for _ in range(k-1)]
        vals.append(target_best)
        child = rng.uniform(0.97, 0.995)
    elif kind == "NULL":
        parent = clamp(base)
        target_best = clamp(base + rng.uniform(0.00, 0.04), hi=0.78)
        vals = [clamp(target_best - abs(rng.gauss(0.0, 0.02)), hi=0.80) for _ in range(k-1)]
        vals.append(target_best)
        child = clamp(parent + rng.uniform(-0.01, 0.01), hi=0.80)
    else:
        raise ValueError(kind)
    return parent, vals, child


def reoptimize_shadow(rng, true_vals, n_reopt):
    # Synthetic proxy for a bounded but substantial reoptimization of the old class:
    # estimate every ancestral configuration on an independent optimization sample,
    # then return the true performance of the selected configuration.
    est = []
    for p in true_vals:
        sd = math.sqrt(max(1e-9, p * (1-p) / n_reopt))
        est.append(clamp(rng.gauss(p, sd)))
    idx = max(range(len(est)), key=est.__getitem__)
    return true_vals[idx], idx, est[idx]


def eval_triplet(rng, p_parent, p_child, p_shadow, n_holdout, difficulty_sd):
    parent, child, shadow = [], [], []
    for _ in range(n_holdout):
        d = rng.gauss(0.0, difficulty_sd)
        pp = clamp(p_parent + d)
        pc = clamp(p_child + d)
        ps = clamp(p_shadow + d)
        parent.append(1 if rng.random() < pp else 0)
        child.append(1 if rng.random() < pc else 0)
        shadow.append(1 if rng.random() < ps else 0)
    return parent, child, shadow


def alpha_i(i, family_alpha):
    return family_alpha * 6.0 / (math.pi**2 * i * i)


def run_one_lifetime(rng, spec):
    kinds = (["TUNING"] * spec["counts_per_lifetime"]["tuning"] +
             ["STRUCTURE"] * spec["counts_per_lifetime"]["structure"] +
             ["NULL"] * spec["counts_per_lifetime"]["null"])
    rng.shuffle(kinds)
    test_counter = 0
    rows = []
    false_birth = False
    for pos, kind in enumerate(kinds, start=1):
        p_parent, old_class, p_child = make_old_class(rng, kind, spec["old_class_size"])
        p_shadow, shadow_idx, shadow_est = reoptimize_shadow(rng, old_class, spec["reopt_samples_per_config"])
        parent, child, shadow = eval_triplet(
            rng, p_parent, p_child, p_shadow,
            spec["fresh_holdout_pairs"], spec["case_difficulty_sd"])

        p_cp, cp_wins, cp_losses = mcnemar_one_sided(child, parent)
        p_cs, cs_wins, cs_losses = mcnemar_one_sided(child, shadow)

        # Gate A: raw parent-relative improvement, no statistical certificate.
        gate_a = (sum(child) > sum(parent))
        # Gate B: SGM-like incumbent statistical gate (simplified comparator).
        gate_b = (sum(child) > sum(parent) and p_cp < 0.05)
        # Gate Raw-Shadow: no cumulative error control.
        gate_raw_shadow = (sum(child) > sum(shadow) and p_cs < 0.05)

        # ECSH ledger: every candidate structural-admission test consumes the next alpha_i.
        test_counter += 1
        ai = alpha_i(test_counter, spec["family_alpha"])
        gate_ecsh = (sum(child) > sum(shadow) and p_cs < ai)

        if gate_ecsh and kind != "STRUCTURE":
            false_birth = True

        rows.append({
            "position": pos, "kind": kind,
            "p_parent": p_parent, "p_child": p_child, "p_shadow": p_shadow,
            "shadow_index": shadow_idx, "shadow_estimate": shadow_est,
            "holdout_parent": sum(parent), "holdout_child": sum(child), "holdout_shadow": sum(shadow),
            "p_child_vs_parent": p_cp, "p_child_vs_shadow": p_cs,
            "alpha_i": ai,
            "gate_a": gate_a, "gate_b": gate_b,
            "gate_raw_shadow": gate_raw_shadow, "gate_ecsh": gate_ecsh,
            "cp_wins": cp_wins, "cp_losses": cp_losses,
            "cs_wins": cs_wins, "cs_losses": cs_losses,
        })
    return rows, false_birth


def summarize(all_rows, false_birth_lifetimes, lifetimes):
    out = {}
    for gate in ["gate_a", "gate_b", "gate_raw_shadow", "gate_ecsh"]:
        tp = sum(1 for r in all_rows if r["kind"] == "STRUCTURE" and r[gate])
        fn = sum(1 for r in all_rows if r["kind"] == "STRUCTURE" and not r[gate])
        fp = sum(1 for r in all_rows if r["kind"] != "STRUCTURE" and r[gate])
        tn = sum(1 for r in all_rows if r["kind"] != "STRUCTURE" and not r[gate])
        out[gate] = {
            "structural_recall": tp / (tp + fn) if tp + fn else None,
            "false_heritable_births_total": fp,
            "false_heritable_births_per_lifetime": fp / lifetimes,
            "precision": tp / (tp + fp) if tp + fp else None,
            "tp": tp, "fn": fn, "fp": fp, "tn": tn,
        }
    out["gate_ecsh"]["p_any_false_birth_per_lifetime"] = false_birth_lifetimes / lifetimes
    out["gate_ecsh"]["lifetimes_with_any_false_birth"] = false_birth_lifetimes
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spec', default='ECSH_REPRO_SPEC.json')
    ap.add_argument('--out', default='results.json')
    ap.add_argument('--seed', type=int, default=None)
    args = ap.parse_args()
    spec_path = Path(args.spec)
    spec = json.loads(spec_path.read_text(encoding='utf-8'))
    seed = spec["canonical_seed"] if args.seed is None else args.seed
    rng = random.Random(seed)

    start = time.time()
    all_rows = []
    false_birth_lifetimes = 0
    for _ in range(spec["lifetimes"]):
        rows, false_birth = run_one_lifetime(rng, spec)
        all_rows.extend(rows)
        false_birth_lifetimes += int(false_birth)
    summary = summarize(all_rows, false_birth_lifetimes, spec["lifetimes"])

    result = {
        "status": "PASS_RECONSTRUCTED_ECSH_SYNTHETIC_REPRO_EXECUTED",
        "version": VERSION,
        "claim_boundary": {
            "recreates_original_missing_artifact": False,
            "uses_frozen_ecsh_core": True,
            "synthetic_only": True,
            "real_self_modification_validated": False,
            "old_9655_result_claimed_reproduced": False
        },
        "seed": seed,
        "spec": spec,
        "summary": summary,
        "elapsed_seconds": round(time.time()-start, 3),
        "python": __import__('sys').version,
        "platform": __import__('platform').platform(),
    }
    Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')

    print(json.dumps({
        "status": result["status"],
        "seed": seed,
        "ecsh": summary["gate_ecsh"],
        "comparators": {k: summary[k] for k in ["gate_a", "gate_b", "gate_raw_shadow"]},
        "output": str(Path(args.out).resolve()),
        "elapsed_seconds": result["elapsed_seconds"]
    }, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
