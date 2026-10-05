# compute-scg publication record — 2026-10-05

Owner request: create a skill variant called compute-scg, include the four topics
in the supplied image based on the Claude Science notes, place it in this registry
and push to main. This explicit instruction governs this change's direct-main
publication rather than the default review-branch flow. It does not assert that
the owner reviewed the finished implementation or that cluster jobs were rerun.

Scope: one standalone SCG skill, unchanged bundled SSH helper and tests, two
parameterized SBATCH templates, setup/operations references, source hashes,
registry/index/README/router/profile/changelog/provenance updates. Actual lab
accounts are retained in an ignored overlay; usernames, personal environment
paths, internal hostnames, raw attachment and unrelated app settings are excluded.

Historical evidence distinguishes completed P100 detection and CPU runs from
accepted-but-pending H200/A100 submissions. QOS allowance is separated from GPU
partition hardware/access. Obsolete key-bypasses-Duo and no-ControlPersist claims
are excluded. User-specific install permissions are not inherited by lab members.

Validation: registry checks passed (22 skills, 21 profiles); public-content scan
passed (109 text files); git diff --check passed; Bash syntax checks passed for
the helper and both templates; all 10 mocked SSH helper tests passed. CPU and GPU
templates executed with disposable local fixtures, a stub Conda activation and
mock nvidia-smi. Relative Markdown links and copied helper/test hashes verified.
Manual content review found no real personal paths, credentials, internal
endpoints or actual lab account names in the added public artifacts. The ignored
lab overlay is excluded from staging. The original portable skill remains intact.
No live SCG connection, Slurm submission, real environment activation or GPU
application was tested here. Historical results retain their supplied dates.
No redistribution license was assigned. Explicit owner publication authorization
is recorded above; no separate finished-artifact human review is claimed.
