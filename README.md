# ECSH: Certifying Structural Capability Birth in Self-Modifying Systems via Reoptimized Ancestral Counterfactuals

Ryutaro Yonezu — Independent Researcher, Japan

Version 1.0.0, published 17 September 2026.

- Paper DOI: `10.5281/zenodo.22806440`
- Software/Evidence DOI: `10.5281/zenodo.22806442`
- Repository: https://github.com/yonezaemon1-hub/ecsh-structural-capability-birth-certification

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

The earlier historical candidate-level raw artifact was not recovered in the bounded local search. The public evidence is therefore a fresh deterministic regeneration from the frozen source/specification and is not represented as recovered historical raw.

## Evidence and immutable identities

Full fresh-regeneration evidence archive:

- `NO15_ECSH_PUBLIC_EVIDENCE_REBUILD_20260917_135911.zip`
- SHA-256 `3894d5ac995ff26a1d97dde01d91da304ae9bfbd355a329964b8ff26a08c1042`
- 960,000 candidate rows
- Software/Evidence DOI `10.5281/zenodo.22806442`

Frozen public reproduction archive:

- `NAGI_ECSH_REPRO_V1_0_0.zip`
- SHA-256 `ac8d1f0765561bfc5b67442e58636a601602073049b24608df4285a3080912e4`

Final paper:

- DOCX SHA-256 `0677bd27b1f6d4768696dec5c1679a9b56703bcaa9597b4f30154ae975006536`
- PDF SHA-256 `7ff69867c04f4e016653ea7fd4e0be9c018ce87f3a381fa03d6a57dffc8cd78e`
- Paper DOI `10.5281/zenodo.22806440`

The full 960,000-row evidence archive is intentionally not stored in GitHub because it is a large data artifact; it belongs in the Software/Evidence Zenodo deposit.

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

## Release

The Paper and Software/Evidence records above were published on Zenodo on 17 September 2026. The GitHub `v1.0.0` tag/release is the final repository release marker for this publication.
