---
name: compute-scg
description: Set up Stanford SCG SSH access, discover account and GPU access, size and submit Slurm jobs, and use project environments with lab-specific configuration.
license: NOASSERTION
---

# Compute on Stanford SCG

SCG-specific variant of the portable remote-compute-ssh workflow, derived at
its owner's request on 2026-10-05. Includes the standalone connection helper.
Use for SCG onboarding, CPU/GPU job preparation, submission, monitoring, and
result verification. Bash 3.2+ and OpenSSH with `ssh -G` are required locally;
Python is needed only for bundled helper tests.

## First connection

Read [connection setup](references/setup.md) for account enrollment, local
Terminal aliases, authentication, and connection shutdown. Establish the user's
own SUNet ID and SCG access. The bundled helper is `scripts/ssh-connect`;
resolve that path from this skill's directory. With a confirmed alias:

```bash
bash scripts/ssh-connect --host scg --non-interactive
```

If authentication is needed, give the same command without `--non-interactive`
for the user's Terminal. They enter their password and approve Duo there.
Verify a real remote response rather than only `ssh -O check`. Reuse a verified
connection across turns. Diagnose a failed master rather than closing the
user's sessions or repeating authentication requests. Keep credentials out of
chat and shared files. SSH access does not establish GPU or billing access.

## Project and lab context

Read remote project instructions before preparing jobs. For lab-specific work,
read the necessary fields in the consuming project's private overlay or this
registry's ignored `.local/compute-scg/settings.json`. Read data; do not source
it as executable shell code. The overlay provides the account map, billing
approval policy, environment, and shared work directory; see
[SCG operations](references/scg-operations.md) for its placeholder contract.
Confirm missing values with the user. Another member's account access,
installation permissions, environment paths, and resource budget do not transfer.

## Prepare and run jobs

Read [SCG operations](references/scg-operations.md) before sizing or submitting
jobs. It covers live discovery, account/partition selection, dated CPU/GPU
observations, environments/storage, and logging/path/SIGPIPE lessons.

- Login nodes are for light orchestration and inspection. Their probed hardware
  is not a job budget. Use Slurm for substantial computation.
- Discover the current user's accounts, partition/QOS limits, GPU types and
  node state. Report access, available hardware, and queue conditions separately.
- Size CPUs from useful parallelism, memory from workload/pilot evidence, and
  walltime from realistic runtime. Request GPUs only for GPU-capable work.
- Every job specifies account, partition, time, CPUs and memory; normally use
  one node and one task. Inspect project module/Conda instructions first.
- Carry forward existing authorization. Obtain approval for billed submissions,
  GPU use, large arrays, cancellation/resubmission, or material budget increases
  when the user's instructions have not already authorized them. Do not ask
  again for a job within an approved resource envelope.
- Copy and customize [CPU](templates/cpu.sbatch) or
  [P100 smoke](templates/gpu-p100-smoke.sbatch) templates. Replace every
  `REPLACE_*` token before `sbatch --test-only`; this checks submission acceptance,
  not successful execution or a guaranteed start time. Preserve user scripts.
- Submit authorized scripts with `sbatch --parsable`. Record the rendered script,
  account/partition, environment/modules, input/output locations, job ID,
  scheduler status, logs, and `sacct`/`seff` results. Check existing jobs first.
- Verify exit status and intended outputs. A completed GPU detection smoke test
  does not validate application compatibility or scientific results. SSH loss
  does not itself cancel Slurm jobs.

## Completion

Report what ran, what was only accepted/pending, what was checked locally, and
what remains unverified. Keep private values and run logs out of the public
registry. The dated source observations are historical evidence, not a current
cluster validation. Bundled helper tests: `python3 -m unittest discover -s tests`.

Bundled helper origin and hashes: [provenance](references/provenance.json).
