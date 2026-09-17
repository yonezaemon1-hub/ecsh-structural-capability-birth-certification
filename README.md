# ECSH: Certifying Structural Capability Birth in Self-Modifying Systems via Reoptimized Ancestral Counterfactuals

Ryutaro Yonezu — Independent Researcher, Japan

This repository is the pre-DOI public-release repository for ECSH.

## Scope

ECSH is a structural-attribution protocol for deciding whether a candidate structural element may become available to future candidate generation relative to a declared pre-change capability boundary.

The narrow core is:

1. preserve the identity of the candidate child;
2. reconstruct or constrain the pre-c ancestral capability class from versioned state;
3. disable the candidate structure and required equivalents;
4. reoptimize/search/enumerate/upper-bound the old class under a declared refutation-sufficiency condition;
5. compare the child and the counterfactual old-class evidence on informationally isolated evaluation data;
6. keep operational adoption separate from structural attribution; and
7. update future structural availability only after the declared non-reducibility test passes.

## Reproduction status

A fresh deterministic regeneration was performed on 17 September 2026 from the frozen public reproduction source/specification using seeds 20260816, 20260819, 20260820, and 20260821.

- 240,000 candidate rows per seed
- 960,000 candidate rows total
- canonical recall: 97.55%
- canonical false heritable births: 24
- canonical false births/lifetime: 0.020
- canonical precision: 99.8976%
- fresh three-seed mean recall: 97.5014%
- fresh mean false births/lifetime: 0.01944
- fresh mean precision: 99.9004%

The earlier historical candidate-level raw artifact was not recovered in the bounded local search. The current public evidence is therefore a fresh deterministic regeneration from the frozen source/specification and must not be represented as recovered historical raw.

## Evidence

The full 960,000-row evidence archive is intentionally not stored in this GitHub repository because it is a large data artifact. Its immutable local pre-DOI identity is recorded in `evidence/EVIDENCE_POINTER.md`. The release archive will be deposited separately with a DOI before final v1.0.0 freeze.

## Claim boundary

The synthetic experiment calibrates gate behavior in a known-label control. It does not establish:

- real-world structural capability birth;
- deployment safety;
- absolute impossibility of all candidate-free implementations;
- legal novelty, inventive step, patent validity, infringement, or freedom to operate.

## Patent status

A Japanese patent application covering the narrow ECSH core was filed on 19 August 2026. Publication of this repository does not grant a patent license.

## Rights

Copyright © 2026 Ryutaro Yonezu. All rights reserved. See `RIGHTS_NOTICE.md`.

## DOI

DOI metadata will be inserted after reservation. This repository is intentionally pre-DOI at this commit.
