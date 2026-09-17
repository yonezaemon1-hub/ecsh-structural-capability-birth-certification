NAGI_ECSH_REPRO_V1_0_0
======================

PURPOSE
Fresh, auditable synthetic reproduction package for the frozen ECSH-Core.
The previously described NAGI_ECSH_V1_0_0 artifact was NOT found on the user's machine.
Therefore this package DOES NOT claim to reproduce the old 96.55% / 0.040 / 99.80% numbers.

FROZEN CORE TESTED
1. Freeze realized Child candidate.
2. Exclude candidate structure from the ancestral capability class.
3. Reoptimize that old class to select a Shadow Ancestor.
4. Compare Child vs Shadow on fresh held-out paired observations.
5. Structural admission uses cumulative alpha spending:
   alpha_i = 0.05 * 6/(pi^2*i^2)
6. Operational improvement and hereditary structural admission are separate.

SYNTHETIC GROUND TRUTH
TUNING: Child gain is attainable by the reoptimized old class.
STRUCTURE: Child contains a performance margin unavailable to the old class.
NULL: Child has no meaningful gain.
Ground-truth labels are used only for post-hoc metrics, never by the ECSH gate.

CANONICAL RUN
PowerShell in this folder:
  Set-ExecutionPolicy -Scope Process Bypass -Force
  & .\RUN_WINDOWS.ps1

The run creates a timestamped RUN_* evidence directory with:
- exact result JSON
- stdout log
- input/output SHA-256 manifests
- Python/platform metadata

OPTIONAL ROBUSTNESS
  & .\RUN_ROBUSTNESS_3SEEDS.ps1

CLAIM BOUNDARY
Synthetic only. No real NAGI self-modification validation is claimed.
